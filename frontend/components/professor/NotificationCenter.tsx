// Frontend/components/professor/NotificationCenter.tsx
'use client'

import { useState, useEffect } from 'react'
import { Bell, X, CheckCircle } from 'lucide-react'
import { ProfessorNotification } from '@/types/soutenance'
import { getProfessorNotifications, markNotificationAsRead } from '@/services/api'
import { MOCK_PROFESSOR_NOTIFICATIONS } from '@/data/mockProfessorData'

export default function NotificationCenter() {
  const [notifications, setNotifications] = useState<ProfessorNotification[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        let data: ProfessorNotification[] = []
        
        // Essayer d'obtenir les données de l'API, sinon utiliser les données mock
        try {
          data = await getProfessorNotifications()
        } catch (apiError) {
          console.log('API not available, using mock notifications...')
          // Charger depuis localStorage ou utiliser mock
          const stored = localStorage.getItem('notifications')
          if (stored) {
            data = JSON.parse(stored)
          } else {
            data = MOCK_PROFESSOR_NOTIFICATIONS
            localStorage.setItem('notifications', JSON.stringify(data))
          }
        }
        
        setNotifications(data)
      } catch (error) {
        console.error('Failed to fetch notifications:', error)
        // Fallback to mock data on error
        setNotifications(MOCK_PROFESSOR_NOTIFICATIONS)
      } finally {
        setLoading(false)
      }
    }

    fetchNotifications()
    const interval = setInterval(fetchNotifications, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  const handleMarkAsRead = async (id: number) => {
    try {
      await markNotificationAsRead(id)
      setNotifications(notifications.map(n => 
        n.id === id ? { ...n, est_lue: true } : n
      ))
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
    }
  }

  const getNotificationIcon = (type: string) => {
    const icons: any = {
      'ASSIGNMENT': '📋',
      'ACCEPTANCE': '✅',
      'REFUSAL': '❌',
      'DATE_SCHEDULED': '📅',
    }
    return icons[type] || '📧'
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b flex items-center justify-between">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <Bell className="h-5 w-5 text-primary-600" />
          Notifications
        </h3>
      </div>

      <div className="divide-y max-h-[600px] overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-gray-500">Loading...</div>
        ) : notifications.length === 0 ? (
          <div className="p-4 text-center text-gray-500">No notifications</div>
        ) : (
          notifications.map(notif => (
            <div
              key={notif.id}
              className={`p-4 hover:bg-gray-50 transition-colors ${
                !notif.est_lue ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex gap-3">
                <span className="text-xl">{getNotificationIcon(notif.type_action)}</span>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{notif.message}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(notif.date_creation).toLocaleDateString()}
                  </p>
                </div>
                {!notif.est_lue && (
                  <button
                    onClick={() => handleMarkAsRead(notif.id)}
                    className="text-primary-600 hover:text-primary-700"
                  >
                    <CheckCircle className="h-5 w-5" />
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}