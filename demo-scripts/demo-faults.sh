#!/bin/bash

# Demo script for fault injection testing
# Make sure the backend is running on localhost:8000

API_BASE="http://localhost:8000"

echo "🚀 Microservice Healthboard - Fault Injection Demo"
echo "=================================================="
echo ""

# Function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -n "$data" ]; then
        curl -s -X $method "$API_BASE$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X $method "$API_BASE$endpoint"
    fi
    echo ""
}

# Function to wait and show status
wait_and_show() {
    local message=$1
    local seconds=$2
    
    echo "⏳ $message"
    sleep $seconds
    echo "📊 Current pod status:"
    api_call "GET" "/pods"
    echo ""
}

echo "1. Initial state - All pods healthy"
api_call "GET" "/pods"
echo ""

echo "2. Injecting 1000ms delay into sensor-sim-pod-1"
api_call "POST" "/fault/sensor-sim-pod-1" '{"delay_ms": 1000}'
wait_and_show "Waiting 3 seconds to observe latency impact..." 3

echo "3. Setting 30% error rate for planner-sim-pod-1"
api_call "POST" "/fault/planner-sim-pod-1" '{"error_rate": 0.3}'
wait_and_show "Waiting 3 seconds to observe error rate impact..." 3

echo "4. Killing ui-proxy-pod-1"
api_call "POST" "/fault/ui-proxy-pod-1" '{"kill": true}'
wait_and_show "Waiting 3 seconds to observe pod down status..." 3

echo "5. Checking SLO status"
api_call "GET" "/slo"
echo ""

echo "6. Restarting ui-proxy-pod-1"
api_call "POST" "/restart/ui-proxy-pod-1"
wait_and_show "Waiting 2 seconds to observe pod recovery..." 2

echo "7. Clearing all faults from sensor-sim-pod-1"
api_call "POST" "/fault/sensor-sim-pod-1" '{"delay_ms": 0}'
wait_and_show "Waiting 2 seconds to observe latency recovery..." 2

echo "8. Clearing error rate from planner-sim-pod-1"
api_call "POST" "/fault/planner-sim-pod-1" '{"error_rate": 0}'
wait_and_show "Waiting 2 seconds to observe error rate recovery..." 2

echo "9. Final state - All pods should be healthy"
api_call "GET" "/pods"
echo ""

echo "10. Final SLO status"
api_call "GET" "/slo"
echo ""

echo "✅ Demo completed! Check the frontend at http://localhost:3000 to see the visual dashboard."
