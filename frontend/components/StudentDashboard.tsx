'use client'

import { useState } from 'react'
import { FileText, Plus, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import SoutenanceRequestForm from './SoutenanceRequestForm'
import RequestHistory from './RequestHistory'
import { SoutenanceRequest } from '@/types/soutenance'

export default function StudentDashboard() {
  const [showForm, setShowForm] = useState(false)
  const [requests, setRequests] = useState<SoutenanceRequest[]>([])

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

  const counts = getStatusCounts()

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
            <button
              onClick={() => setShowForm(!showForm)}
              className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Plus className="h-5 w-5" />
              <span>New Request</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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

