"""
API Test Script for RAG Document Q&A Application
Run this script to test all API endpoints
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
SAMPLE_DOCS_DIR = Path("sample_documents")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy (status: {data.get('status')})")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is it running on port 8000?")
        return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_upload(file_path):
    """Test document upload"""
    print("\n" + "="*60)
    print("TEST 2: Document Upload")
    print("="*60)
    
    if not Path(file_path).exists():
        print_error(f"File not found: {file_path}")
        return None
    
    print_info(f"Uploading: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{BASE_URL}/api/documents/upload",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Upload successful!")
            print(f"  📄 Filename: {data['filename']}")
            print(f"  🆔 Document ID: {data['document_id']}")
            print(f"  📊 Chunks: {data['chunk_count']}")
            print(f"  ⏰ Upload time: {data['upload_time']}")
            return data['document_id']
        else:
            print_error(f"Upload failed: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print_error("Upload timeout - file may be too large or server is slow")
        return None
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return None

def test_list_documents():
    """Test listing documents"""
    print("\n" + "="*60)
    print("TEST 3: List Documents")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/documents", timeout=10)
        
        if response.status_code == 200:
            docs = response.json()
            print_success(f"Found {len(docs)} document(s)")
            
            for i, doc in enumerate(docs, 1):
                print(f"\n  Document {i}:")
                print(f"    Name: {doc['filename']}")
                print(f"    ID: {doc['id']}")
                print(f"    Chunks: {doc['chunk_count']}")
                print(f"    Size: {doc['file_size']} bytes")
                print(f"    Uploaded: {doc['upload_time']}")
            
            return docs
        else:
            print_error(f"List documents failed: {response.text}")
            return []
            
    except Exception as e:
        print_error(f"List documents error: {str(e)}")
        return []

def test_query(document_id, question):
    """Test querying a document"""
    print(f"\n{'─'*60}")
    print_info(f"Question: {question}")
    
    try:
        payload = {
            "document_id": document_id,
            "question": question
        }
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/documents/query",
            json=payload,
            timeout=30
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success("Query successful!")
            print(f"\n  💬 Answer:")
            print(f"  {data['answer']}\n")
            print(f"  ⏱️  Processing time: {data['processing_time']}s")
            print(f"  ⏱️  Total time: {elapsed_time:.2f}s")
            print(f"  📚 Sources used: {len(data['sources'])} chunk(s)")
            
            if data['sources']:
                print(f"\n  📖 Source References:")
                for i, source in enumerate(data['sources'], 1):
                    print(f"    {i}. Chunk {source['chunk_index']} (relevance: {source['relevance_score']:.2%})")
                    print(f"       Preview: {source['chunk_text'][:100]}...")
            
            return data
        else:
            print_error(f"Query failed: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print_error("Query timeout - may need to increase timeout or check Groq API")
        return None
    except Exception as e:
        print_error(f"Query error: {str(e)}")
        return None

def test_query_batch(document_id, questions):
    """Test multiple queries"""
    print("\n" + "="*60)
    print("TEST 4: Query Document")
    print("="*60)
    
    results = []
    for question in questions:
        result = test_query(document_id, question)
        if result:
            results.append(result)
        time.sleep(1)  # Rate limiting
    
    if results:
        print_success(f"\nCompleted {len(results)}/{len(questions)} queries successfully")
    
    return results

def test_history(document_id):
    """Test query history"""
    print("\n" + "="*60)
    print("TEST 5: Query History")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/documents/{document_id}/history",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            print_success(f"Found {len(history)} query/answer pair(s)")
            
            for i, item in enumerate(history, 1):
                print(f"\n  History {i}:")
                print(f"    Q: {item['question']}")
                print(f"    A: {item['answer'][:100]}...")
                print(f"    Time: {item['query_time']}")
            
            return history
        else:
            print_warning("Query history not available (may not be enabled)")
            return []
            
    except Exception as e:
        print_warning(f"Query history error: {str(e)}")
        return []

def test_delete(document_id):
    """Test deleting a document"""
    print("\n" + "="*60)
    print("TEST 6: Delete Document")
    print("="*60)
    
    print_warning(f"About to delete document: {document_id}")
    confirm = input("  Type 'yes' to confirm deletion: ")
    
    if confirm.lower() != 'yes':
        print_info("Deletion cancelled")
        return False
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/documents/{document_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Document deleted successfully")
            return True
        else:
            print_error(f"Delete failed: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Delete error: {str(e)}")
        return False

def run_full_test_suite():
    """Run complete test suite"""
    print("\n" + "🧪 " + "="*58 + " 🧪")
    print("       RAG DOCUMENT Q&A - API TEST SUITE")
    print("🧪 " + "="*58 + " 🧪\n")
    
    # Test 1: Health
    if not test_health():
        print_error("\n❌ Tests aborted - backend is not available")
        return
    
    # Test 2: Upload
    sample_file = SAMPLE_DOCS_DIR / "ai_business_impact.txt"
    if not sample_file.exists():
        print_error(f"\n❌ Sample file not found: {sample_file}")
        print_info("Please ensure sample_documents/ai_business_impact.txt exists")
        return
    
    doc_id = test_upload(str(sample_file))
    if not doc_id:
        print_error("\n❌ Tests aborted - couldn't upload document")
        return
    
    # Test 3: List
    docs = test_list_documents()
    
    # Test 4: Query
    questions = [
        "What is the main conclusion of this document?",
        "What percentage increase in efficiency was reported?",
        "What are the three key recommendations?",
        "What challenges do businesses face with AI adoption?",
    ]
    
    test_query_batch(doc_id, questions)
    
    # Test 5: History
    test_history(doc_id)
    
    # Test 6: Delete (optional)
    test_delete(doc_id)
    
    # Final summary
    print("\n" + "🎉 " + "="*58 + " 🎉")
    print("       TEST SUITE COMPLETED")
    print("🎉 " + "="*58 + " 🎉\n")
    print_success("All tests executed!")
    print_info("Check the results above for any errors")

if __name__ == "__main__":
    try:
        run_full_test_suite()
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
