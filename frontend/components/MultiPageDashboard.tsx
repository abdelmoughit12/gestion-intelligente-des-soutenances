'use client'

import { useState, useEffect } from 'react'
import { UnifiedSidebar } from './unified-sidebar'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import { SiteHeader } from '@/components/site-header'
import DashboardHome from './DashboardHome'
import SoutenanceRequestForm from './SoutenanceRequestForm'
import RequestHistory from './RequestHistory'
import { SoutenanceRequest } from '@/types/soutenance'

type Page = 'home' | 'upload' | 'history'

export default function MultiPageDashboard() {
    const [currentPage, setCurrentPage] = useState<Page>('home')
    const [requests, setRequests] = useState<SoutenanceRequest[]>([])

    // Handle URL-based navigation
    useEffect(() => {
        const params = new URLSearchParams(window.location.search)
        const page = params.get('page') as Page
        if (page && ['home', 'upload', 'history'].includes(page)) {
            setCurrentPage(page)
        }
    }, [])

    const handleNavigate = (page: Page) => {
        setCurrentPage(page)
        const url = new URL(window.location.href)
        url.searchParams.set('page', page)
        window.history.pushState({}, '', url)
    }

    const handleRequestSubmit = (newRequest: SoutenanceRequest) => {
        setRequests([newRequest, ...requests])
        handleNavigate('history')
    }

    return (
        <SidebarProvider>
            <UnifiedSidebar 
                role="student" 
                userName="Test Student"
                userEmail="student@example.com"
                variant="inset" 
            />
            <SidebarInset>
                <SiteHeader />
                <div className="flex flex-1 flex-col bg-gray-50">
                    <div className="@container/main flex flex-1 flex-col gap-2">
                        <main className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
                            {currentPage === 'home' && (
                                <DashboardHome
                                    onNavigate={handleNavigate}
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
                                        onCancel={() => handleNavigate('home')}
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
                </div>
            </SidebarInset>
        </SidebarProvider>
    )
}
