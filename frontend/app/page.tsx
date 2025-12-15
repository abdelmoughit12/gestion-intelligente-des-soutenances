'use client'

import { useState } from 'react'
import StudentDashboard from '@/components/StudentDashboard'
import ProfessorDashboardPage from './professor/dashboard/page'

export default function Home() {
  const [role, setRole] = useState<'student' | 'professor'>('professor') // Change for testing

  return role === 'student' ? <StudentDashboard /> : <ProfessorDashboardPage />
}


