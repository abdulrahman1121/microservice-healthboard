#!/bin/bash

# Start script for the Microservice Healthboard
# This script starts both backend and frontend services

echo "🚀 Starting Microservice Healthboard"
echo "===================================="
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "   Attempt $attempt/$max_attempts - waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to start within expected time"
    return 1
}

# Check if ports are already in use
if check_port 8000; then
    echo "⚠️  Port 8000 is already in use. Backend might already be running."
fi

if check_port 3000; then
    echo "⚠️  Port 3000 is already in use. Frontend might already be running."
fi

echo ""
echo "🔧 Starting Backend (FastAPI)..."
echo "================================"

# Start backend
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start backend in background
echo "🚀 Starting FastAPI server..."
python app.py &
BACKEND_PID=$!

# Wait for backend to be ready
if wait_for_service "http://localhost:8000/health" "Backend"; then
    echo "✅ Backend started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Failed to start backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎨 Starting Frontend (React)..."
echo "==============================="

# Start frontend
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start frontend in background
echo "🚀 Starting React development server..."
npm start &
FRONTEND_PID=$!

# Wait for frontend to be ready
if wait_for_service "http://localhost:3000" "Frontend"; then
    echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start frontend"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Microservice Healthboard is now running!"
echo "==========================================="
echo ""
echo "📊 Frontend Dashboard: http://localhost:3000"
echo "🔧 Backend API:        http://localhost:8000"
echo "📈 Metrics Endpoint:   http://localhost:8000/metrics"
echo "📋 API Docs:           http://localhost:8000/docs"
echo ""
echo "🛑 To stop the services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "🧪 Try the demo scripts:"
echo "   ./demo-scripts/demo-faults.sh"
echo "   ./demo-scripts/chaos-test.sh"
echo ""

# Keep script running and show logs
echo "📝 Service logs (Ctrl+C to stop all services):"
echo "=============================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
