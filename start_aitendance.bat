@echo off

cd /d %~dp0

echo Starting AiTendance Backend...
start cmd /k "cd backend && call venv\Scripts\activate && python -m uvicorn app.main:app --reload"

timeout /t 5 > nul

echo Starting AiTendance Frontend...
start cmd /k "cd frontend && npm run dev"

timeout /t 8 > nul

start http://localhost:3000

exit