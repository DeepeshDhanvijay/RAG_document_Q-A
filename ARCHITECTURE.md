# RAG Document Q&A - Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                    http://localhost:3000                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                           │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────────┐  │
│  │  Upload    │  │ Document   │  │   Q&A Interface          │  │
│  │  Component │  │ List       │  │   + Source Display       │  │
│  └────────────┘  └────────────┘  └──────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              API Service (Axios)                         │  │
│  │  - uploadDocument()   - queryDocument()                  │  │
│  │  - getDocuments()     - deleteDocument()                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ REST API Calls
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                             │
│                 http://localhost:8000                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  API Endpoints                           │  │
│  │  POST   /api/documents/upload                            │  │
│  │  GET    /api/documents                                   │  │
│  │  POST   /api/documents/query                             │  │
│  │  DELETE /api/documents/{id}                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │  Document   │  │ Vector Store │  │   LLM Service      │    │
│  │  Processor  │  │   (FAISS)    │  │   (Groq API)       │    │
│  │             │  │              │  │                    │    │
│  │ - Extract   │  │ - Embed      │  │ - Generate Answer  │    │
│  │ - Chunk     │  │ - Index      │  │ - Context Prompt   │    │
│  │ - Clean     │  │ - Search     │  │ - Llama 3-8B       │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Database Service                            │  │
│  │              (Supabase Client)                           │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────────┘
                          │
                          │ PostgreSQL Protocol
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SUPABASE (PostgreSQL)                         │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────────────┐    │
│  │   documents table   │    │   query_history table       │    │
│  │  - id               │    │  - document_id              │    │
│  │  - filename         │    │  - question                 │    │
│  │  - chunk_count      │    │  - answer                   │    │
│  │  - file_size        │    │  - query_time               │    │
│  │  - upload_time      │    └─────────────────────────────┘    │
│  └─────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   LOCAL FILE SYSTEM                             │
│                                                                  │
│  uploads/                      vector_store/                    │
│  ├── {uuid}.pdf                ├── {uuid}/                      │
│  ├── {uuid}.txt                │   ├── index.faiss              │
│  └── ...                       │   ├── chunks.pkl               │
│                                │   └── metadata.json            │
│                                └── ...                           │
└─────────────────────────────────────────────────────────────────┘
```

## RAG Pipeline Flow

```
1. DOCUMENT UPLOAD
   ┌─────────────┐
   │   User      │
   │  Uploads    │
   │  PDF/TXT    │
   └──────┬──────┘
          │
          ▼
   ┌─────────────────────┐
   │  File Validation    │
   │  - Type: .pdf/.txt  │
   │  - Size: < 10MB     │
   │  - Not empty        │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Text Extraction    │
   │  - PyPDF2 for PDF   │
   │  - File read for TXT│
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │   Text Chunking     │
   │  - 500 chars/chunk  │
   │  - 50 char overlap  │
   │  - Sentence-aware   │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Generate Embeddings│
   │  Sentence-Transformers│
   │  all-MiniLM-L6-v2   │
   │  → 384-dim vectors  │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │   FAISS Indexing    │
   │  - Normalize vectors│
   │  - Create L2 index  │
   │  - Persist to disk  │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Store Metadata     │
   │  - Supabase DB      │
   │  - Local JSON       │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │   Return Success    │
   │  + Document ID      │
   │  + Chunk Count      │
   └─────────────────────┘

2. QUESTION ANSWERING
   ┌─────────────┐
   │   User      │
   │  Asks       │
   │  Question   │
   └──────┬──────┘
          │
          ▼
   ┌─────────────────────┐
   │  Generate Query     │
   │  Embedding          │
   │  Same model as docs │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Similarity Search  │
   │  FAISS.search()     │
   │  → Top K=3 chunks   │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Rank by Relevance  │
   │  L2 distance → score│
   │  Return best matches│
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Construct Prompt   │
   │  System: "You are...│
   │  Context: chunks    │
   │  Question: user q   │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Call Groq LLM      │
   │  Model: Llama3-8B   │
   │  Temperature: 0.3   │
   │  Max tokens: 1024   │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │  Return Answer      │
   │  + Source chunks    │
   │  + Relevance scores │
   │  + Processing time  │
   └─────────────────────┘
