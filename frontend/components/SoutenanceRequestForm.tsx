'use client'

import { useState } from 'react'
import { X, Upload, FileText } from 'lucide-react'
import PDFUpload from './PDFUpload'
import { RequestFormData, SoutenanceRequest, Domain } from '@/types/soutenance'
import { submitSoutenanceRequest } from '@/services/api'

interface SoutenanceRequestFormProps {
  onSubmit: (request: SoutenanceRequest) => void
  onCancel: () => void
}

const DOMAINS: Domain[] = ['Web', 'AI', 'IoT', 'Mobile', 'Security', 'Data Science', 'Other']

export default function SoutenanceRequestForm({ onSubmit, onCancel }: SoutenanceRequestFormProps) {
  const [formData, setFormData] = useState<RequestFormData>({
    title: '',
    domain: 'Web',
    pdfFile: null,
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!formData.title.trim()) {
      setError('Please enter a title for your soutenance request')
      return
    }

    if (!formData.pdfFile) {
      setError('Please upload your report PDF')
      return
    }

    setIsSubmitting(true)

    try {
      // Create form data for file upload
      const uploadFormData = new FormData()
      uploadFormData.append('title', formData.title)
      uploadFormData.append('domain', formData.domain)
      uploadFormData.append('pdf', formData.pdfFile)

      // Submit to backend
      const response = await submitSoutenanceRequest(uploadFormData)

      // Create request object for local state
      const newRequest: SoutenanceRequest = {
        id: response.id || Date.now().toString(),
        title: formData.title,
        domain: formData.domain,
        status: 'pending',
        pdfUrl: response.pdfUrl,
        summary: response.summary,
        similarityScore: response.similarityScore,
        createdAt: new Date().toISOString(),
      }

      onSubmit(newRequest)

      // Reset form
      setFormData({
        title: '',
        domain: 'Web',
        pdfFile: null,
      })
    } catch (err: any) {
      setError(err.message || 'Failed to submit request. Please try again.')
      console.error('Error submitting request:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleFileSelect = (file: File) => {
    setFormData({ ...formData, pdfFile: file })
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">New Soutenance Request</h2>
        <button
          onClick={onCancel}
          className="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="h-6 w-6" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title Input */}
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Title <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            placeholder="e.g., E-commerce Platform with AI Recommendations"
            required
          />
        </div>

        {/* Domain Selection */}
        <div>
          <label htmlFor="domain" className="block text-sm font-medium text-gray-700 mb-2">
            Domain <span className="text-red-500">*</span>
          </label>
          <select
            id="domain"
            value={formData.domain}
            onChange={(e) => setFormData({ ...formData, domain: e.target.value as Domain })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            {DOMAINS.map((domain) => (
              <option key={domain} value={domain}>
                {domain}
              </option>
            ))}
          </select>
        </div>

        {/* PDF Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Report PDF <span className="text-red-500">*</span>
          </label>
          <PDFUpload onFileSelect={handleFileSelect} selectedFile={formData.pdfFile} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Submit Buttons */}
        <div className="flex items-center justify-end space-x-4 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Submitting...</span>
              </>
            ) : (
              <>
                <Upload className="h-4 w-4" />
                <span>Submit Request</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

