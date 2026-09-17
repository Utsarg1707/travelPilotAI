import React from 'react';
import { CheckCircle2, Clock, AlertTriangle, ShieldCheck, UserCheck, Bot } from 'lucide-react';
import { PlanResponse } from '../types/travel';

interface WorkflowVisualizerProps {
  planResponse?: PlanResponse;
  isLoading: boolean;
}

export const WorkflowVisualizer: React.FC<WorkflowVisualizerProps> = ({ planResponse, isLoading }) => {
  const selectedAgents = planResponse?.selected_agents || ['flight', 'hotel', 'weather', 'budget', 'itinerary'];

  const nodes = [
    { id: 'guardrail', name: 'Input Guardrail', type: 'guardrail', icon: ShieldCheck },
    { id: 'supervisor', name: 'Supervisor Agent', type: 'supervisor', icon: Bot },
    { id: 'flight', name: 'Flight Agent', type: 'specialist', icon: Bot },
    { id: 'hotel', name: 'Hotel Agent', type: 'specialist', icon: Bot },
    { id: 'weather', name: 'Weather Agent', type: 'specialist', icon: Bot },
    { id: 'budget', name: 'Budget Agent', type: 'specialist', icon: Bot },
    { id: 'itinerary', name: 'Itinerary Agent', type: 'specialist', icon: Bot },
    { id: 'output_guardrail', name: 'Output Guardrail', type: 'guardrail', icon: ShieldCheck },
    { id: 'hitl', name: 'Human Review', type: 'hitl', icon: UserCheck },
  ];

  const getNodeStatus = (nodeId: string) => {
    if (!planResponse && !isLoading) return 'pending';
    if (isLoading) return 'running';
    if (planResponse?.status === 'blocked' && nodeId !== 'guardrail') return 'pending';
    if (nodeId === 'guardrail') return 'completed';
    if (nodeId === 'supervisor') return 'completed';

    if (['flight', 'hotel', 'weather', 'budget', 'itinerary'].includes(nodeId)) {
      return selectedAgents.includes(nodeId) ? 'completed' : 'skipped';
    }

    if (nodeId === 'output_guardrail') return 'completed';
    if (nodeId === 'hitl') {
      return planResponse?.status === 'waiting_for_approval' ? 'waiting' : 'completed';
    }
    return 'completed';
  };

  return (
    <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
      <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--text-muted)' }}>
        LangGraph Multi-Agent Execution State
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '0.75rem' }}>
        {nodes.map((node) => {
          const status = getNodeStatus(node.id);
          const Icon = node.icon;

          let statusBg = 'rgba(255, 255, 255, 0.04)';
          let statusBorder = 'rgba(255, 255, 255, 0.1)';
          let statusColor = 'var(--text-muted)';

          if (status === 'completed') {
            statusBg = 'rgba(16, 185, 129, 0.1)';
            statusBorder = 'rgba(16, 185, 129, 0.4)';
            statusColor = '#34d399';
          } else if (status === 'running') {
            statusBg = 'rgba(99, 102, 241, 0.15)';
            statusBorder = 'rgba(99, 102, 241, 0.5)';
            statusColor = '#818cf8';
          } else if (status === 'waiting') {
            statusBg = 'rgba(245, 158, 11, 0.15)';
            statusBorder = 'rgba(245, 158, 11, 0.5)';
            statusColor = '#fbbf24';
          } else if (status === 'skipped') {
            statusBg = 'rgba(255, 255, 255, 0.02)';
            statusBorder = 'rgba(255, 255, 255, 0.05)';
            statusColor = '#475569';
          }

          return (
            <div
              key={node.id}
              style={{
                background: statusBg,
                border: `1px solid ${statusBorder}`,
                borderRadius: '12px',
                padding: '0.75rem',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                gap: '0.4rem',
              }}
              className={status === 'running' ? 'pulse-running' : ''}
            >
              <Icon size={18} color={statusColor} />
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: statusColor }}>{node.name}</span>
              <span style={{ fontSize: '0.65rem', textTransform: 'capitalize', opacity: 0.8 }}>
                {status === 'waiting' ? 'Waiting Review' : status}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