```

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      USER ACTIONS                            │
└─────────┬────────────────────────┬───────────────────────────┘
          │                        │
          │ Upload File            │ Ask Question
          ▼                        ▼
┌─────────────────┐      ┌─────────────────────────────┐
│  FileUpload.tsx │      │    QAInterface.tsx          │
│                 │      │                             │
│ - Drag & Drop   │      │ - Question Input            │
│ - File Select   │      │ - Submit Button             │
│ - Progress Bar  │      │ - Answer Display            │
└────────┬────────┘      └────────┬────────────────────┘
         │                        │
         │ useDocumentUpload()    │
         ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│                  useDocuments.ts (Hook)                 │
│                                                         │
│  - uploadDocument()  - queryDocument()                  │
│  - deleteDocument()  - refreshDocuments()               │
└────────┬────────────────────────┬───────────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│                    api.ts (Service)                     │
│                                                         │
│  APIService class with Axios HTTP calls                 │
└────────┬────────────────────────┬───────────────────────┘
         │                        │
         │ HTTP POST              │ HTTP POST
         ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)                  │
│                                                         │
│  @app.post("/api/documents/upload")                     │
│  @app.post("/api/documents/query")                      │
└────────┬────────────────────────┬───────────────────────┘
         │                        │
         │ Process Document       │ Query Document
         ▼                        ▼
┌──────────────────┐    ┌─────────────────────────────┐
│ DocumentProcessor│    │      VectorStore            │
│                  │    │                             │
│ extract_text()   │    │ search()                    │
│ chunk_text()     │    │ → retrieve top 3 chunks     │
└────────┬─────────┘    └────────┬────────────────────┘
         │                       │
         │ Chunks                │ Context Chunks
         ▼                       ▼
┌──────────────────┐    ┌─────────────────────────────┐
│   VectorStore    │    │      LLMService             │
│                  │    │                             │
│ create_embeddings│    │ generate_answer()           │
│ create_index()   │    │ → Call Groq API             │
│ save_index()     │    │ → Return answer             │
└──────────────────┘    └─────────────────────────────┘
```

## Data Flow - Upload Process

```
User File (PDF/TXT)
      │
      ▼
[Frontend Validation]
      │
      ├─ Valid file? ──No──> Error Message
      │
      Yes
      ▼
[Upload to Backend via FormData]
      │
      ▼
[Backend Validation]
      │
      ├─ Type/Size OK? ──No──> 400 Error
      │
      Yes
      ▼
[Save to uploads/{uuid}.ext]
      │
      ▼
[Extract Text]
      │
      ├─ PDF ──> PyPDF2.PdfReader()
      │
      └─ TXT ──> open().read()
      │
      ▼
[Clean & Normalize Text]
      │
      ├─ Remove excess whitespace
      ├─ Normalize punctuation
      └─ Remove special chars
      │
      ▼
[Chunk Text]
      │
      ├─ Split by sentences
      ├─ Combine into 500-char chunks
      └─ Add 50-char overlap
      │
      ▼
[Generate Embeddings]
      │
      ├─ Load Sentence-BERT model
      ├─ Encode each chunk
      └─ Get 384-dim vectors
      │
      ▼
[Create FAISS Index]
      │
      ├─ Normalize vectors (L2)
      ├─ Create IndexFlatL2
      └─ Add vectors to index
      │
      ▼
[Persist to Disk]
      │
      ├─ vector_store/{uuid}/index.faiss
      ├─ vector_store/{uuid}/chunks.pkl
      └─ vector_store/{uuid}/metadata.json
      │
      ▼
[Save to Database]
      │
      └─ Supabase: documents table
      │
      ▼
[Return Response to Frontend]
      │
      ├─ document_id
      ├─ filename
      ├─ chunk_count
      └─ upload_time
      │
      ▼
[Update UI]
      │
      ├─ Add to document list
      ├─ Show success message
      └─ Reset upload form
```

## Data Flow - Query Process

```
User Question
      │
      ▼
[Frontend Input]
      │
      ▼
[Submit to Backend]
      │
      └─ POST /api/documents/query
         {document_id, question}
      │
      ▼
[Load Document's Vector Store]
      │
      ├─ Read index.faiss
      └─ Read chunks.pkl
      │
      ▼
[Generate Query Embedding]
      │
      └─ Same model as documents
         "What is the main conclusion?"
         → [0.123, -0.456, 0.789, ...]
      │
      ▼
[FAISS Similarity Search]
      │
      ├─ Compare with all doc vectors
      ├─ Calculate L2 distances
      └─ Return top K=3 closest
      │
      ▼
[Calculate Relevance Scores]
      │
      └─ score = 1 / (1 + distance)
      │
      ▼
[Prepare Context]
      │
      └─ [Chunk 1]
         [Chunk 2]
         [Chunk 3]
      │
      ▼
[Construct LLM Prompt]
      │
      └─ System: You are a helpful assistant...
         Context: {chunks}
         Question: {user_question}
      │
      ▼
[Call Groq API]
      │
      ├─ Model: llama3-8b-8192
      ├─ Temperature: 0.3
      └─ Max tokens: 1024
      │
      ▼
[Receive LLM Response]
      │
      └─ Generated answer text
      │
      ▼
[Prepare Response]
      │
      ├─ question
      ├─ answer
      ├─ sources (with scores)
      └─ processing_time
      │
      ▼
[Return to Frontend]
      │
      ▼
[Display Answer]
      │
      ├─ Show answer text
      ├─ Show processing time
      └─ Expandable sources
      │
      ▼
[Save to History (Optional)]
      │
      └─ Supabase: query_history table
```

