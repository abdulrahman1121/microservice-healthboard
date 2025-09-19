import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Charts = ({ pods }) => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString();
    
    // Calculate service-level metrics
    const services = {};
    pods.forEach(pod => {
      if (!services[pod.service]) {
        services[pod.service] = {
          latency: [],
          errorRate: [],
          healthy: []
        };
      }
      services[pod.service].latency.push(pod.latency_ms);
      services[pod.service].errorRate.push(pod.error_rate);
      services[pod.service].healthy.push(pod.status === 'Healthy' ? 1 : 0);
    });

    const newDataPoint = {
      time: timestamp,
      timestamp: now.getTime()
    };

    // Add service metrics to data point
    Object.entries(services).forEach(([serviceName, metrics]) => {
      const avgLatency = metrics.latency.reduce((sum, val) => sum + val, 0) / metrics.latency.length;
      const avgErrorRate = metrics.errorRate.reduce((sum, val) => sum + val, 0) / metrics.errorRate.length;
      const healthyRatio = metrics.healthy.reduce((sum, val) => sum + val, 0) / metrics.healthy.length;
      
      newDataPoint[`${serviceName}_latency`] = Math.round(avgLatency);
      newDataPoint[`${serviceName}_error_rate`] = Math.round(avgErrorRate * 100);
      newDataPoint[`${serviceName}_healthy`] = Math.round(healthyRatio * 100);
    });

    setChartData(prev => {
      const updated = [...prev, newDataPoint];
      // Keep only last 5 minutes of data (300 data points at 1s intervals)
      return updated.slice(-300);
    });
  }, [pods]);

  const services = ['sensor-sim', 'planner-sim', 'ui-proxy'];
  const colors = {
    'sensor-sim': '#8884d8',
    'planner-sim': '#82ca9d',
    'ui-proxy': '#ffc658'
  };

  return (
    <div className="charts-section">
      <h3>Real-time Metrics (Last 5 Minutes)</h3>
      
      <div className="charts-grid">
        <div>
          <h4 style={{ marginBottom: '15px', color: '#333' }}>Latency (ms)</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="time" 
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                labelStyle={{ color: '#333' }}
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
              />
              <Legend />
              {services.map(service => (
                <Line
                  key={`${service}_latency`}
                  type="monotone"
                  dataKey={`${service}_latency`}
                  stroke={colors[service]}
                  strokeWidth={2}
                  dot={false}
                  name={`${service} latency`}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div>
          <h4 style={{ marginBottom: '15px', color: '#333' }}>Error Rate (%)</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="time" 
                tick={{ fontSize: 12 }}
                interval="preserveStartEnd"
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip 
                labelStyle={{ color: '#333' }}
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
              />
              <Legend />
              {services.map(service => (
                <Line
                  key={`${service}_error_rate`}
                  type="monotone"
                  dataKey={`${service}_error_rate`}
                  stroke={colors[service]}
                  strokeWidth={2}
                  dot={false}
                  name={`${service} error rate`}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h4 style={{ marginBottom: '15px', color: '#333' }}>Service Health (%)</h4>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              domain={[0, 100]}
              tick={{ fontSize: 12 }}
            />
            <Tooltip 
              labelStyle={{ color: '#333' }}
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
            />
            <Legend />
            {services.map(service => (
              <Line
                key={`${service}_healthy`}
                type="monotone"
                dataKey={`${service}_healthy`}
                stroke={colors[service]}
                strokeWidth={2}
                dot={false}
                name={`${service} health`}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;
