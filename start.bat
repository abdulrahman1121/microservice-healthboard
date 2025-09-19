@echo off
echo 🚀 Starting Microservice Healthboard
echo ====================================
echo.

echo 🔧 Starting Backend (FastAPI)...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt > nul 2>&1

REM Start backend in background
echo 🚀 Starting FastAPI server...
start "Backend" cmd /k "python app.py"

REM Wait a moment for backend to start
timeout /t 5 /nobreak > nul

echo.
echo 🎨 Starting Frontend (React)...
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
)

REM Start frontend
echo 🚀 Starting React development server...
start "Frontend" cmd /k "npm start"

echo.
echo 🎉 Microservice Healthboard is starting!
echo ========================================
echo.
echo 📊 Frontend Dashboard: http://localhost:3000
echo 🔧 Backend API:        http://localhost:8000
echo 📈 Metrics Endpoint:   http://localhost:8000/metrics
echo 📋 API Docs:           http://localhost:8000/docs
echo.
echo 🧪 Try the demo scripts:
echo    python demo-scripts\demo-api.py
echo.
echo Press any key to exit...
pause > nul
