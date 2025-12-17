// Frontend/components/professor/AssignedSoutenances.tsx
'use client'

import { useState } from 'react'
import { Search, Filter, Download, Eye, Edit, Loader2 } from 'lucide-react'
import { AssignedSoutenance } from '@/types/soutenance'
import SoutenanceDetailsModal from '@/components/professor/SoutenanceDetailsModal'
import { downloadReport } from '@/services/api'

interface Props {
  soutenances: AssignedSoutenance[]
  loading: boolean
}

export default function AssignedSoutenances({ soutenances, loading }: Props) {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [selectedSoutenance, setSelectedSoutenance] = useState<AssignedSoutenance | null>(null)
  const [downloadingId, setDownloadingId] = useState<number | null>(null)

  const handleDownload = async (soutenanceId: number) => {
    setDownloadingId(soutenanceId)
    try {
      const blob = await downloadReport(soutenanceId)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `report-soutenance-${soutenanceId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.parentNode?.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to download report:', error)
    } finally {
      setDownloadingId(null)
    }
  }
  
  const filtered = soutenances.filter(s => {
    const matchesSearch = 
      s.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.studentName.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesStatus = statusFilter === 'all' || s.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusBadge = (status: string) => {
    const statusConfig: any = {
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
    <div className="bg-white rounded-lg shadow w-full">
      {/* Search & Filter */}
      <div className="p-6 border-b w-full">
        <div className="flex flex-col md:flex-row gap-4 w-full">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by title or student..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-600"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-600 cursor-pointer">
            <option value="all" className="bg-gray-700 text-white">All Statuses</option>
            <option value="pending" className="bg-gray-700 text-white">Pending</option>
            <option value="scheduled" className="bg-gray-700 text-white">Scheduled</option>
            <option value="in_progress" className="bg-gray-700 text-white">In Progress</option>
            <option value="evaluated" className="bg-gray-700 text-white">Evaluated</option>
          </select>
        </div>
      </div>

      {/* List */}
      <div className="overflow-x-auto w-full">
        <table className="w-full min-w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Student</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Domain</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Scheduled</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                  No soutenances found
                </td>
              </tr>
            ) : (
              filtered.map(s => (
                <tr key={s.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">{s.title}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{s.studentName}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{s.domain}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {s.scheduledDate
                      ? `${new Date(s.scheduledDate).toLocaleDateString('fr-FR')} ${
                          s.scheduledTime || ''
                        }`
                      : 'N/A'}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium capitalize">
                      {s.juryRole}
                    </span>
                  </td>
                  <td className="px-7 py-4">{getStatusBadge(s.status)}</td>
                  <td className="px-7 py-4 flex gap-2">
                    <button
                      onClick={() => setSelectedSoutenance(s)}
                      className="p-2 text-primary-600 hover:bg-primary-50 rounded transition"
                      title="View details"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => setSelectedSoutenance(s)}
                      className="p-2 text-purple-600 hover:bg-purple-50 rounded transition"
                      title={s.status === 'evaluated' ? "Modifier l'évaluation" : "Évaluer"}
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDownload(s.id)}
                      disabled={downloadingId === s.id}
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded transition disabled:opacity-50 disabled:cursor-not-allowed"
                      title="Download report"
                    >
                      {downloadingId === s.id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Download className="h-4 w-4" />
                      )}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {selectedSoutenance && (
        <SoutenanceDetailsModal
          soutenance={selectedSoutenance}
          onClose={() => setSelectedSoutenance(null)}
        />
      )}
    </div>
  )
}