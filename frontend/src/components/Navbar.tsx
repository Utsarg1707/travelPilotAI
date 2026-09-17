import React from 'react';
import { Compass, Shield, Zap } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="glass-card" style={{ margin: '1rem 2rem', padding: '1rem 2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            background: 'var(--accent-gradient)',
            padding: '0.6rem',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Compass size={24} color="white" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.4rem', fontWeight: 800, background: 'var(--accent-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              TravelPilot AI
            </h1>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Production Agentic Multi-Agent Orchestrator
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span className="badge badge-demo" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Zap size={14} /> Demo Mode (Free Tier)
          </span>
          <span className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Shield size={14} /> Guardrails Active
          </span>
        </div>
      </div>
    </header>
  );
};
