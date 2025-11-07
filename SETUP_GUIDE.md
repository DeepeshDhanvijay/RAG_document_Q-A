# Environment Setup Guide

## Getting Your Groq API Key

1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to `backend/.env`:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

## Supabase Setup (Optional)

The application works with or without Supabase. If the database is unavailable, the app will still function using local file storage for metadata.

If you want to use your own Supabase instance:

1. Create account at [https://supabase.com/](https://supabase.com/)
2. Create a new project
3. Go to Settings → API
4. Copy your project URL and anon key
5. Update `backend/.env`:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```

6. Create tables using the SQL editor:

```sql
-- Documents table
CREATE TABLE documents (
  id TEXT PRIMARY KEY,
  filename TEXT NOT NULL,
  chunk_count INTEGER NOT NULL,
  file_size INTEGER NOT NULL,
  upload_time TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Query history table (optional)
CREATE TABLE query_history (
  id SERIAL PRIMARY KEY,
  document_id TEXT NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  query_time TIMESTAMP NOT NULL DEFAULT NOW(),
  FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_documents_upload_time ON documents(upload_time DESC);
CREATE INDEX idx_query_history_document_id ON query_history(document_id);
CREATE INDEX idx_query_history_query_time ON query_history(query_time DESC);
```

## Python Virtual Environment

### Windows
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Mac/Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Node.js Setup

Make sure you have Node.js 18+ installed:
```bash
node --version  # Should show v18.x.x or higher
```

Install frontend dependencies:
```bash
cd frontend
npm install
```

## Troubleshooting Installation

### Python Issues

**Issue**: `pip` not found
```powershell
python -m pip install --upgrade pip
```

**Issue**: Permission errors on Windows
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue**: FAISS installation fails
```powershell
pip install faiss-cpu --no-cache-dir
```

### Node.js Issues

**Issue**: npm errors
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Tailwind not working
```bash
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
```

## Verifying Installation

### Backend
```powershell
cd backend
python -c "import fastapi, faiss, sentence_transformers, groq; print('All packages imported successfully!')"
```

### Frontend
```bash
cd frontend
npm run build  # Should complete without errors
```

## First Run Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Groq API key added to backend/.env
- [ ] Frontend dependencies installed
- [ ] Both servers start without errors
- [ ] Can access http://localhost:3000

## Performance Optimization

### For Faster Development

1. **Backend**: Use `uvicorn main:app --reload` for auto-reload
2. **Frontend**: Use `npm run dev` for hot module replacement
3. **FAISS**: The first embedding generation will download the model (~80MB), subsequent uses will be faster

### For Production

1. **Backend**: Use `gunicorn` with multiple workers
2. **Frontend**: Run `npm run build` and `npm start`
3. **Caching**: Enable Redis for query caching (optional)

## Common Environment Variables

### Backend (.env)
```env
# Required
GROQ_API_KEY=your_groq_api_key

# Optional (has defaults)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
MAX_FILE_SIZE=10485760  # 10MB in bytes
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=3
```

### Frontend (.env.local)
```env
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
```

## Directory Permissions

Ensure these directories are writable:
- `backend/uploads/` - Stores uploaded files
- `backend/vector_store/` - Stores FAISS indices
- `frontend/.next/` - Next.js build cache

Windows:
```powershell
# These directories are auto-created with proper permissions
```

Mac/Linux:
```bash
chmod 755 backend/uploads backend/vector_store
```
