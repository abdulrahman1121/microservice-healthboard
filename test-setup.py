#!/usr/bin/env python3
"""
Test script to verify the Microservice Healthboard setup
"""

import requests
import time
import sys

def test_backend():
    """Test if the backend is running and responding"""
    print("🔧 Testing Backend...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test pods endpoint
        response = requests.get("http://localhost:8000/pods", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "pods" in data and len(data["pods"]) > 0:
                print(f"✅ Found {len(data['pods'])} pods")
            else:
                print("❌ No pods found")
                return False
        else:
            print(f"❌ Pods endpoint failed: {response.status_code}")
            return False
        
        # Test SLO endpoint
        response = requests.get("http://localhost:8000/slo", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "burn_rate_5m" in data:
                print("✅ SLO endpoint working")
            else:
                print("❌ SLO endpoint missing data")
                return False
        else:
            print(f"❌ SLO endpoint failed: {response.status_code}")
            return False
        
        # Test metrics endpoint
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        if response.status_code == 200:
            if "pod_healthy" in response.text:
                print("✅ Metrics endpoint working")
            else:
                print("❌ Metrics endpoint missing data")
                return False
        else:
            print(f"❌ Metrics endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_fault_injection():
    """Test fault injection functionality"""
    print("\n🎯 Testing Fault Injection...")
    
    try:
        # Test delay injection
        response = requests.post(
            "http://localhost:8000/fault/sensor-sim-pod-1",
            json={"delay_ms": 500},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Delay injection working")
        else:
            print(f"❌ Delay injection failed: {response.status_code}")
            return False
        
        # Test error rate injection
        response = requests.post(
            "http://localhost:8000/fault/planner-sim-pod-1",
            json={"error_rate": 0.2},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Error rate injection working")
        else:
            print(f"❌ Error rate injection failed: {response.status_code}")
            return False
        
        # Test pod restart
        response = requests.post(
            "http://localhost:8000/restart/sensor-sim-pod-1",
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Pod restart working")
        else:
            print(f"❌ Pod restart failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fault injection test failed: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print("\n🎨 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Is it running on localhost:3000?")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    print("🧪 Microservice Healthboard - Setup Test")
    print("=" * 45)
    
    backend_ok = test_backend()
    
    if backend_ok:
        fault_ok = test_fault_injection()
    else:
        fault_ok = False
    
    frontend_ok = test_frontend()
    
    print("\n📊 Test Results:")
    print("=" * 15)
    print(f"Backend:        {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Fault Injection: {'✅ PASS' if fault_ok else '❌ FAIL'}")
    print(f"Frontend:       {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if backend_ok and fault_ok and frontend_ok:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\n🌐 Access the dashboard at: http://localhost:3000")
        print("🔧 API documentation at: http://localhost:8000/docs")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the setup.")
        if not backend_ok:
            print("   - Start the backend: cd backend && python app.py")
        if not frontend_ok:
            print("   - Start the frontend: cd frontend && npm start")
        return 1

if __name__ == "__main__":
    sys.exit(main())
