import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { TravelForm } from './components/TravelForm';
import { WorkflowVisualizer } from './components/WorkflowVisualizer';
import { ResultsDashboard } from './components/ResultsDashboard';
import { HumanReviewModal } from './components/HumanReviewModal';
import { submitTravelPlan, approvePlan, editPlan, rejectPlan } from './services/api';
import { PlanResponse } from './types/travel';
import { AlertTriangle } from 'lucide-react';

export const App: React.FC = () => {
  const [planResponse, setPlanResponse] = useState<PlanResponse | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleQuerySubmit = async (query: string) => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await submitTravelPlan(query);
      setPlanResponse(res);
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred while communicating with the travel backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (sessionId: string) => {
    setIsLoading(true);
    try {
      const res = await approvePlan(sessionId);
      setPlanResponse(res);
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = async (sessionId: string, feedback: string) => {
    setIsLoading(true);
    try {
      const res = await editPlan(sessionId, feedback);
      setPlanResponse(res);
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReject = async (sessionId: string) => {
    setIsLoading(true);
    try {
      const res = await rejectPlan(sessionId);
      setPlanResponse(res);
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', paddingBottom: '4rem' }}>
      <Navbar />

      <main style={{ padding: '0 2rem' }}>
        <TravelForm onSubmit={handleQuerySubmit} isLoading={isLoading} />

        {errorMsg && (
          <div
            className="glass-card"
            style={{
              padding: '1rem 1.5rem',
              marginBottom: '2rem',
              borderColor: 'rgba(239, 68, 68, 0.4)',
              background: 'rgba(30, 15, 15, 0.8)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              color: '#f87171',
            }}
          >
            <AlertTriangle size={20} />
            <span>{errorMsg}</span>
          </div>
        )}

        <WorkflowVisualizer planResponse={planResponse} isLoading={isLoading} />

        {planResponse && planResponse.status === 'waiting_for_approval' && (
          <HumanReviewModal
            sessionId={planResponse.session_id}
            onApprove={handleApprove}
            onEdit={handleEdit}
            onReject={handleReject}
            isLoading={isLoading}
          />
        )}

        {planResponse && <ResultsDashboard planResponse={planResponse} />}
      </main>
    </div>
  );
};
