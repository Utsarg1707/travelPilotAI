import React, { useState } from 'react';
import { Send, Sparkles } from 'lucide-react';

interface TravelFormProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

export const TravelForm: React.FC<TravelFormProps> = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState(
    'Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000. I like beaches, food and relaxed activities.'
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const sampleQueries = [
    'Plan a 5-day trip to Dubai from Bangalore for 2 people under ₹1.5L',
    'What is the weather in Dubai next week?',
    'Find flights from Bangalore to Dubai for 2 passengers',
  ];

  return (
    <div className="glass-card" style={{ padding: '2rem', marginBottom: '2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
        <Sparkles size={20} color="#6366f1" />
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Describe Your Travel Goal</h2>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ position: 'relative', marginBottom: '1rem' }}>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            placeholder="e.g. Plan a 4-day trip to Paris from London for 2 people with a budget of €2000..."
            rows={3}
            style={{
              width: '100%',
              background: 'rgba(10, 15, 26, 0.7)',
              border: '1px solid rgba(99, 102, 241, 0.3)',
              borderRadius: '12px',
              color: 'var(--text-main)',
              padding: '1rem',
              fontSize: '0.95rem',
              fontFamily: 'inherit',
              resize: 'vertical',
              outline: 'none',
            }}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', alignSelf: 'center' }}>Examples:</span>
            {sampleQueries.map((q, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setQuery(q)}
                disabled={isLoading}
                style={{
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  color: 'var(--text-muted)',
                  fontSize: '0.75rem',
                  padding: '0.3rem 0.6rem',
                  cursor: 'pointer',
                }}
              >
                {q.length > 35 ? q.substring(0, 35) + '...' : q}
              </button>
            ))}
          </div>

          <button type="submit" disabled={isLoading} className="btn-primary">
            <Send size={18} /> {isLoading ? 'Orchestrating Agents...' : 'Execute Agent Plan'}
          </button>
        </div>
      </form>
    </div>
  );
};
