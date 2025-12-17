import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

const toFileUrl = (maybePath?: string | null) => {
  if (!maybePath) return ''
  if (maybePath.startsWith('http://') || maybePath.startsWith('https://')) return maybePath
  const normalized = maybePath.replace(/^\/+/, '')
  return `${API_BASE_URL}/${normalized}`
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
    const response = await api.post('/api/students/soutenance-requests', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    // Transform backend response to match frontend expectations
    return {
      id: response.data.id.toString(),
      pdfUrl: toFileUrl(response.data.report?.file_name),
      summary: response.data.report?.ai_summary,
      similarityScore: response.data.report?.ai_similarity_score,
      domain: response.data.report?.ai_domain,
    }
  } catch (error: any) {
    // Check if it's a network/connection error (backend not running)
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
    const response = await api.get('/api/students/soutenance-requests')
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

// Define the new interface for the stats data
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
    const response = await api.get('/api/stats/'); // Change endpoint
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch dashboard data');
    }
    throw new Error('Network error. Please check your connection.');
  }
}

export const getDefenses = async () => {
  try {
    const response = await api.get('/api/v1/defenses/')
    return response.data
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch defenses')
    }
    throw new Error('Network error. Please check your connection.')
  }
}

export const updateDefenseStatus = async (id: number, status: 'accepted' | 'declined') => {
  try {
    const response = await api.patch(`/api/v1/defenses/${id}/`, { status });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to update defense status');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

// Define an interface for Professor data
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

export interface UpdateDefensePayload {
  status?: 'accepted' | 'declined' | 'pending';
  defense_date?: string;
  defense_time?: string;
}

export const updateDefenseDetails = async (id: number, payload: UpdateDefensePayload) => {
  try {
    const response = await api.patch(`/api/v1/defenses/${id}/`, payload);
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
    const response = await api.post(`/api/v1/defenses/${defenseId}/jury`, payload);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      // Don't throw for 409 conflict, it means the assignment already exists.
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
