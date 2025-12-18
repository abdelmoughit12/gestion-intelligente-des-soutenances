
'use client'

import { useState, useEffect } from 'react'
import { FileText, Plus, Clock, CheckCircle, XCircle } from 'lucide-react'
import { useRouter } from 'next/navigation'
import SoutenanceRequestForm from './SoutenanceRequestForm'
import RequestHistory from './RequestHistory'
import { SoutenanceRequest } from '@/types/soutenance'
import { getStudentRequests } from '@/services/api'
import { logout } from '@/services/auth'

export default function StudentDashboard() {
  const [showForm, setShowForm] = useState(false)
  const [requests, setRequests] = useState<SoutenanceRequest[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  // Fetch requests on component mount
  useEffect(() => {
    const fetchRequests = async () => {
      try {
        setIsLoading(true)
        const data = await getStudentRequests()
        setRequests(data)
        setError(null)
      } catch (err: any) {
        console.error('Failed to fetch requests:', err)
        setError(err.message || 'Failed to load requests')
      } finally {
        setIsLoading(false)
      }
    }

    fetchRequests()
  }, [])

  const handleRequestSubmit = (newRequest: SoutenanceRequest) => {
    setRequests([newRequest, ...requests])
    setShowForm(false)
  }

  const getStatusCounts = () => {
    return {
      pending: requests.filter(r => r.status === 'pending').length,
      accepted: requests.filter(r => r.status === 'accepted').length,
      refused: requests.filter(r => r.status === 'refused').length,
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  const counts = getStatusCounts()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-8 w-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">Student Dashboard</h1>
            </div>
            <div>
              <button
                onClick={() => setShowForm(!showForm)}
                className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors mr-4"
              >
                <Plus className="h-5 w-5" />
                <span>New Request</span>
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
              >
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{counts.pending}</p>
              </div>
              <Clock className="h-12 w-12 text-yellow-500" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Accepted</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{counts.accepted}</p>
              </div>
              <CheckCircle className="h-12 w-12 text-green-500" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Refused</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{counts.refused}</p>
              </div>
              <XCircle className="h-12 w-12 text-red-500" />
            </div>
          </div>
        </div>

        {/* Request Form */}
        {showForm && (
          <div className="mb-8">
            <SoutenanceRequestForm
              onSubmit={handleRequestSubmit}
              onCancel={() => setShowForm(false)}
            />
          </div>
        )}

        {/* Request History */}
        <RequestHistory requests={requests} />
      </main>
    </div>
  )
}