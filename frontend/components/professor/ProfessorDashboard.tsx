// Frontend/components/professor/ProfessorDashboard.tsx
'use client'

import { useState, useEffect } from 'react'
import { Users, Clock, CheckCircle, FileText, Bell } from 'lucide-react'
import { AssignedSoutenance, ProfessorStats } from '@/types/soutenance'
import { getProfessorAssignedSoutenances } from '@/services/api'
import { MOCK_ASSIGNED_SOUTENANCES } from '@/data/mockProfessorData'
import AssignedSoutenances from '@/components/professor/AssignedSoutenanceCard'
import NotificationCenter from '@/components/professor/NotificationCenter'

export default function ProfessorDashboard() {
  const [soutenances, setSoutenances] = useState<AssignedSoutenance[]>([])
  const [stats, setStats] = useState<ProfessorStats>({
    assignedCount: 0,
    evaluatedCount: 0,
    pendingCount: 0,
    scheduledCount: 0,
  })
  const [loading, setLoading] = useState(true)
  const [showNotifications, setShowNotifications] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        let data: AssignedSoutenance[] = []
        
        // Essayer d'obtenir les données de l'API, sinon utiliser les données mock
        try {
          data = await getProfessorAssignedSoutenances()
        } catch (apiError) {
          console.log('API not available, using mock data...')
          data = MOCK_ASSIGNED_SOUTENANCES
        }
        
        setSoutenances(data)
        
        // Calculer les stats
        setStats({
          assignedCount: data.length,
          evaluatedCount: data.filter((s: any) => s.status === 'evaluated').length,
          pendingCount: data.filter((s: any) => s.status === 'pending').length,
          scheduledCount: data.filter((s: any) => s.status === 'scheduled').length,
        })
      } catch (error) {
        console.error('Failed to fetch soutenances:', error)
        // Fallback to mock data on error
        setSoutenances(MOCK_ASSIGNED_SOUTENANCES)
        setStats({
          assignedCount: MOCK_ASSIGNED_SOUTENANCES.length,
          evaluatedCount: MOCK_ASSIGNED_SOUTENANCES.filter(s => s.status === 'evaluated').length,
          pendingCount: MOCK_ASSIGNED_SOUTENANCES.filter(s => s.status === 'pending').length,
          scheduledCount: MOCK_ASSIGNED_SOUTENANCES.filter(s => s.status === 'scheduled').length,
        })
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Users className="h-8 w-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">Professor Dashboard</h1>
            </div>
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 text-gray-600 hover:text-gray-900"
            >
              <Bell className="h-6 w-6" />
              <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={<Users className="h-12 w-12 text-blue-500" />}
            label="Assigned"
            value={stats.assignedCount}
            color="blue"
          />
          <StatCard
            icon={<Clock className="h-12 w-12 text-yellow-500" />}
            label="Pending"
            value={stats.pendingCount}
            color="yellow"
          />
          <StatCard
            icon={<FileText className="h-12 w-12 text-purple-500" />}
            label="Scheduled"
            value={stats.scheduledCount}
            color="purple"
          />
          <StatCard
            icon={<CheckCircle className="h-12 w-12 text-green-500" />}
            label="Evaluated"
            value={stats.evaluatedCount}
            color="green"
          />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className={showNotifications ? "lg:col-span-3" : "lg:col-span-4"}>
            <AssignedSoutenances soutenances={soutenances} loading={loading} />
          </div>
          {showNotifications && (
            <div className="lg:col-span-1">
              <NotificationCenter />
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

// Composant Stats Card réutilisable
function StatCard({ icon, label, value, color }: any) {
  const borderColors: any = {
    blue: 'border-blue-500',
    yellow: 'border-yellow-500',
    purple: 'border-purple-500',
    green: 'border-green-500',
  }

  return (
    <div className={`bg-white rounded-lg shadow p-6 border-l-4 ${borderColors[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{label}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        {icon}
      </div>
    </div>
  )
}