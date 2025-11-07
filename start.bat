@echo off
echo Starting RAG Document Q&A Application...

echo.
echo Starting Backend Server...
start cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak > nul

echo.
echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Application is starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Close the terminal windows to stop the servers.
