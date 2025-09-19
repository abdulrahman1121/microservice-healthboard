# Microservice Healthboard with Fault Injection

A Kubernetes-style health dashboard that monitors mock microservices with fault injection capabilities. This project simulates a microservice environment with SLO tracking, burn rate monitoring, and real-time fault injection for testing and demonstration purposes.

## 🎯 Features

- **Real-time Monitoring**: Track 3 mock services (sensor-sim, planner-sim, ui-proxy)
- **Fault Injection**: Inject delays, errors, and kill pods to simulate failures
- **SLO Tracking**: Monitor latency P95, availability targets, and error budgets
- **Burn Rate Monitoring**: Track error budget consumption with visual indicators
- **Prometheus Metrics**: Expose `/metrics` endpoint in Prometheus format
- **Interactive Dashboard**: React-based UI with real-time charts and controls


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

