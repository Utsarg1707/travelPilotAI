import React from 'react';
import { Plane, Hotel, CloudSun, DollarSign, Calendar, Info } from 'lucide-react';
import { PlanResponse } from '../types/travel';

interface ResultsDashboardProps {
  planResponse: PlanResponse;
}

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ planResponse }) => {
  if (!planResponse.final_response) return null;

  const decision = planResponse.supervisor_decision;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Overview & Metadata Card */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>
              ✈️ Trip Plan: {decision?.destination || 'Destination'}
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Origin: {decision?.origin || 'Bangalore'} | Travelers: {decision?.travelers || 1} | Duration: {decision?.duration_days || 5} Days
            </p>
          </div>
          <span className={`badge ${planResponse.approval_status === 'approved' ? 'badge-success' : 'badge-warning'}`}>
            Status: {planResponse.approval_status}
          </span>
        </div>

        {decision?.routing_reason && (
          <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.75rem 1rem', borderRadius: '8px', fontSize: '0.85rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <Info size={16} color="#818cf8" />
            <span><strong>Supervisor Routing Metadata:</strong> {decision.routing_reason}</span>
          </div>
        )}
      </div>

      {/* Structured Output Render */}
      <div className="glass-card" style={{ padding: '2rem' }}>
        <div style={{ whiteSpace: 'pre-line', fontSize: '0.95rem', lineHeight: 1.7 }}>
          {planResponse.final_response}
        </div>
      </div>

      {/* Tool Call Audit Log */}
      {planResponse.tool_calls && planResponse.tool_calls.length > 0 && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--text-muted)' }}>
            🛠️ Model Context Protocol (MCP) Executed Tools Audit Log
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {planResponse.tool_calls.map((t, idx) => (
              <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '0.6rem 1rem', borderRadius: '8px', fontSize: '0.8rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontWeight: 600, color: '#38bdf8' }}>[{t.agent_name}]</span> call <code style={{ color: '#a78bfa' }}>{t.tool_name}</code>
                  <span style={{ color: 'var(--text-muted)', marginLeft: '0.5rem' }}>— {t.result_summary}</span>
                </div>
                <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{t.execution_time_ms} ms</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
