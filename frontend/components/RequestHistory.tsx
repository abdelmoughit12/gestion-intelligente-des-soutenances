'use client'

import { Clock, CheckCircle, XCircle, FileText, Calendar, Users } from 'lucide-react'
import { SoutenanceRequest } from '@/types/soutenance'
import { format } from 'date-fns'

interface RequestHistoryProps {
  requests: SoutenanceRequest[]
}

const getStatusIcon = (status: SoutenanceRequest['status']) => {
  switch (status) {
    case 'pending':
      return <Clock className="h-5 w-5 text-yellow-500" />
    case 'accepted':
      return <CheckCircle className="h-5 w-5 text-green-500" />
    case 'refused':
      return <XCircle className="h-5 w-5 text-red-500" />
  }
}

const getStatusBadge = (status: SoutenanceRequest['status']) => {
  const baseClasses = 'px-3 py-1 rounded-full text-xs font-medium'
  switch (status) {
    case 'pending':
      return `${baseClasses} bg-yellow-100 text-yellow-800`
    case 'accepted':
      return `${baseClasses} bg-green-100 text-green-800`
    case 'refused':
      return `${baseClasses} bg-red-100 text-red-800`
  }
}

export default function RequestHistory({ requests }: RequestHistoryProps) {
  if (requests.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center">
        <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No requests yet</h3>
        <p className="text-gray-500">Submit your first soutenance request to get started</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Request History</h2>
      </div>
      <div className="divide-y divide-gray-200">
        {requests.map((request) => (
          <div key={request.id} className="p-6 hover:bg-gray-50 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  {getStatusIcon(request.status)}
                  <h3 className="text-lg font-semibold text-gray-900">{request.title}</h3>
                </div>

                <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-gray-600">
                  <div className="flex items-center space-x-1">
                    <span className="font-medium">Domain:</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                      {request.domain}
                    </span>
                  </div>

                  <div className="flex items-center space-x-1">
                    <Calendar className="h-4 w-4" />
                    <span>
                      {format(new Date(request.createdAt), 'MMM dd, yyyy HH:mm')}
                    </span>
                  </div>

                  {request.scheduledDate && (
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-4 w-4" />
                      <span>
                        Scheduled: {format(new Date(request.scheduledDate), 'MMM dd, yyyy')}
                        {request.scheduledTime && ` at ${request.scheduledTime}`}
                      </span>
                    </div>
                  )}

                  {request.jury && request.jury.length > 0 && (
                    <div className="flex items-center space-x-1">
                      <Users className="h-4 w-4" />
                      <span>Jury: {request.jury.join(', ')}</span>
                    </div>
                  )}
                </div>

                {request.summary && (
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-700 mb-1">AI Summary:</p>
                    <p className="text-sm text-gray-600">{request.summary}</p>
                  </div>
                )}

                {request.similarityScore !== undefined && (
                  <div className="mt-3">
                    <p className="text-sm text-gray-600">
                      Similarity Score: <span className="font-medium">{request.similarityScore}%</span>
                    </p>
                  </div>
                )}

                {request.pdfUrl && (
                  <div className="mt-3">
                    <a
                      href={request.pdfUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 text-sm text-primary-600 hover:text-primary-700"
                    >
                      <FileText className="h-4 w-4" />
                      <span>View Report</span>
                    </a>
                  </div>
                )}
              </div>

              <div className="ml-4">
                <span className={getStatusBadge(request.status)}>
                  {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

