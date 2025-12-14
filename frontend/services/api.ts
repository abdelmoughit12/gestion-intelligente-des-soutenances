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

    // Transform backend response to match frontend expectations
    return {
      id: response.data.id.toString(),
      pdfUrl: response.data.report?.file_name || '',
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
      pdfUrl: defense.report?.file_name,
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

