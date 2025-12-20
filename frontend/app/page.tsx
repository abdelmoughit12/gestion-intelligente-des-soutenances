"use client";

import StudentDashboard from "@/components/StudentDashboard";
import ProfessorDashboard from "@/components/professor/ProfessorDashboard";
import withAuth from "@/components/withAuth";
import { useAuth } from "@/hooks/useAuth";

// Placeholder component for Manager role
const ManagerDashboard = () => <div className="p-8"><h1>Manager Dashboard</h1></div>;

function Home() {
  const { user } = useAuth();

  if (!user) {
    return <div>Loading...</div>;
  }

  switch (user.role) {
    case "student":
      return <StudentDashboard />;
    case "professor":
      return <ProfessorDashboard />;
    case "manager":
      return <ManagerDashboard />;
    default:
      return <div>Unknown role</div>;
  }
}

export default withAuth(Home);
