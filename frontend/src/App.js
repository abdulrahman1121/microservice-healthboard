import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ServiceCard from './components/ServiceCard';
import SLODashboard from './components/SLODashboard';
import Charts from './components/Charts';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [pods, setPods] = useState([]);
  const [sloData, setSloData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [podsResponse, sloResponse] = await Promise.all([
        axios.get(`${API_BASE}/pods`),
        axios.get(`${API_BASE}/slo`)
      ]);
      
      setPods(podsResponse.data.pods);
      setSloData(sloResponse.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data from backend');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000); // Update every second
    return () => clearInterval(interval);
  }, []);

  const handleFaultInjection = async (podId, faultData) => {
    try {
      await axios.post(`${API_BASE}/fault/${podId}`, faultData);
      fetchData(); // Refresh data
    } catch (err) {
      setError(`Failed to inject fault: ${err.message}`);
    }
  };

  const handleRestart = async (podId) => {
    try {
      await axios.post(`${API_BASE}/restart/${podId}`);
      fetchData(); // Refresh data
    } catch (err) {
      setError(`Failed to restart pod: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="header">
          <h1>Microservice Healthboard</h1>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="header">
          <h1>Microservice Healthboard</h1>
          <p style={{ color: 'red' }}>Error: {error}</p>
          <button onClick={fetchData} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Group pods by service
  const services = {};
  pods.forEach(pod => {
    if (!services[pod.service]) {
      services[pod.service] = [];
    }
    services[pod.service].push(pod);
  });

  return (
    <div className="container">
      <div className="header">
        <h1>Microservice Healthboard</h1>
        <p>Kubernetes-style monitoring with fault injection capabilities</p>
      </div>

      {sloData && <SLODashboard sloData={sloData} />}

      <div className="grid">
        {Object.entries(services).map(([serviceName, servicePods]) => (
          <ServiceCard
            key={serviceName}
            serviceName={serviceName}
            pods={servicePods}
            onFaultInjection={handleFaultInjection}
            onRestart={handleRestart}
          />
        ))}
      </div>

      <Charts pods={pods} />
    </div>
  );
}

export default App;
