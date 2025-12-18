'use client'

import { useState } from 'react'
import { FileText, Home, Upload, History, Settings } from 'lucide-react'
import DashboardHome from './DashboardHome'
import SoutenanceRequestForm from './SoutenanceRequestForm'
import RequestHistory from './RequestHistory'
import { SoutenanceRequest } from '@/types/soutenance'

type Page = 'home' | 'upload' | 'history'

export default function MultiPageDashboard() {
    const [currentPage, setCurrentPage] = useState<Page>('home')
    const [requests, setRequests] = useState<SoutenanceRequest[]>([])

    const handleRequestSubmit = (newRequest: SoutenanceRequest) => {
        setRequests([newRequest, ...requests])
        setCurrentPage('history')
    }

    const navigation = [
        { id: 'home' as Page, label: 'Home', icon: Home },
        { id: 'upload' as Page, label: 'New Request', icon: Upload },
        { id: 'history' as Page, label: 'My Requests', icon: History },
    ]

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center space-x-3">
                            <FileText className="h-8 w-8 text-blue-600" />
                            <h1 className="text-xl font-bold text-gray-900">Student Portal</h1>
                        </div>

                        {/* Navigation */}
                        <nav className="flex space-x-2">
                            {navigation.map((item) => {
                                const Icon = item.icon
                                const isActive = currentPage === item.id
                                return (
                                    <button
                                        key={item.id}
                                        onClick={() => setCurrentPage(item.id)}
                                        className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${isActive
                                                ? 'bg-blue-600 text-white'
                                                : 'text-gray-700 hover:bg-gray-100'
                                            }`}
                                    >
                                        <Icon className="h-5 w-5" />
                                        <span className="hidden sm:inline">{item.label}</span>
                                    </button>
                                )
                            })}
                        </nav>
                    </div>
                </div>
            </header>

            {/* Page Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {currentPage === 'home' && (
                    <DashboardHome
                        onNavigate={setCurrentPage}
                        requests={requests}
                        setRequests={setRequests}
                    />
                )}

                {currentPage === 'upload' && (
                    <div>
                        <div className="mb-6">
                            <h2 className="text-2xl font-bold text-gray-900">Submit New Request</h2>
                            <p className="text-gray-600 mt-1">Upload your thesis report and request a defense</p>
                        </div>
                        <SoutenanceRequestForm
                            onSubmit={handleRequestSubmit}
                            onCancel={() => setCurrentPage('home')}
                        />
                    </div>
                )}

                {currentPage === 'history' && (
                    <div>
                        <div className="mb-6">
                            <h2 className="text-2xl font-bold text-gray-900">My Requests</h2>
                            <p className="text-gray-600 mt-1">Track your submitted defense requests</p>
                        </div>
                        <RequestHistory requests={requests} />
                    </div>
                )}
            </main>
        </div>
    )
}
