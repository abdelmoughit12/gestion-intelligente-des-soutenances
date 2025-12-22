// frontend/app/professor/dashboard/page.tsx
'use client'

import { UnifiedSidebar } from '@/components/unified-sidebar'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import { SiteHeader } from '@/components/site-header'
import ProfessorDashboard from '@/components/professor/ProfessorDashboard'
import withAuth from '@/components/withAuth'
import { UserRole } from '@/types/soutenance'
import { useAuth } from '@/hooks/useAuth'

function ProfessorDashboardPage() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>; // Or a more sophisticated skeleton loader
  }

  // If user is null, withAuth on individual pages will redirect.
  // This layout won't render for unauthenticated users in practice.
  if (!user) {
    return null; 
  }

  return (
    <SidebarProvider>
      <UnifiedSidebar
        role={user.role}
        userName={`${user.first_name || ''} ${user.last_name || ''}`}
        userEmail={user.email}
        variant="inset"
      />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col bg-gray-50">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <main className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
              <ProfessorDashboard />
            </main>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}

export default withAuth(ProfessorDashboardPage, UserRole.Professor);