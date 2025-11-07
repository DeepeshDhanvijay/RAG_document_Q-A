# Quick Start Guide

## 5-Minute Setup

### Step 1: Get Groq API Key
1. Visit: https://console.groq.com/
2. Sign up (free)
3. Create API key
4. Copy the key

### Step 2: Add API Key
Open `backend\.env` and add your key:
```
GROQ_API_KEY=your_actual_key_here
```

### Step 3: Install Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 4: Install Frontend
```powershell
cd ..\frontend
npm install
```

### Step 5: Start Application

**Option A: Automatic (Windows)**
```powershell
.\start.bat
```

**Option B: Manual**

Terminal 1 (Backend):
```powershell
cd backend
python main.py
```

Terminal 2 (Frontend):
```powershell
cd frontend
npm run dev
```

### Step 6: Open Browser
```
http://localhost:3000
```

---

## Common Commands

### Backend
```powershell
# Activate virtual environment
cd backend
.\venv\Scripts\Activate.ps1

# Run server
python main.py

# Run tests
cd ..
python test_api.py

# Check API docs
# Visit: http://localhost:8000/docs
```

### Frontend
```powershell
# Development mode
cd frontend
npm run dev

# Production build
npm run build
npm start

# Lint
npm run lint
```

---

## First Time Use

### 1. Upload a Document
- Click or drag-and-drop a PDF/TXT file
- Wait for processing (~10-30 seconds)
- Document appears in list

### 2. Ask a Question
- Click on a document to select it
- Type your question
- Click "Get Answer"
- View answer and sources

### 3. Try Sample Documents
Use the provided samples:
- `sample_documents/ai_business_impact.txt`
- `sample_documents/climate_change.txt`

### 4. Example Questions

**For AI Business Impact:**
- "What is the main conclusion?"
- "What percentage increase in efficiency?"
- "What are the three key recommendations?"

**For Climate Change:**
- "How much have temperatures risen?"
- "What are the main causes?"
- "What is the economic impact?"

---

## Troubleshooting

### Backend Won't Start

**Error: No module named 'X'**
```powershell
cd backend
pip install -r requirements.txt
```

**Error: Groq API authentication failed**
- Check your API key in `backend\.env`
- Make sure there are no extra spaces

### Frontend Won't Start

**Error: Cannot find module**
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

**Error: Port 3000 already in use**
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Can't Upload Documents

**Check:**
- File is PDF or TXT format
- File size < 10MB
- Backend is running
- No firewall blocking localhost:8000

### Queries Not Working

**Check:**
- Document is selected (highlighted in blue)
- Backend is running
- Groq API key is valid
- Internet connection is active

---

## File Locations

```
rag_document_qa/
├── README.md              <- Main documentation
├── SETUP_GUIDE.md         <- Detailed setup
├── API_TESTING.md         <- API examples
├── PROJECT_SUMMARY.md     <- Project overview
├── test_api.py            ← Test script
│
├── backend/
│   ├── .env               <- Add your API key here!
│   ├── main.py            <- Backend entry point
│   └── requirements.txt   <- Python packages
│
└── frontend/
    ├── .env.local         <- Frontend config
    └── package.json       <- Node packages
```

---

## Environment Variables

### Required
```env
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

### Optional (Already Configured)
```env
# backend/.env
SUPABASE_URL=https://ihhwuoxotjynfiskvetx.supabase.co
SUPABASE_KEY=eyJhbGci...

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Testing

### Manual Test
1. Start both servers
2. Open http://localhost:3000
3. Upload `sample_documents/ai_business_impact.txt`
4. Ask: "What is the main conclusion?"
5. Should get detailed answer with sources

### Automated Test
```powershell
python test_api.py
```

---

## Performance Expectations

- **Upload** (10-page PDF): 10-30 seconds
- **Query**: 2-5 seconds
- **List documents**: < 1 second

---

## Tech Stack Summary

**Backend:** Python + FastAPI + FAISS + Groq
**Frontend:** TypeScript + Next.js + Tailwind CSS
**Database:** Supabase (PostgreSQL)
**Embeddings:** Sentence Transformers
**LLM:** Groq (Llama 3-8B)

---

## Tips & Tricks

1. **Start with small files** - Use TXT files for faster testing
2. **Sample docs included** - Use provided samples to test
3. **Check API docs** - Visit http://localhost:8000/docs
4. **Use test script** - Run `python test_api.py` to verify setup
5. **View sources** - Click "Source References" to see how answer was generated

---

## Need Help?

1. **Setup issues** - Check SETUP_GUIDE.md
2. **API questions** - Check API_TESTING.md
3. **General info** - Check README.md
4. **Project details** - Check PROJECT_SUMMARY.md

---

## Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Got Groq API key from console.groq.com
- [ ] Added API key to backend/.env
- [ ] Installed backend dependencies (pip install -r requirements.txt)
- [ ] Installed frontend dependencies (npm install)
- [ ] Backend starts without errors (python main.py)
- [ ] Frontend starts without errors (npm run dev)
- [ ] Can access http://localhost:3000
- [ ] Successfully uploaded a test document
- [ ] Successfully got an answer to a question

**All checked? You're ready to go!**

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Start backend | `cd backend; python main.py` |
| Start frontend | `cd frontend; npm run dev` |
| Run tests | `python test_api.py` |
| View API docs | Open `http://localhost:8000/docs` |
| View app | Open `http://localhost:3000` |
| Install backend | `cd backend; pip install -r requirements.txt` |
| Install frontend | `cd frontend; npm install` |

---

**Happy coding!**
