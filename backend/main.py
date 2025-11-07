from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import time
import shutil
from pathlib import Path
from typing import List

from config import config
from models import (
    DocumentUploadResponse, 
    DocumentInfo, 
    QueryRequest, 
    QueryResponse,
    SourceReference,
    ErrorResponse
)
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_service import LLMService
from database import DatabaseService

# Initialize FastAPI app
app = FastAPI(
    title="RAG Document Q&A API",
    description="API for document upload and question answering using RAG",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP
)
vector_store = VectorStore(
    model_name=config.EMBEDDING_MODEL,
    store_dir=config.VECTOR_STORE_DIR
)
llm_service = LLMService(api_key=config.GROQ_API_KEY)
db_service = DatabaseService()

# Create necessary directories
os.makedirs(config.UPLOAD_DIR, exist_ok=True)
os.makedirs(config.VECTOR_STORE_DIR, exist_ok=True)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "RAG Document Q&A API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/documents/upload",
            "list": "/api/documents",
            "query": "/api/documents/query",
            "delete": "/api/documents/{document_id}"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/api/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF or TXT) and process it for RAG
    """
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not supported. Allowed types: {', '.join(config.ALLOWED_EXTENSIONS)}"
            )
        
        # Validate file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {config.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = os.path.join(config.UPLOAD_DIR, f"{document_id}{file_extension}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document: extract text and chunk
        try:
            full_text, chunks = document_processor.process_document(file_path, file_extension)
        except Exception as e:
            # Clean up file if processing fails
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Error processing document: {str(e)}")
        
        # Create embeddings and store in vector database
        metadata = {
            "filename": file.filename,
            "document_id": document_id,
            "chunk_count": len(chunks),
            "upload_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            vector_store.process_and_store(document_id, chunks, metadata)
        except Exception as e:
            # Clean up file if vector storage fails
            os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error creating vector store: {str(e)}")
        
        # Save document metadata to database
        db_service.create_document(
            document_id=document_id,
            filename=file.filename,
            chunk_count=len(chunks),
            file_size=file_size
        )
        
        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            upload_time=metadata["upload_time"],
            chunk_count=len(chunks),
            message="Document uploaded and processed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/documents", response_model=List[DocumentInfo])
async def get_documents():
    """
    Retrieve list of all uploaded documents
    """
    try:
        # Get documents from database
        documents = db_service.get_all_documents()
        
        # If database is empty, try to get from vector store directory
        if not documents:
            vector_store_path = Path(config.VECTOR_STORE_DIR)
            if vector_store_path.exists():
                documents = []
                for doc_dir in vector_store_path.iterdir():
                    if doc_dir.is_dir():
                        metadata_file = doc_dir / "metadata.json"
                        if metadata_file.exists():
                            import json
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                                documents.append({
                                    "id": metadata.get("document_id"),
                                    "filename": metadata.get("filename"),
                                    "upload_time": metadata.get("upload_time"),
                                    "chunk_count": metadata.get("chunk_count"),
                                    "file_size": 0
                                })
        
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


@app.post("/api/documents/query", response_model=QueryResponse)
async def query_document(query_request: QueryRequest):
    """
    Ask a question about a specific document
    """
    start_time = time.time()
    
    try:
        # Validate inputs
        if not query_request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Retrieve relevant chunks from vector store
        try:
            results = vector_store.search(
                document_id=query_request.document_id,
                query=query_request.question,
                top_k=config.TOP_K_RESULTS
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching vector store: {str(e)}")
        
        if not results:
            raise HTTPException(status_code=404, detail="No relevant information found in document")
        
        # Generate answer using LLM
        try:
            answer = llm_service.generate_answer(query_request.question, results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
        
        # Get document metadata
        doc_metadata = db_service.get_document(query_request.document_id)
        document_name = doc_metadata["filename"] if doc_metadata else "Unknown Document"
        
        # Prepare source references
        sources = [
            SourceReference(
                chunk_text=chunk_text[:300] + "..." if len(chunk_text) > 300 else chunk_text,
                relevance_score=round(score, 4),
                chunk_index=idx
            )
            for chunk_text, score, idx in results
        ]
        
        # Save query to history (optional)
        try:
            db_service.save_query_history(
                document_id=query_request.document_id,
                question=query_request.question,
                answer=answer
            )
        except:
            pass  # Don't fail if history save fails
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            question=query_request.question,
            answer=answer,
            document_id=query_request.document_id,
            document_name=document_name,
            sources=sources,
            processing_time=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and its associated data
    """
    try:
        # Delete from database
        db_service.delete_document(document_id)
        
        # Delete vector store
        try:
            vector_store.delete_index(document_id)
        except:
            pass  # Continue even if vector store deletion fails
        
        # Delete uploaded file
        upload_path = Path(config.UPLOAD_DIR)
        for file_path in upload_path.glob(f"{document_id}.*"):
            try:
                os.remove(file_path)
            except:
                pass
        
        return {
            "message": "Document deleted successfully",
            "document_id": document_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")


@app.get("/api/documents/{document_id}/history")
async def get_document_history(document_id: str):
    """
    Get query history for a specific document (bonus feature)
    """
    try:
        history = db_service.get_query_history(document_id)
        return {
            "document_id": document_id,
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
