import React, { useState } from 'react';
import { Check, Edit3, X, AlertCircle } from 'lucide-react';

interface HumanReviewModalProps {
  sessionId: string;
  onApprove: (sessionId: string) => void;
  onEdit: (sessionId: string, feedback: string) => void;
  onReject: (sessionId: string) => void;
  isLoading: boolean;
}

export const HumanReviewModal: React.FC<HumanReviewModalProps> = ({
  sessionId,
  onApprove,
  onEdit,
  onReject,
  isLoading,
}) => {
  const [feedback, setFeedback] = useState('');
  const [showEditInput, setShowEditInput] = useState(false);

  return (
    <div
      className="glass-card"
      style={{
        padding: '1.5rem 2rem',
        marginBottom: '2rem',
        borderColor: 'rgba(245, 158, 11, 0.5)',
        background: 'rgba(30, 25, 15, 0.85)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
        <AlertCircle size={24} color="#f59e0b" />
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fbbf24' }}>
            Human-in-the-Loop Review Required
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            LangGraph execution paused at checkpointer interrupt. Please review proposed plan before proceeding.
          </p>
        </div>
      </div>

      {showEditInput && (
        <div style={{ marginBottom: '1rem' }}>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="Specify your plan edit request (e.g. Choose a 4-star hotel near downtown, or make flights cheaper)..."
            rows={2}
            style={{
              width: '100%',
              background: 'rgba(0, 0, 0, 0.4)',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              borderRadius: '8px',
              color: 'var(--text-main)',
              padding: '0.75rem',
              fontSize: '0.85rem',
              fontFamily: 'inherit',
              marginBottom: '0.5rem',
            }}
          />
        </div>
      )}

      <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
        <button
          onClick={() => onApprove(sessionId)}
          disabled={isLoading}
          className="btn-success"
          style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
        >
          <Check size={16} /> Approve & Finalize
        </button>

        {!showEditInput ? (
          <button
            onClick={() => setShowEditInput(true)}
            disabled={isLoading}
            className="btn-warning"
            style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Edit3 size={16} /> Edit / Revise Plan
          </button>
        ) : (
          <button
            onClick={() => onEdit(sessionId, feedback)}
            disabled={isLoading || !feedback.trim()}
            className="btn-warning"
            style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Edit3 size={16} /> Submit Revision Instructions
          </button>
        )}

        <button
          onClick={() => onReject(sessionId)}
          disabled={isLoading}
          className="btn-danger"
          style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
        >
          <X size={16} /> Reject Plan
        </button>
      </div>
    </div>
  );
};
