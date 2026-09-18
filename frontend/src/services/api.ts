import { PlanResponse, SessionDetail } from '../types/travel';

const BASE_URL = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace(/\/$/, '') : '';
const API_BASE = `${BASE_URL}/api/v1/travel`;

export async function submitTravelPlan(userQuery: string, sessionId?: string): Promise<PlanResponse> {
  const response = await fetch(`${API_BASE}/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_query: userQuery, session_id: sessionId }),
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to generate travel plan');
  }
  return response.json();
}

export async function getSessionDetails(sessionId: string): Promise<SessionDetail> {
  const response = await fetch(`${API_BASE}/${sessionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch session details');
  }
  return response.json();
}

export async function approvePlan(sessionId: string, feedback: string = ''): Promise<PlanResponse> {
  const response = await fetch(`${API_BASE}/${sessionId}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ feedback }),
  });
  if (!response.ok) {
    throw new Error('Failed to approve plan');
  }
  return response.json();
}

export async function editPlan(sessionId: string, feedback: string): Promise<PlanResponse> {
  const response = await fetch(`${API_BASE}/${sessionId}/edit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ feedback }),
  });
  if (!response.ok) {
    throw new Error('Failed to submit plan edits');
  }
  return response.json();
}

export async function rejectPlan(sessionId: string, feedback: string = ''): Promise<PlanResponse> {
  const response = await fetch(`${API_BASE}/${sessionId}/reject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ feedback }),
  });
  if (!response.ok) {
    throw new Error('Failed to reject plan');
  }
  return response.json();
}
