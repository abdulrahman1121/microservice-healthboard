# Microservice Healthboard with Fault Injection

A Kubernetes-style health dashboard that monitors mock microservices with fault injection capabilities. This project simulates a microservice environment with SLO tracking, burn rate monitoring, and real-time fault injection for testing and demonstration purposes.

## 🎯 Features

- **Real-time Monitoring**: Track 3 mock services (sensor-sim, planner-sim, ui-proxy)
- **Fault Injection**: Inject delays, errors, and kill pods to simulate failures
- **SLO Tracking**: Monitor latency P95, availability targets, and error budgets
- **Burn Rate Monitoring**: Track error budget consumption with visual indicators
- **Prometheus Metrics**: Expose `/metrics` endpoint in Prometheus format
- **Interactive Dashboard**: React-based UI with real-time charts and controls

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python app.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`


# Kill a pod
curl -X POST "http://localhost:8000/fault/ui-proxy-pod-1" \
  -H "Content-Type: application/json" \
  -d '{"kill": true}'

# Restart a pod
curl -X POST "http://localhost:8000/restart/sensor-sim-pod-1"
```


## 🎮 Demo Scenarios

### Scenario 1: Normal Operation
1. Start both backend and frontend
2. Observe all services showing "Healthy" status
3. Check SLO dashboard shows normal burn rate

### Scenario 2: Latency Injection
1. Use the fault injection controls to add 1000ms delay to sensor-sim
2. Watch the latency chart spike
3. Observe service status change to "Degraded"

### Scenario 3: Error Rate Injection
1. Set error rate to 0.4 (40%) for planner-sim
2. Watch error rate chart increase
3. Check burn rate increase in SLO dashboard

### Scenario 4: Pod Failure
1. Kill a pod using the fault injection
2. Observe status change to "Down"
3. Use restart button to recover the pod

### Scenario 5: Cascade Failure
1. Kill multiple pods across different services
2. Watch overall system health degrade
3. Monitor burn rate increase
4. Restart pods to simulate recovery

## 📈 SLO Configuration

The system tracks the following SLOs:
- **Latency P95**: Target < 200ms
- **Availability**: Target 99.5%
- **Error Budget**: Tracks remaining budget
- **Burn Rate**: 5-minute error budget consumption rate

Burn rate indicators:
- 🟢 Normal: < 1.0x
- 🟡 Medium: 1.0x - 2.0x
- 🔴 High: > 2.0x

## 🎯 Learning Objectives

This project demonstrates:
- Microservice monitoring patterns
- Fault injection for chaos engineering
- SLO/SLI implementation
- Real-time dashboard development
- Kubernetes-style resource management
- Error budget tracking
- Burn rate monitoring

Perfect for understanding how to build observability tools and implement reliability engineering practices!

