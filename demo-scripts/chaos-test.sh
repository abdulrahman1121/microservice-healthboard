#!/bin/bash

# Chaos engineering demo script
# Simulates various failure scenarios

API_BASE="http://localhost:8000"

echo "🔥 Chaos Engineering Demo - Microservice Healthboard"
echo "===================================================="
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

# Function to show SLO status
show_slo() {
    echo "📊 SLO Status:"
    api_call "GET" "/slo"
    echo ""
}

echo "🎯 Scenario 1: Gradual Degradation"
echo "=================================="
echo "Injecting increasing delays across all services..."

for delay in 200 500 1000 2000; do
    echo "Adding ${delay}ms delay to all pods..."
    api_call "POST" "/fault/sensor-sim-pod-1" "{\"delay_ms\": $delay}"
    api_call "POST" "/fault/planner-sim-pod-1" "{\"delay_ms\": $delay}"
    api_call "POST" "/fault/ui-proxy-pod-1" "{\"delay_ms\": $delay}"
    sleep 2
    show_slo
done

echo "🔄 Recovering from delays..."
api_call "POST" "/fault/sensor-sim-pod-1" '{"delay_ms": 0}'
api_call "POST" "/fault/planner-sim-pod-1" '{"delay_ms": 0}'
api_call "POST" "/fault/ui-proxy-pod-1" '{"delay_ms": 0}'
sleep 3
echo ""

echo "💥 Scenario 2: Error Rate Storm"
echo "==============================="
echo "Gradually increasing error rates..."

for rate in 0.1 0.2 0.3 0.5 0.7; do
    echo "Setting ${rate} error rate across all services..."
    api_call "POST" "/fault/sensor-sim-pod-1" "{\"error_rate\": $rate}"
    api_call "POST" "/fault/planner-sim-pod-1" "{\"error_rate\": $rate}"
    api_call "POST" "/fault/ui-proxy-pod-1" "{\"error_rate\": $rate}"
    sleep 2
    show_slo
done

echo "🔄 Recovering from error storm..."
api_call "POST" "/fault/sensor-sim-pod-1" '{"error_rate": 0}'
api_call "POST" "/fault/planner-sim-pod-1" '{"error_rate": 0}'
api_call "POST" "/fault/ui-proxy-pod-1" '{"error_rate": 0}'
sleep 3
echo ""

echo "💀 Scenario 3: Complete Service Failure"
echo "======================================="
echo "Killing all pods one by one..."

echo "Killing sensor-sim-pod-1..."
api_call "POST" "/fault/sensor-sim-pod-1" '{"kill": true}'
sleep 2
show_slo

echo "Killing planner-sim-pod-1..."
api_call "POST" "/fault/planner-sim-pod-1" '{"kill": true}'
sleep 2
show_slo

echo "Killing ui-proxy-pod-1..."
api_call "POST" "/fault/ui-proxy-pod-1" '{"kill": true}'
sleep 2
show_slo

echo "🔄 Recovery sequence..."
echo "Restarting all pods..."

api_call "POST" "/restart/sensor-sim-pod-1"
api_call "POST" "/restart/planner-sim-pod-1"
api_call "POST" "/restart/ui-proxy-pod-1"

sleep 3
echo "Final recovery status:"
api_call "GET" "/pods"
show_slo

echo "🎯 Scenario 4: Mixed Faults"
echo "==========================="
echo "Applying different faults to different services..."

api_call "POST" "/fault/sensor-sim-pod-1" '{"delay_ms": 1500, "error_rate": 0.2}'
api_call "POST" "/fault/planner-sim-pod-1" '{"error_rate": 0.4}'
api_call "POST" "/fault/ui-proxy-pod-1" '{"delay_ms": 800}'

sleep 3
echo "Mixed fault status:"
api_call "GET" "/pods"
show_slo

echo "🔄 Final recovery..."
api_call "POST" "/restart/sensor-sim-pod-1"
api_call "POST" "/restart/planner-sim-pod-1"
api_call "POST" "/restart/ui-proxy-pod-1"

sleep 2
echo "✅ All systems recovered!"
api_call "GET" "/pods"
show_slo

echo ""
echo "🎉 Chaos engineering demo completed!"
echo "Check the frontend dashboard to see the visual impact of these scenarios."
