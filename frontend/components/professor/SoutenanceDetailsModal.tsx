// Frontend/components/professor/SoutenanceDetailsModal.tsx
'use client'

import { useState } from 'react'
import { X, Download, Mail } from 'lucide-react'
import { AssignedSoutenance } from '@/types/soutenance'
import { downloadReport } from '@/services/api'
import EvaluationForm from './EvaluationForm'

interface Props {
  soutenance: AssignedSoutenance
  onClose: () => void
}

export default function SoutenanceDetailsModal({ soutenance, onClose }: Props) {
  const [loading, setLoading] = useState(false)
  const [showEvaluation, setShowEvaluation] = useState(false)

  const handleDownloadReport = async () => {
    setLoading(true)
    try {
      const blob = await downloadReport(soutenance.id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report-${soutenance.id}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to download report:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    interface StatusConfig {
      bg: string
      text: string
      label: string
    }
    
    const statusConfig: Record<string, StatusConfig> = {
      pending: { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'Pending' },
      scheduled: { bg: 'bg-blue-100', text: 'text-blue-800', label: 'Scheduled' },
      in_progress: { bg: 'bg-purple-100', text: 'text-purple-800', label: 'In Progress' },
      evaluated: { bg: 'bg-green-100', text: 'text-green-800', label: 'Evaluated' },
    }
    const config = statusConfig[status] || statusConfig.pending
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${config.bg} ${config.text}`}>
        {config.label}
      </span>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b sticky top-0 bg-white">
          <h2 className="text-xl font-bold text-gray-900">{soutenance.title}</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status Badge */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-2">Status</label>
            {getStatusBadge(soutenance.status)}
          </div>

          {/* Student Info */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Student Name</p>
              <p className="text-lg text-gray-900">{soutenance.studentName}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Email</p>
              <p className="text-lg text-gray-900">{soutenance.studentEmail}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Domain</p>
              <p className="text-lg text-gray-900">{soutenance.domain}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Your Role</p>
              <p className="text-lg text-gray-900 capitalize">{soutenance.juryRole}</p>
            </div>
          </div>

          {/* Dates */}
          {(soutenance.scheduledDate || soutenance.scheduledTime) && (
            <div className="grid grid-cols-2 gap-4 bg-blue-50 p-4 rounded-lg">
              <div>
                <p className="text-sm font-medium text-gray-600">Scheduled Date</p>
                <p className="text-lg text-gray-900">
                  {soutenance.scheduledDate
                    ? new Date(soutenance.scheduledDate).toLocaleDateString('fr-FR')
                    : 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Scheduled Time</p>
                <p className="text-lg text-gray-900">{soutenance.scheduledTime || 'N/A'}</p>
              </div>
            </div>
          )}

          {/* AI Analysis */}
          {soutenance.aiSummary && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">AI Summary</h3>
              <p className="text-gray-700 text-sm">{soutenance.aiSummary}</p>
              <div className="mt-3 flex items-center justify-between">
                <span className="text-sm text-gray-600">Similarity Score:</span>
                <span className="text-lg font-semibold text-gray-900">
                  {soutenance.aiSimilarityScore}%
                </span>
              </div>
            </div>
          )}

          {/* Previous Evaluation */}
          {soutenance.evaluationScore !== undefined && (
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">Votre Évaluation Précédente</h3>
              <div className="grid grid-cols-2 gap-4 mb-3">
                <div>
                  <p className="text-sm font-medium text-gray-600">Note</p>
                  <p className="text-lg font-bold text-green-700">
                    {soutenance.evaluationScore}/20
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600">Date</p>
                  <p className="text-sm text-gray-700">
                    {soutenance.evaluationDate
                      ? new Date(soutenance.evaluationDate).toLocaleDateString('fr-FR')
                      : 'N/A'}
                  </p>
                </div>
              </div>
              {soutenance.evaluationComments && (
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Commentaires</p>
                  <p className="text-sm text-gray-700 bg-white p-2 rounded border border-green-200">
                    {soutenance.evaluationComments}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Evaluation Form - Toggle View */}
          {!showEvaluation ? (
            <div className="flex gap-3">
              <button
                onClick={() => setShowEvaluation(true)}
                className="flex items-center gap-2 flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition font-medium"
              >
                {soutenance.evaluationScore !== undefined ? '✏️ Modifier l\'évaluation' : '✍️ Évaluer cette Soutenance'}
              </button>
              <button
                onClick={handleDownloadReport}
                disabled={loading}
                className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 transition"
              >
                <Download className="h-4 w-4" />
                {loading ? 'Downloading...' : 'Download Report'}
              </button>
             <button
                onClick={() =>
                  window.open(
                    `https://mail.google.com/mail/?view=cm&fs=1&to=${soutenance.studentEmail}&su=Soutenance: ${encodeURIComponent(soutenance.title)}`,
                    '_blank'
                  )
                }
                className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-medium shadow-sm"
              >
                <Mail className="h-4 w-4" />
                Contacter l’étudiant
              </button>

            </div>
          ) : (
            <EvaluationForm
              soutenanceId={soutenance.id}
              studentName={soutenance.studentName}
              initialData={{
                score: soutenance.evaluationScore,
                comments: soutenance.evaluationComments,
              }}
              onSubmitSuccess={() => {
                setShowEvaluation(false)
                // Optional: refetch data or close modal
              }}
              onCancel={() => setShowEvaluation(false)}
            />
          )}
        </div>
      </div>
    </div>
  )
}