## Technology Integration Map

```
┌─────────────────────────────────────────────────────────┐
│                    TECHNOLOGIES                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Frontend Layer                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │  Next.js 14 (React Framework)                │      │
│  │    ├─ App Router                             │      │
│  │    ├─ Server Components                      │      │
│  │    └─ Client Components ('use client')       │      │
│  │                                               │      │
│  │  TypeScript (Type Safety)                    │      │
│  │    ├─ Interface definitions                  │      │
│  │    ├─ Type checking                          │      │
│  │    └─ IDE support                            │      │
│  │                                               │      │
│  │  Tailwind CSS (Styling)                      │      │
│  │    ├─ Utility classes                        │      │
│  │    ├─ Responsive design                      │      │
│  │    └─ Custom components                      │      │
│  │                                               │      │
│  │  Axios (HTTP Client)                         │      │
│  │    ├─ API calls                              │      │
│  │    ├─ Error handling                         │      │
│  │    └─ Request/Response interceptors          │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  Backend Layer                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │  FastAPI (Web Framework)                     │      │
│  │    ├─ Async endpoints                        │      │
│  │    ├─ Auto documentation (Swagger)           │      │
│  │    ├─ Pydantic validation                    │      │
│  │    └─ CORS middleware                        │      │
│  │                                               │      │
│  │  Python 3.8+ (Language)                      │      │
│  │    ├─ Type hints                             │      │
│  │    ├─ Async/await                            │      │
│  │    └─ Context managers                       │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  RAG Components                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │  FAISS (Vector Database)                     │      │
│  │    ├─ IndexFlatL2 (L2 distance)              │      │
│  │    ├─ Vector normalization                   │      │
│  │    └─ Similarity search                      │      │
│  │                                               │      │
│  │  Sentence Transformers (Embeddings)          │      │
│  │    ├─ all-MiniLM-L6-v2 model                 │      │
│  │    ├─ 384-dimensional vectors                │      │
│  │    └─ Fast inference                         │      │
│  │                                               │      │
│  │  Groq (LLM Provider)                         │      │
│  │    ├─ Llama 3-8B model                       │      │
│  │    ├─ Very fast inference (~200 tokens/s)    │      │
│  │    └─ Generous free tier                     │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  Data Layer                                             │
│  ┌──────────────────────────────────────────────┐      │
│  │  Supabase (Backend-as-a-Service)             │      │
│  │    ├─ PostgreSQL database                    │      │
│  │    ├─ Auto-generated REST API                │      │
│  │    └─ Real-time subscriptions                │      │
│  │                                               │      │
│  │  File System (Local Storage)                 │      │
│  │    ├─ uploads/ - Original files              │      │
│  │    └─ vector_store/ - FAISS indices          │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
│  Document Processing                                    │
│  ┌──────────────────────────────────────────────┐      │
│  │  PyPDF2 (PDF Parsing)                        │      │
│  │    ├─ Text extraction                        │      │
│  │    ├─ Page-by-page processing                │      │
│  │    └─ Pure Python (no external deps)         │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

## Request/Response Flow Examples

### Upload Request
```
Client                   Server
  │                        │
  ├─ POST /api/documents/upload
  │  Content-Type: multipart/form-data
  │  Body: file=@document.pdf
  │                        │
  │                        ├─ Validate file
  │                        ├─ Extract text
  │                        ├─ Chunk text
  │                        ├─ Create embeddings
  │                        ├─ Build FAISS index
  │                        ├─ Save to disk
  │                        └─ Save to DB
  │                        │
  │ ◄──────────────────────┤
  │  {
  │    "document_id": "abc123",
  │    "chunk_count": 15,
  │    "message": "Success"
  │  }
  │                        │
```

### Query Request
```
Client                   Server
  │                        │
  ├─ POST /api/documents/query
  │  Content-Type: application/json
  │  Body: {
  │    "document_id": "abc123",
  │    "question": "What is...?"
  │  }
  │                        │
  │                        ├─ Load vector store
  │                        ├─ Generate query embedding
  │                        ├─ Search FAISS
  │                        ├─ Get top 3 chunks
  │                        ├─ Call Groq LLM
  │                        └─ Format response
  │                        │
  │ ◄──────────────────────┤
  │  {
  │    "answer": "The main...",
  │    "sources": [...],
  │    "processing_time": 2.34
  │  }
  │                        │
```

---

**Legend:**
- `┌─┐` : System/Component boundary
- `│  │` : Contains/Includes
- `→ ▼` : Data flow direction
- `├─┤` : Connection/Relationship
