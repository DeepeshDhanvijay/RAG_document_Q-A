import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ihhwuoxotjynfiskvetx.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImloaHd1b3hvdGp5bmZpc2t2ZXR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MzA3NjQsImV4cCI6MjA3ODAwNjc2NH0.93JLxYNpr3qp-Fbnqojbg5GkZL6k1KYeQlZTlzKOMwU")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".pdf", ".txt"}
    UPLOAD_DIR = "uploads"
    VECTOR_STORE_DIR = "vector_store"
    
    # RAG settings
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 3
    
    # Model settings
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "llama-3.1-8b-instant"

config = Config()
