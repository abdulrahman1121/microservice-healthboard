from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import time
import asyncio
import random
from datetime import datetime, timedelta
import threading
from collections import defaultdict, deque

app = FastAPI(title="Microservice Healthboard", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Types
class Pod(BaseModel):
    id: str
    service: str  # "sensor-sim" | "planner-sim" | "ui-proxy"
    status: str   # "Healthy" | "Degraded" | "Down"
    last_heartbeat: float
    restarts: int
    latency_ms: float
    error_rate: float  # 0..1
    delay_ms: int = 0
    killed: bool = False

class FaultRequest(BaseModel):
    delay_ms: Optional[int] = None
    error_rate: Optional[float] = None
    kill: Optional[bool] = None

class SLOStatus(BaseModel):
    latency_p95_target_ms: int
    availability_target: float
    burn_rate_5m: float
    budget_remaining: float

# Global state
pods: Dict[str, Pod] = {}
metrics_history = defaultdict(lambda: deque(maxlen=300))  # 5 minutes at 1s intervals
slo_data = {
    "latency_p95_target_ms": 200,
    "availability_target": 0.995,
    "error_budget": 1.0,
    "burn_rate_5m": 0.0,
    "budget_remaining": 1.0
}

# Initialize mock pods
def initialize_pods():
    services = ["sensor-sim", "planner-sim", "ui-proxy"]
    for i, service in enumerate(services):
        pod_id = f"{service}-pod-{i+1}"
        pods[pod_id] = Pod(
            id=pod_id,
            service=service,
            status="Healthy",
            last_heartbeat=time.time(),
            restarts=0,
            latency_ms=random.uniform(50, 150),
            error_rate=0.0
        )

# Health monitoring loop
def update_pod_health():
    current_time = time.time()
    for pod_id, pod in pods.items():
        # Update heartbeat if not killed
        if not pod.killed:
            pod.last_heartbeat = current_time
        
        # Calculate artificial latency
        base_latency = random.uniform(50, 150)
        pod.latency_ms = base_latency + pod.delay_ms
        
        # Determine status
        time_since_heartbeat = current_time - pod.last_heartbeat
        
        if pod.killed or time_since_heartbeat > 5.0:
            pod.status = "Down"
        elif pod.error_rate > 0.2:
            pod.status = "Degraded"
        else:
            pod.status = "Healthy"
        
        # Record metrics
        metrics_history[f"{pod.service}_latency"].append(pod.latency_ms)
        metrics_history[f"{pod.service}_error_rate"].append(pod.error_rate)
        metrics_history[f"{pod.service}_healthy"].append(1 if pod.status == "Healthy" else 0)

# Background health monitoring
def health_monitor():
    while True:
        update_pod_health()
        time.sleep(1)

# Start health monitoring in background
health_thread = threading.Thread(target=health_monitor, daemon=True)
health_thread.start()

# Initialize pods on startup
initialize_pods()

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Microservice Healthboard API", "version": "1.0.0"}

@app.get("/pods")
async def get_pods():
    """Get all pods with their current status"""
    return {
        "pods": [pod.dict() for pod in pods.values()],
        "timestamp": time.time()
    }

@app.post("/fault/{pod_id}")
async def inject_fault(pod_id: str, fault: FaultRequest):
    """Inject faults into a specific pod"""
    if pod_id not in pods:
        raise HTTPException(status_code=404, detail="Pod not found")
    
    pod = pods[pod_id]
    
    if fault.delay_ms is not None:
        pod.delay_ms = max(0, fault.delay_ms)
    
    if fault.error_rate is not None:
        pod.error_rate = max(0.0, min(1.0, fault.error_rate))
    
    if fault.kill is not None:
        pod.killed = fault.kill
        if fault.kill:
            pod.status = "Down"
    
    return {"message": f"Fault injected into {pod_id}", "pod": pod.dict()}

@app.post("/restart/{pod_id}")
async def restart_pod(pod_id: str):
    """Restart a pod (clear faults and increment restart counter)"""
    if pod_id not in pods:
        raise HTTPException(status_code=404, detail="Pod not found")
    
    pod = pods[pod_id]
    pod.restarts += 1
    pod.delay_ms = 0
    pod.error_rate = 0.0
    pod.killed = False
    pod.status = "Healthy"
    pod.last_heartbeat = time.time()
    
    return {"message": f"Pod {pod_id} restarted", "pod": pod.dict()}

@app.get("/metrics")
async def get_metrics():
    """Prometheus-style metrics endpoint"""
    current_time = time.time()
    metrics = []
    
    # Pod health metrics
    for pod_id, pod in pods.items():
        metrics.append(f'pod_healthy{{pod_id="{pod_id}",service="{pod.service}"}} {1 if pod.status == "Healthy" else 0}')
        metrics.append(f'pod_restarts{{pod_id="{pod_id}",service="{pod.service}"}} {pod.restarts}')
        metrics.append(f'pod_latency_ms{{pod_id="{pod_id}",service="{pod.service}"}} {pod.latency_ms}')
        metrics.append(f'pod_error_rate{{pod_id="{pod_id}",service="{pod.service}"}} {pod.error_rate}')
    
    # Service-level metrics
    for service in ["sensor-sim", "planner-sim", "ui-proxy"]:
        service_pods = [p for p in pods.values() if p.service == service]
        if service_pods:
            avg_latency = sum(p.latency_ms for p in service_pods) / len(service_pods)
            avg_error_rate = sum(p.error_rate for p in service_pods) / len(service_pods)
            healthy_count = sum(1 for p in service_pods if p.status == "Healthy")
            
            metrics.append(f'service_latency_ms{{service="{service}"}} {avg_latency}')
            metrics.append(f'service_error_rate{{service="{service}"}} {avg_error_rate}')
            metrics.append(f'service_healthy_pods{{service="{service}"}} {healthy_count}')
            metrics.append(f'service_total_pods{{service="{service}"}} {len(service_pods)}')
    
    # SLO metrics
    metrics.append(f'slo_latency_p95_target_ms {slo_data["latency_p95_target_ms"]}')
    metrics.append(f'slo_availability_target {slo_data["availability_target"]}')
    metrics.append(f'slo_burn_rate_5m {slo_data["burn_rate_5m"]}')
    metrics.append(f'slo_budget_remaining {slo_data["budget_remaining"]}')
    
    return "\n".join(metrics)

@app.get("/slo")
async def get_slo():
    """Get SLO status and burn rate"""
    # Calculate current burn rate (simplified)
    total_errors = sum(p.error_rate for p in pods.values())
    total_pods = len(pods)
    current_error_rate = total_errors / total_pods if total_pods > 0 else 0
    
    # Simple burn rate calculation (error rate vs target)
    target_error_rate = 1 - slo_data["availability_target"]
    burn_rate = current_error_rate / target_error_rate if target_error_rate > 0 else 0
    
    # Update budget (simplified calculation)
    slo_data["burn_rate_5m"] = burn_rate
    slo_data["budget_remaining"] = max(0, slo_data["budget_remaining"] - (burn_rate * 0.01))
    
    return SLOStatus(
        latency_p95_target_ms=slo_data["latency_p95_target_ms"],
        availability_target=slo_data["availability_target"],
        burn_rate_5m=burn_rate,
        budget_remaining=slo_data["budget_remaining"]
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
