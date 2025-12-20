'use client'

import MultiPageDashboard from '@/components/MultiPageDashboard'
import withAuth from '@/components/withAuth'
import { UserRole } from '@/types/soutenance';

function StudentPage() {
    return <MultiPageDashboard />
}

export default withAuth(StudentPage, UserRole.Student);
