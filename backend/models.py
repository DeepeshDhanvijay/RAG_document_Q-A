from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    upload_time: str
    chunk_count: int
    message: str

class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_time: str
    chunk_count: int
    file_size: int

class QueryRequest(BaseModel):
    document_id: str
    question: str

class SourceReference(BaseModel):
    chunk_text: str
    relevance_score: float
    chunk_index: int

class QueryResponse(BaseModel):
    question: str
    answer: str
    document_id: str
    document_name: str
    sources: List[SourceReference]
    processing_time: float

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
