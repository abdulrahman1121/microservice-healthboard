#!/usr/bin/env python3
"""
Python demo script for the Microservice Healthboard API
Demonstrates various fault injection scenarios using the REST API
"""

import requests
import time
import json
from typing import Dict, Any

API_BASE = "http://localhost:8000"

class HealthboardDemo:
    def __init__(self, api_base: str = API_BASE):
        self.api_base = api_base
        self.session = requests.Session()
    
    def api_call(self, method: str, endpoint: str, data: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """Make an API call and return the response"""
        url = f"{self.api_base}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        
        except requests.exceptions.RequestException as e:
            print(f"❌ API call failed: {e}")
            return {}
    
    def get_pods(self) -> Dict[Any, Any]:
        """Get current pod status"""
        return self.api_call("GET", "/pods")
    
    def get_slo(self) -> Dict[Any, Any]:
        """Get SLO status"""
        return self.api_call("GET", "/slo")
    
    def inject_fault(self, pod_id: str, delay_ms: int = None, error_rate: float = None, kill: bool = None) -> Dict[Any, Any]:
        """Inject a fault into a specific pod"""
        fault_data = {}
        if delay_ms is not None:
            fault_data["delay_ms"] = delay_ms
        if error_rate is not None:
            fault_data["error_rate"] = error_rate
        if kill is not None:
            fault_data["kill"] = kill
        
        return self.api_call("POST", f"/fault/{pod_id}", fault_data)
    
    def restart_pod(self, pod_id: str) -> Dict[Any, Any]:
        """Restart a specific pod"""
        return self.api_call("POST", f"/restart/{pod_id}")
    
    def print_status(self, title: str = ""):
        """Print current system status"""
        if title:
            print(f"\n📊 {title}")
            print("=" * (len(title) + 4))
        
        pods = self.get_pods()
        slo = self.get_slo()
        
        if pods and "pods" in pods:
            print("🔧 Pod Status:")
            for pod in pods["pods"]:
                status_emoji = {"Healthy": "🟢", "Degraded": "🟡", "Down": "🔴"}.get(pod["status"], "⚪")
                print(f"  {status_emoji} {pod['id']}: {pod['status']} "
                      f"(Latency: {pod['latency_ms']:.0f}ms, "
                      f"Errors: {pod['error_rate']*100:.0f}%, "
                      f"Restarts: {pod['restarts']})")
        
        if slo:
            print(f"\n📈 SLO Status:")
            print(f"  🎯 Latency P95 Target: {slo['latency_p95_target_ms']}ms")
            print(f"  🎯 Availability Target: {slo['availability_target']*100:.1f}%")
            print(f"  🔥 Burn Rate (5m): {slo['burn_rate_5m']:.2f}x")
            print(f"  💰 Budget Remaining: {slo['budget_remaining']*100:.1f}%")
    
    def wait_and_observe(self, message: str, seconds: int = 3):
        """Wait and then show current status"""
        print(f"\n⏳ {message}")
        time.sleep(seconds)
        self.print_status("Current Status")
    
    def run_demo(self):
        """Run the complete demo"""
        print("🚀 Microservice Healthboard - Python API Demo")
        print("=" * 50)
        
        # Check if backend is running
        try:
            self.get_pods()
        except:
            print("❌ Backend is not running. Please start it first:")
            print("   cd backend && python app.py")
            return
        
        print("✅ Backend is running!")
        
        # Initial status
        self.print_status("Initial State")
        
        # Scenario 1: Latency injection
        print("\n🎯 Scenario 1: Latency Injection")
        print("-" * 35)
        self.inject_fault("sensor-sim-pod-1", delay_ms=1000)
        self.wait_and_observe("Added 1000ms delay to sensor-sim-pod-1", 3)
        
        # Scenario 2: Error rate injection
        print("\n🎯 Scenario 2: Error Rate Injection")
        print("-" * 37)
        self.inject_fault("planner-sim-pod-1", error_rate=0.3)
        self.wait_and_observe("Set 30% error rate for planner-sim-pod-1", 3)
        
        # Scenario 3: Pod kill
        print("\n🎯 Scenario 3: Pod Failure")
        print("-" * 25)
        self.inject_fault("ui-proxy-pod-1", kill=True)
        self.wait_and_observe("Killed ui-proxy-pod-1", 3)
        
        # Scenario 4: Mixed faults
        print("\n🎯 Scenario 4: Mixed Faults")
        print("-" * 26)
        self.inject_fault("sensor-sim-pod-1", delay_ms=500, error_rate=0.2)
        self.inject_fault("planner-sim-pod-1", error_rate=0.4)
        self.wait_and_observe("Applied mixed faults to multiple pods", 3)
        
        # Scenario 5: Recovery
        print("\n🎯 Scenario 5: Recovery")
        print("-" * 20)
        print("🔄 Restarting all pods...")
        self.restart_pod("sensor-sim-pod-1")
        self.restart_pod("planner-sim-pod-1")
        self.restart_pod("ui-proxy-pod-1")
        self.wait_and_observe("All pods restarted", 3)
        
        # Final status
        self.print_status("Final State - All Systems Recovered")
        
        print("\n✅ Demo completed successfully!")
        print("🌐 Check the frontend dashboard at: http://localhost:3000")

def main():
    demo = HealthboardDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
