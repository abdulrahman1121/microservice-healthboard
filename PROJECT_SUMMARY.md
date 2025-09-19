# Microservice Healthboard - Project Summary

## 🎯 What We Built

A complete **Kubernetes-style microservice health monitoring dashboard** with fault injection capabilities, simulating a real production monitoring system.

## 🏗️ Architecture Overview

### Backend (FastAPI)
- **Pod Registry**: In-memory simulation of Kubernetes pods
- **Health Monitoring**: Real-time heartbeat and status tracking
- **Fault Injection**: API endpoints for injecting delays, errors, and pod kills
- **SLO Tracking**: Service Level Objective monitoring with burn rate calculation
- **Prometheus Metrics**: Standard metrics endpoint for monitoring tools

### Frontend (React)
- **Service Cards**: Visual representation of each microservice
- **Fault Controls**: Interactive buttons for fault injection
- **Real-time Charts**: Live latency, error rate, and health monitoring
- **SLO Dashboard**: Burn rate visualization and error budget tracking

## 🚀 Key Features Implemented

### ✅ Core Monitoring
- [x] 3 mock services (sensor-sim, planner-sim, ui-proxy)
- [x] Real-time health status (Healthy/Degraded/Down)
- [x] Latency tracking with artificial delays
- [x] Error rate monitoring (0-100%)
- [x] Pod restart counter

### ✅ Fault Injection
- [x] Delay injection (0-5000ms)
- [x] Error rate injection (0-100%)
- [x] Pod kill simulation
- [x] Pod restart functionality

### ✅ SLO & Reliability
- [x] Latency P95 target (200ms)
- [x] Availability target (99.5%)
- [x] Error budget tracking
- [x] Burn rate calculation (5-minute window)
- [x] Visual burn rate indicators

### ✅ Observability
- [x] Prometheus-style metrics endpoint
- [x] Real-time charts (last 5 minutes)
- [x] Service-level aggregation
- [x] Health percentage tracking

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pods` | GET | List all pods with status |
| `/fault/{pod_id}` | POST | Inject faults (delay, error, kill) |
| `/restart/{pod_id}` | POST | Restart pod and clear faults |
| `/metrics` | GET | Prometheus-style metrics |
| `/slo` | GET | SLO status and burn rate |
| `/health` | GET | Health check |

## 🎮 Demo Scenarios

### 1. **Normal Operation**
- All services healthy
- Low latency and error rates
- Normal burn rate

### 2. **Latency Injection**
- Add delays to simulate network issues
- Watch latency charts spike
- Observe service degradation

### 3. **Error Rate Storm**
- Inject high error rates
- Monitor burn rate increase
- Track error budget consumption

### 4. **Pod Failures**
- Kill pods to simulate crashes
- Watch cascade effects
- Test recovery procedures

### 5. **Chaos Engineering**
- Mixed fault scenarios
- System resilience testing
- Recovery time measurement

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Threading**: Background health monitoring
- **JSON**: API communication

### Frontend
- **React**: Component-based UI framework
- **Recharts**: Real-time data visualization
- **Axios**: HTTP client for API calls
- **CSS Grid/Flexbox**: Responsive layout

## 📁 Project Structure

```
microservice-healthboard/
├── backend/                 # FastAPI application
│   ├── app.py              # Main application with all endpoints
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ServiceCard.js    # Service monitoring cards
│   │   │   ├── SLODashboard.js   # SLO metrics display
│   │   │   └── Charts.js         # Real-time charts
│   │   ├── App.js          # Main application
│   │   └── index.js        # Entry point
│   └── package.json        # Node.js dependencies
├── demo-scripts/           # Demo and testing scripts
│   ├── demo-faults.sh      # Basic fault injection demo
│   ├── chaos-test.sh       # Chaos engineering scenarios
│   ├── demo-api.py         # Python API demo
│   └── start-services.sh   # Service startup script
├── README.md               # Complete documentation
├── start.bat              # Windows startup script
└── test-setup.py          # Setup verification script
```

## 🎯 Learning Outcomes

This project demonstrates:

1. **Microservice Monitoring**: How to build observability for distributed systems
2. **Fault Injection**: Chaos engineering and resilience testing
3. **SLO Implementation**: Service Level Objective tracking and alerting
4. **Real-time Dashboards**: Live monitoring with WebSocket-like updates
5. **API Design**: RESTful APIs for system management
6. **Frontend-Backend Integration**: Modern web application architecture

## 🚀 Getting Started

### Quick Start
```bash
# Start everything
./demo-scripts/start-services.sh

# Or on Windows
start.bat

# Test the setup
python test-setup.py

# Run demos
python demo-scripts/demo-api.py
```

### Manual Start
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 🌐 Access Points

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **Metrics**: http://localhost:8000/metrics
- **API Docs**: http://localhost:8000/docs

## 🎉 Success Criteria Met

✅ **"Debug live system, identify root causes, fix"** → Fault injection, cascade monitoring, recovery procedures

✅ **"Build metrics & monitor performance + reliability"** → SLI/SLO tiles, burn rate tracking, error budgets

✅ **"k8s nice-to-have"** → Pod terminology, restart simulation, service monitoring

This project successfully simulates a production-grade microservice monitoring system with all the essential features for understanding system reliability and observability!
