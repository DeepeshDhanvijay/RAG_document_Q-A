# API Testing Guide

This guide provides detailed examples for testing the RAG Document Q&A API endpoints.

## Prerequisites

- Backend server running at `http://localhost:8000`
- A test document file (PDF or TXT)

## Testing Tools

You can use any of these tools:
- **cURL** (command line)
- **Postman** (GUI)
- **Thunder Client** (VS Code extension)
- **Python requests** (script)

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/documents/upload` | Upload a document |
| GET | `/api/documents` | List all documents |
| POST | `/api/documents/query` | Ask a question |
| DELETE | `/api/documents/{id}` | Delete a document |
| GET | `/api/documents/{id}/history` | Get query history |

---

## 1. Health Check

### cURL
```bash
curl http://localhost:8000/health
```

### Expected Response
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123
}
```

---

## 2. Upload Document

### cURL (Windows PowerShell)
```powershell
curl -X POST http://localhost:8000/api/documents/upload `
  -F "file=@sample_documents\ai_business_impact.txt"
```

### cURL (Mac/Linux)
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@sample_documents/ai_business_impact.txt"
```

### Postman
1. Method: POST
2. URL: `http://localhost:8000/api/documents/upload`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select your file
6. Send

### Expected Response
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "ai_business_impact.txt",
  "upload_time": "2024-01-15 10:30:00",
  "chunk_count": 12,
  "message": "Document uploaded and processed successfully"
}
```

### Error Responses

**Invalid file type**
```json
{
  "error": "File type .docx not supported. Allowed types: .pdf, .txt"
}
```

**File too large**
```json
{
  "error": "File size exceeds maximum allowed size of 10.0MB"
}
```

**Empty file**
```json
{
  "error": "File is empty"
}
```

---

## 3. List Documents

### cURL
```bash
curl http://localhost:8000/api/documents
```

### Expected Response
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "ai_business_impact.txt",
    "upload_time": "2024-01-15 10:30:00",
    "chunk_count": 12,
    "file_size": 5242880
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "filename": "climate_change.txt",
    "upload_time": "2024-01-15 11:00:00",
    "chunk_count": 8,
    "file_size": 3145728
  }
]
```

---

## 4. Query Document

### cURL (Windows PowerShell)
```powershell
curl -X POST http://localhost:8000/api/documents/query `
  -H "Content-Type: application/json" `
  -d '{\"document_id\": \"550e8400-e29b-41d4-a716-446655440000\", \"question\": \"What is the main conclusion?\"}'
```

### cURL (Mac/Linux)
```bash
curl -X POST http://localhost:8000/api/documents/query \
  -H "Content-Type: application/json" \
  -d '{"document_id": "550e8400-e29b-41d4-a716-446655440000", "question": "What is the main conclusion?"}'
```

### Postman
1. Method: POST
2. URL: `http://localhost:8000/api/documents/query`
3. Headers: `Content-Type: application/json`
4. Body → raw → JSON:
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What is the main conclusion?"
}
```

### Expected Response
```json
{
  "question": "What is the main conclusion?",
  "answer": "The main conclusion is that artificial intelligence represents a transformational opportunity for businesses willing to invest in the technology and manage the associated challenges. While initial costs and implementation hurdles exist, the long-term benefits in efficiency, decision-making, and customer satisfaction far outweigh these obstacles.",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_name": "ai_business_impact.txt",
  "sources": [
    {
      "chunk_text": "The main conclusion is that artificial intelligence represents a transformational opportunity for businesses willing to invest in the technology and manage the associated challenges...",
      "relevance_score": 0.9234,
      "chunk_index": 10
    },
    {
      "chunk_text": "Companies that successfully integrate AI into their operations will gain significant competitive advantages in the coming years...",
      "relevance_score": 0.8567,
      "chunk_index": 11
    },
    {
      "chunk_text": "AI-powered automation has led to a 35% increase in operational efficiency across surveyed companies...",
      "relevance_score": 0.7823,
      "chunk_index": 3
    }
  ],
  "processing_time": 2.34
}
```

### Test Questions for Sample Documents

#### For `ai_business_impact.txt`:
```json
{"document_id": "your-doc-id", "question": "What percentage increase in efficiency was reported?"}
{"document_id": "your-doc-id", "question": "What are the three key recommendations?"}
{"document_id": "your-doc-id", "question": "What is the average cost reduction?"}
{"document_id": "your-doc-id", "question": "Why did the authors choose this methodology?"}
```

#### For `climate_change.txt`:
```json
{"document_id": "your-doc-id", "question": "How much have global temperatures risen?"}
{"document_id": "your-doc-id", "question": "What are the main causes of climate change?"}
{"document_id": "your-doc-id", "question": "How does approach A differ from approach B?"}
{"document_id": "your-doc-id", "question": "What percentage increase in droughts was mentioned?"}
```

### Error Responses

**Document not found**
```json
{
  "error": "Document not found"
}
```

**Empty question**
```json
{
  "error": "Question cannot be empty"
}
```

**No relevant information**
```json
{
  "error": "No relevant information found in document"
}
```

---

## 5. Delete Document

### cURL
```bash
curl -X DELETE http://localhost:8000/api/documents/550e8400-e29b-41d4-a716-446655440000
```

### Expected Response
```json
{
  "message": "Document deleted successfully",
  "document_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 6. Get Query History (Bonus Feature)

### cURL
```bash
curl http://localhost:8000/api/documents/550e8400-e29b-41d4-a716-446655440000/history
```

### Expected Response
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "history": [
    {
      "question": "What is the main conclusion?",
      "answer": "The main conclusion is that artificial intelligence...",
      "query_time": "2024-01-15 10:35:00"
    },
    {
      "question": "What are the key recommendations?",
      "answer": "The three key recommendations are: 1. Start Small...",
      "query_time": "2024-01-15 10:32:00"
    }
  ]
}
```

---

## Python Test Script

Save this as `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())
    return response.status_code == 200

