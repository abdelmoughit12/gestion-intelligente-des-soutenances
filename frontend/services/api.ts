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

export const getDashboardData = async () => {
  try {
    const response = await api.get('/api/students/dashboard')
    return response.data
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch dashboard data')
    }
    throw new Error('Network error. Please check your connection.')
  }
}

