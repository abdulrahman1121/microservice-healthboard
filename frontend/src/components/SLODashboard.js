import React from 'react';

const SLODashboard = ({ sloData }) => {
  const getBurnRateStatus = (burnRate) => {
    if (burnRate > 2.0) return 'high';
    if (burnRate > 1.0) return 'medium';
    return 'normal';
  };

  const burnRateStatus = getBurnRateStatus(sloData.burn_rate_5m);
  const budgetPercentage = Math.round(sloData.budget_remaining * 100);

  return (
    <div className="slo-dashboard">
      <h2>Service Level Objectives (SLO)</h2>
      
      <div className="slo-metrics">
        <div className="slo-metric">
          <div className="slo-metric-label">Latency P95 Target</div>
          <div className="slo-metric-value">{sloData.latency_p95_target_ms}ms</div>
          <div className="slo-metric-target">Target: &lt; 200ms</div>
        </div>
        
        <div className="slo-metric">
          <div className="slo-metric-label">Availability Target</div>
          <div className="slo-metric-value">
            {Math.round(sloData.availability_target * 100)}%
          </div>
          <div className="slo-metric-target">Target: 99.5%</div>
        </div>
        
        <div className="slo-metric">
          <div className="slo-metric-label">Error Budget</div>
          <div className="slo-metric-value">{budgetPercentage}%</div>
          <div className="slo-metric-target">Remaining</div>
        </div>
      </div>
      
      <div className={`burn-rate ${burnRateStatus}`}>
        <div style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '5px' }}>
          Burn Rate (5m): {sloData.burn_rate_5m.toFixed(2)}x
        </div>
        <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>
          {burnRateStatus === 'high' && '🚨 High burn rate - immediate attention required'}
          {burnRateStatus === 'medium' && '⚠️ Elevated burn rate - monitor closely'}
          {burnRateStatus === 'normal' && '✅ Normal burn rate - within acceptable limits'}
        </div>
      </div>
    </div>
  );
};

export default SLODashboard;
