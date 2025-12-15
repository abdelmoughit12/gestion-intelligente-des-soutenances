import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor pour ajouter X-Professor-Id (pour test/développement)
api.interceptors.request.use((config) => {
  // Récupérer l'ID du prof depuis localStorage ou session
  const professorId = localStorage.getItem('professorId') || '1' // Default: 1 pour test
  config.headers['X-Professor-Id'] = professorId
  return config
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

/////////////////////////////////////////

// Ajouter ces fonctions
export const getProfessorAssignedSoutenances = async () => {
  try {
    const response = await api.get('/api/professors/assigned-soutenances')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch assigned soutenances')
  }
}

export const getSoutenanceDetail = async (defenseId: number) => {
  try {
    const response = await api.get(`/api/professors/soutenances/${defenseId}`)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch soutenance detail')
  }
}

export const downloadReport = async (defenseId: number) => {
  try {
    const response = await api.get(`/api/professors/soutenances/${defenseId}/report/download`, {
      responseType: 'blob'
    })
    return response.data
  } catch (error: any) {
    throw new Error('Failed to download report')
  }
}

export const getProfessorNotifications = async () => {
  try {
    const response = await api.get('/api/professors/notifications')
    return response.data
  } catch (error: any) {
    throw new Error('Failed to fetch notifications')
  }
}

export const markNotificationAsRead = async (notificationId: number) => {
  try {
    await api.patch(`/api/professors/notifications/${notificationId}/read`)
  } catch (error: any) {
    throw new Error('Failed to mark notification as read')
  }
}

// Évaluation des soutenances
export const submitEvaluation = async (
  soutenanceId: number,
  evaluationData: { score: number; comments: string }
) => {
  try {
    const response = await api.post(
      `/api/professors/soutenances/${soutenanceId}/evaluation`,
      evaluationData
    )
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to submit evaluation')
  }
}

export const getEvaluations = async () => {
  try {
    const response = await api.get('/api/professors/evaluations')
    return response.data
  } catch (error: any) {
    throw new Error('Failed to fetch evaluations')
  }
}
