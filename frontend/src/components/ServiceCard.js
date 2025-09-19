import React, { useState } from 'react';

const ServiceCard = ({ serviceName, pods, onFaultInjection, onRestart }) => {
  const [faultData, setFaultData] = useState({
    delay_ms: 0,
    error_rate: 0,
    kill: false
  });

  const getServiceStatus = () => {
    const healthyPods = pods.filter(pod => pod.status === 'Healthy').length;
    const totalPods = pods.length;
    
    if (healthyPods === totalPods) return 'Healthy';
    if (healthyPods > 0) return 'Degraded';
    return 'Down';
  };

  const getAverageLatency = () => {
    const totalLatency = pods.reduce((sum, pod) => sum + pod.latency_ms, 0);
    return Math.round(totalLatency / pods.length);
  };

  const getAverageErrorRate = () => {
    const totalErrorRate = pods.reduce((sum, pod) => sum + pod.error_rate, 0);
    return Math.round((totalErrorRate / pods.length) * 100);
  };

  const getTotalRestarts = () => {
    return pods.reduce((sum, pod) => sum + pod.restarts, 0);
  };

  const handleFaultInjection = (podId) => {
    onFaultInjection(podId, faultData);
  };

  const handleRestart = (podId) => {
    onRestart(podId);
  };

  const serviceStatus = getServiceStatus();

  return (
    <div className="card">
      <h3>{serviceName}</h3>
      
      <div className="status-container" style={{ marginBottom: '15px' }}>
        <span className={`status ${serviceStatus.toLowerCase()}`}>
          {serviceStatus}
        </span>
        <span style={{ marginLeft: '10px', fontSize: '0.9rem', color: '#666' }}>
          {pods.length} pod{pods.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="metrics">
        <div className="metric">
          <div className="metric-label">Avg Latency</div>
          <div className="metric-value">{getAverageLatency()}ms</div>
        </div>
        <div className="metric">
          <div className="metric-label">Error Rate</div>
          <div className="metric-value">{getAverageErrorRate()}%</div>
        </div>
        <div className="metric">
          <div className="metric-label">Restarts</div>
          <div className="metric-value">{getTotalRestarts()}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Healthy</div>
          <div className="metric-value">
            {pods.filter(p => p.status === 'Healthy').length}/{pods.length}
          </div>
        </div>
      </div>

      <div style={{ marginTop: '15px' }}>
        <h4 style={{ margin: '0 0 10px 0', fontSize: '1rem', color: '#333' }}>
          Fault Injection
        </h4>
        
        <div className="input-group">
          <label>Delay (ms):</label>
          <input
            type="number"
            value={faultData.delay_ms}
            onChange={(e) => setFaultData({...faultData, delay_ms: parseInt(e.target.value) || 0})}
            min="0"
            max="5000"
          />
        </div>
        
        <div className="input-group">
          <label>Error Rate:</label>
          <input
            type="number"
            value={faultData.error_rate}
            onChange={(e) => setFaultData({...faultData, error_rate: parseFloat(e.target.value) || 0})}
            min="0"
            max="1"
            step="0.1"
          />
        </div>
        
        <div className="input-group">
          <label>
            <input
              type="checkbox"
              checked={faultData.kill}
              onChange={(e) => setFaultData({...faultData, kill: e.target.checked})}
            />
            Kill Pod
          </label>
        </div>
      </div>

      <div className="controls">
        {pods.map(pod => (
          <div key={pod.id} style={{ display: 'flex', flexDirection: 'column', gap: '5px', marginBottom: '10px' }}>
            <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: '500' }}>
              {pod.id}
            </div>
            <div style={{ display: 'flex', gap: '5px' }}>
              <button
                className="btn btn-warning"
                onClick={() => handleFaultInjection(pod.id)}
                disabled={pod.killed}
              >
                Inject Fault
              </button>
              <button
                className="btn btn-success"
                onClick={() => handleRestart(pod.id)}
              >
                Restart
              </button>
            </div>
            <div style={{ fontSize: '0.7rem', color: '#999' }}>
              Status: {pod.status} | Latency: {Math.round(pod.latency_ms)}ms | 
              Errors: {Math.round(pod.error_rate * 100)}% | Restarts: {pod.restarts}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ServiceCard;
