@echo off
echo Starting Semantic Search Application...

REM Activate virtual environment
call venv\Scripts\activate

REM Start backend server
start cmd /k "cd search_api && python app.py"

REM Start frontend development server
start cmd /k "cd frontend && npm start"

echo Application started successfully!
echo Backend running at http://localhost:5000
echo Frontend running at http://localhost:3000 