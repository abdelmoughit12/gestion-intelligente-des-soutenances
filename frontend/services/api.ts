import axios from 'axios';
import { getToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor to add professor ID for testing
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const professorId = localStorage.getItem('professorId') || '1' // for testing
    config.headers['X-Professor-Id'] = professorId
  }
  return config
})

// Helper function to construct file URLs
const toFileUrl = (maybePath?: string | null) => {
  if (!maybePath) return ''
  if (maybePath.startsWith('http://') || maybePath.startsWith('https://')) return maybePath

  // In our new setup, the backend serves files from /reports/filename.ext
  // So we just need to combine the base URL with that path.
  const normalized = maybePath.replace(/^\/+/, '')
  const reportPath = normalized.startsWith('reports/') ? normalized : `reports/${normalized}`

  return `${API_BASE_URL}/${reportPath}`
}


export interface SubmitRequestResponse {
  id: string
  pdfUrl: string
  summary?: string
  similarityScore?: number
  domain?: string
}

export const submitSoutenanceRequest = async (
  formData: FormData
): Promise<SubmitRequestResponse> => {
  try {
    const response = await api.post('/api/v1/students/soutenance-requests', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return {
      id: response.data.id.toString(),
      pdfUrl: toFileUrl(response.data.report?.file_name),
      summary: response.data.report?.ai_summary,
      similarityScore: response.data.report?.ai_similarity_score,
      domain: response.data.report?.ai_domain,
    }
  } catch (error: any) {
    if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error') || !error.response) {
      throw new Error('Backend server is not running. Please start the backend API server at http://localhost:8000')
    }
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to submit request')
    }
    throw new Error('Network error. Please check your connection.')
  }
}

export const getStudentRequests = async () => {
  try {
    const response = await api.get('/api/v1/students/soutenance-requests')
    // Transform backend data to match frontend types
    return response.data.map((defense: any) => ({
      id: defense.id.toString(),
      title: defense.title,
      domain: defense.report?.ai_domain || 'Unknown',
      status: defense.status,
      pdfUrl: toFileUrl(defense.report?.file_name),
      summary: defense.report?.ai_summary,
      similarityScore: defense.report?.ai_similarity_score,
      createdAt: defense.report?.submission_date || new Date().toISOString(),
    }))
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch requests')
    }
    throw new Error('Network error. Please check your connection.')
  }
}

export interface StatsData {
  total_thesis_defenses: number;
  total_students: number;
  total_professors: number;
  thesis_defenses_by_status: {
    declined?: number;
    accepted?: number;
    pending?: number;
  };
  monthly_thesis_defenses: {
    month: string;
    count: number;
  }[];
}

export const getDashboardData = async (): Promise<StatsData> => {
  try {
    const response = await api.get('/api/v1/stats/');
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch dashboard data');
    }
    throw new Error('Network error. Please check your connection.');
  }
}

export const getProfessorAssignedSoutenances = async () => {
  try {
    const response = await api.get('/api/v1/professors/assigned-soutenances/')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch assigned soutenances')
  }
}

export const getSoutenanceDetail = async (defenseId: number) => {
  try {
    const response = await api.get(`/api/v1/professors/soutenances/${defenseId}/`)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch soutenance detail')
  }
}

export const downloadReport = async (defenseId: number) => {
  try {
    const response = await api.get(`/api/v1/professors/soutenances/${defenseId}/report/download/`, {
      responseType: 'blob'
    })
    return response.data
  } catch (error: any) {
    throw new Error('Failed to download report')
  }
}

export const getProfessorNotifications = async () => {
  try {
    const response = await api.get('/api/v1/professors/notifications/')
    return response.data
  } catch (error: any) {
    throw new Error('Failed to fetch notifications')
  }
}

export const markNotificationAsRead = async (notificationId: number) => {
  try {
    await api.patch(`/api/v1/professors/notifications/${notificationId}/read/`)
  } catch (error: any) {
    throw new Error('Failed to mark notification as read')
  }
}

export const submitEvaluation = async (
  soutenanceId: number,
  evaluationData: { score: number; comments: string }
) => {
  try {
    const response = await api.post(
      `/api/v1/professors/soutenances/${soutenanceId}/evaluation/`,
      evaluationData
    )
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to submit evaluation')
  }
}

export const getEvaluations = async () => {
  try {
    const response = await api.get('/api/v1/professors/evaluations/')
    return response.data
  } catch (error: any) {
    throw new Error('Failed to fetch evaluations')
  }
}

export const updateDefenseStatus = async (id: number, status: 'accepted' | 'declined') => {
  try {
    const response = await api.patch(`/api/v1/thesis-defenses/${id}/`, { status });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to update defense status');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
}

export interface Professor {
  user: User;
  specialty?: string;
}

export const getProfessors = async (): Promise<Professor[]> => {
  try {
    const response = await api.get('/api/v1/professors/');
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch professors');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export interface JurySuggestion {
  professor_id: number;
  name: string;
  reason: string;
}

export const getJurySuggestions = async (defenseId: number): Promise<JurySuggestion[]> => {
  try {
    const response = await api.get(`/api/v1/thesis-defenses/${defenseId}/jury-suggestions`);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch jury suggestions');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export interface UpdateDefensePayload {
  status?: 'accepted' | 'declined' | 'pending';
  defense_date?: string;
  defense_time?: string;
}

export const updateDefenseDetails = async (id: number, payload: UpdateDefensePayload) => {
  try {
    const response = await api.patch(`/api/v1/thesis-defenses/${id}/`, payload);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to update defense details');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

export interface JuryMemberCreatePayload {
  thesis_defense_id: number;
  professor_id: number;
  role: string;
}

export const assignJuryMember = async (defenseId: number, professorId: number, role: string) => {
  const payload: JuryMemberCreatePayload = {
    thesis_defense_id: defenseId,
    professor_id: professorId,
    role: role,
  };
  try {
    const response = await api.post(`/api/v1/thesis-defenses/${defenseId}/jury/`, payload);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 409) {
        return null;
      }
      let detail = error.response.data.detail;
      if (typeof detail === 'object' && detail !== null) {
        detail = JSON.stringify(detail);
      }
      throw new Error(detail || `Failed to assign professor ${professorId}`);
    }
    throw new Error('Network error. Please check your connection.');
  }
};
