'use client'

import { useState, useEffect } from 'react'
import { Clock, CheckCircle, XCircle, AlertCircle, TrendingUp, FileText } from 'lucide-react'
import { SoutenanceRequest } from '@/types/soutenance'
import { getStudentRequests, getDashboardData } from '@/services/api'
import { format } from 'date-fns'

interface DashboardHomeProps {
    onNavigate: (page: 'home' | 'upload' | 'history') => void
    requests: SoutenanceRequest[]
    setRequests: (requests: SoutenanceRequest[]) => void
}

export default function DashboardHome({ onNavigate, requests, setRequests }: DashboardHomeProps) {
    const [stats, setStats] = useState({ total: 0, pending: 0, accepted: 0, refused: 0 })
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true)
                const [requestsData, dashboardData] = await Promise.all([
                    getStudentRequests(),
                    getDashboardData().catch(() => null),
                ])
                setRequests(requestsData)

                if (dashboardData) {
                    setStats({
                        total: dashboardData.total,
                        pending: dashboardData.pending,
                        accepted: dashboardData.accepted,
                        refused: dashboardData.refused,
                    })
                } else {
                    setStats({
                        total: requestsData.length,
                        pending: requestsData.filter((r: SoutenanceRequest) => r.status === 'pending').length,
                        accepted: requestsData.filter((r: SoutenanceRequest) => r.status === 'accepted').length,
                        refused: requestsData.filter((r: SoutenanceRequest) => r.status === 'refused').length,
                    })
                }
            } catch (err) {
                console.error('Failed to fetch data:', err)
            } finally {
                setIsLoading(false)
            }
        }

        fetchData()
    }, [setRequests])

    const recentRequests = requests.slice(0, 3)

    return (
        <div className="space-y-8">
            {/* Welcome Section */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-8 text-white">
                <h2 className="text-3xl font-bold mb-2">Welcome to Your Dashboard</h2>
                <p className="text-blue-100 mb-6">Manage your thesis defense requests with AI-powered analysis</p>
                <button
                    onClick={() => onNavigate('upload')}
                    className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-flex items-center space-x-2"
                >
                    <FileText className="h-5 w-5" />
                    <span>Submit New Request</span>
                </button>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Total Requests</p>
                            <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total}</p>
                        </div>
                        <TrendingUp className="h-12 w-12 text-blue-500" />
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Pending</p>
                            <p className="text-3xl font-bold text-gray-900 mt-2">{stats.pending}</p>
                        </div>
                        <Clock className="h-12 w-12 text-yellow-500" />
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Accepted</p>
                            <p className="text-3xl font-bold text-gray-900 mt-2">{stats.accepted}</p>
                        </div>
                        <CheckCircle className="h-12 w-12 text-green-500" />
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Refused</p>
                            <p className="text-3xl font-bold text-gray-900 mt-2">{stats.refused}</p>
                        </div>
                        <XCircle className="h-12 w-12 text-red-500" />
                    </div>
                </div>
            </div>

            {/* Recent Requests */}
            <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-900">Recent Requests</h3>
                    <button
                        onClick={() => onNavigate('history')}
                        className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                    >
                        View All →
                    </button>
                </div>

                {isLoading ? (
                    <div className="p-12 text-center text-gray-500">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4">Loading...</p>
                    </div>
                ) : recentRequests.length === 0 ? (
                    <div className="p-12 text-center">
                        <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                        <h4 className="text-lg font-medium text-gray-900 mb-2">No requests yet</h4>
                        <p className="text-gray-500 mb-4">Get started by submitting your first request</p>
                        <button
                            onClick={() => onNavigate('upload')}
                            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Submit Request
                        </button>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-200">
                        {recentRequests.map((request) => (
                            <div key={request.id} className="p-6 hover:bg-gray-50 transition-colors">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <h4 className="font-semibold text-gray-900 mb-1">{request.title}</h4>
                                        <p className="text-sm text-gray-600">
                                            {format(new Date(request.createdAt), 'MMM dd, yyyy')}
                                        </p>
                                    </div>
                                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                        request.status === 'accepted' ? 'bg-green-100 text-green-800' :
                                            'bg-red-100 text-red-800'
                                        }`}>
                                        {request.status}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
