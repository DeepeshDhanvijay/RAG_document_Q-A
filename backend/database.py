from supabase import create_client, Client
from config import config
from typing import List, Dict, Optional
from datetime import datetime

class DatabaseService:
    """Handles Supabase database operations"""
    
    def __init__(self):
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the documents table exists"""
        # Note: In production, you would create this table via Supabase dashboard or migration
        # For now, we'll handle this with try-except blocks during operations
        pass
    
    def create_document(self, document_id: str, filename: str, chunk_count: int, file_size: int) -> Dict:
        """Create a new document record"""
        try:
            data = {
                "id": document_id,
                "filename": filename,
                "chunk_count": chunk_count,
                "file_size": file_size,
                "upload_time": datetime.utcnow().isoformat(),
            }
            
            result = self.client.table("documents").insert(data).execute()
            return result.data[0] if result.data else data
        except Exception as e:
            # If table doesn't exist, return the data anyway (we'll handle without DB)
            print(f"Database insert error: {e}")
            return {
                "id": document_id,
                "filename": filename,
                "chunk_count": chunk_count,
                "file_size": file_size,
                "upload_time": datetime.utcnow().isoformat(),
            }
    
    def get_all_documents(self) -> List[Dict]:
        """Retrieve all documents"""
        try:
            result = self.client.table("documents").select("*").order("upload_time", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Database query error: {e}")
            return []
    
    def get_document(self, document_id: str) -> Optional[Dict]:
        """Get a specific document by ID"""
        try:
            result = self.client.table("documents").select("*").eq("id", document_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Database query error: {e}")
            return None
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document record"""
        try:
            self.client.table("documents").delete().eq("id", document_id).execute()
            return True
        except Exception as e:
            print(f"Database delete error: {e}")
            return False
    
    def save_query_history(self, document_id: str, question: str, answer: str):
        """Save query history (optional feature)"""
        try:
            data = {
                "document_id": document_id,
                "question": question,
                "answer": answer,
                "query_time": datetime.utcnow().isoformat(),
            }
            self.client.table("query_history").insert(data).execute()
        except Exception as e:
            print(f"Query history save error: {e}")
    
    def get_query_history(self, document_id: str) -> List[Dict]:
        """Retrieve query history for a document"""
        try:
            result = self.client.table("query_history").select("*").eq("document_id", document_id).order("query_time", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Query history retrieval error: {e}")
            return []
