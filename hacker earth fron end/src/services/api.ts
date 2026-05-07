import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 60000,
});

export type BackendResponse = {
  status?: string;
  request_id?: string;
  processing_mode?: string;
  analytics?: Record<string, unknown>;
  dashboard?: Record<string, any>;
  data?: Record<string, any>;
  errors?: string[];
  frontend_adapted?: Record<string, any>;
  decision_intelligence?: Record<string, any>;
  ui_recommended_actions?: any[];
  ui_decision_reasoning?: string | string[];
  ui_appeal_suggestion?: string;
  confidence_score?: number;
  verification_required?: boolean;
  document_quality?: string;
  warning?: string;
  original_language?: string;
  translated_text_used?: boolean;
  ui_deadlines?: any[];
  ui_cards?: any[];
  ui_tags?: any[];
  ui_risk_meter?: any;
  ui_heat_score?: any;
};

const ANALYSIS_KEY = 'nyaya_saarathi_latest_analysis';

export const saveLatestAnalysis = (payload: BackendResponse) => {
  sessionStorage.setItem(ANALYSIS_KEY, JSON.stringify(payload));
};

export const getLatestAnalysis = (): BackendResponse | null => {
  const raw = sessionStorage.getItem(ANALYSIS_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw) as BackendResponse;
  } catch {
    sessionStorage.removeItem(ANALYSIS_KEY);
    return null;
  }
};

export const healthCheck = () => api.get('/health');

export const processJudgment = (data: FormData, mockMode = false) => 
  api.post(`/upload?mock_mode=${mockMode}`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

export const fetchDemoAnalysis = () => api.get('/demo-test');

export const uploadJudgmentWithFallback = async (file: File, mockMode = false) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await processJudgment(formData, mockMode);
    const payload = response.data as BackendResponse;
    if (!payload || typeof payload !== 'object') throw new Error('Empty analysis response');
    saveLatestAnalysis(payload);
    return { payload, usedFallback: false };
  } catch (error) {
    const response = await fetchDemoAnalysis();
    const payload = response.data as BackendResponse;
    saveLatestAnalysis(payload);
    return { payload, usedFallback: true, error };
  }
};

export default api;
