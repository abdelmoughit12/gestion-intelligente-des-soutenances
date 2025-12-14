import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

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
    return response.data
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to submit request')
    }
    throw new Error('Network error. Please check your connection.')
  }
}

export const getStudentRequests = async () => {
  try {
    const response = await api.get('/api/students/soutenance-requests')
    return response.data
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
    const response = await api.get('/api/defenses/')
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
    const response = await api.patch(`/api/defenses/${id}/`, { status });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to update defense status');
    }
    throw new Error('Network error. Please check your connection.');
  }
};