def test_upload(file_path):
    """Test document upload"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/documents/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Upload successful!")
        print(f"Document ID: {data['document_id']}")
        print(f"Chunks: {data['chunk_count']}")
        return data['document_id']
    else:
        print(f"\n❌ Upload failed: {response.text}")
        return None

def test_list_documents():
    """Test listing documents"""
    response = requests.get(f"{BASE_URL}/api/documents")
    docs = response.json()
    print(f"\n📄 Found {len(docs)} documents")
    for doc in docs:
        print(f"  - {doc['filename']} ({doc['chunk_count']} chunks)")
    return docs

def test_query(document_id, question):
    """Test querying a document"""
    payload = {
        "document_id": document_id,
        "question": question
    }
    response = requests.post(f"{BASE_URL}/api/documents/query", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n❓ Question: {question}")
        print(f"✅ Answer: {data['answer'][:200]}...")
        print(f"📊 Processing time: {data['processing_time']}s")
        print(f"📚 Sources: {len(data['sources'])} chunks")
        return data
    else:
        print(f"\n❌ Query failed: {response.text}")
        return None

def test_delete(document_id):
    """Test deleting a document"""
    response = requests.delete(f"{BASE_URL}/api/documents/{document_id}")
    if response.status_code == 200:
        print(f"\n🗑️  Document deleted successfully")
        return True
    else:
        print(f"\n❌ Delete failed: {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 Starting API Tests\n")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n[Test 1] Health Check")
    test_health()
    
    # Test 2: Upload document
    print("\n[Test 2] Upload Document")
    doc_id = test_upload("sample_documents/ai_business_impact.txt")
    
    if not doc_id:
        print("❌ Tests failed - couldn't upload document")
        exit(1)
    
    # Test 3: List documents
    print("\n[Test 3] List Documents")
    test_list_documents()
    
    # Test 4: Query document
    print("\n[Test 4] Query Document")
    questions = [
        "What is the main conclusion?",
        "What percentage increase in efficiency was reported?",
        "What are the three key recommendations?"
    ]
    
    for question in questions:
        test_query(doc_id, question)
    
    # Test 5: Delete document
    print("\n[Test 5] Delete Document")
    # Uncomment to actually delete:
    # test_delete(doc_id)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
```

Run with:
```bash
python test_api.py
```

---

## Performance Testing

### Expected Response Times

- **Upload** (10-page PDF): 10-30 seconds
- **List documents**: < 1 second
- **Query**: 2-5 seconds
- **Delete**: < 1 second

### Load Testing with Apache Bench

```bash
# Test list endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/api/documents

# Test query endpoint
ab -n 50 -c 5 -p query.json -T application/json http://localhost:8000/api/documents/query
```

---

## Common Issues

### 1. Connection Refused
**Problem**: Can't connect to backend
**Solution**: Make sure backend is running on port 8000

### 2. CORS Errors
**Problem**: Frontend can't access API
**Solution**: Backend has CORS configured for localhost:3000

### 3. Slow Query Responses
**Problem**: Queries taking > 10 seconds
**Solution**: 
- Check Groq API status
- Verify internet connection
- Reduce TOP_K_RESULTS in config

### 4. Out of Memory
**Problem**: FAISS fails on large documents
**Solution**: 
- Increase chunk size
- Process in batches
- Use faiss-cpu instead of faiss-gpu

---

## API Rate Limits

### Groq Free Tier
- 30 requests per minute
- 14,400 requests per day

If you hit rate limits, you'll see:
```json
{
  "error": "Rate limit exceeded. Please try again later."
}
```

---

## Best Practices

1. **Always check document_id** before querying
2. **Cache frequent queries** to save API calls
3. **Delete old documents** to save storage
4. **Use appropriate chunk sizes** for your content
5. **Test with small documents** first

---

## Debugging Tips

### Enable Detailed Logging

Add to `backend/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check API Docs
Visit `http://localhost:8000/docs` for interactive Swagger documentation

### Monitor API Health
```bash
# Continuous health check (every 5 seconds)
while true; do curl http://localhost:8000/health; sleep 5; done
```
