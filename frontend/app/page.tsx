"use client";

import StudentDashboard from "@/components/StudentDashboard";
import withAuth from "@/components/withAuth";
import { useAuth } from "@/hooks/useAuth";

// Placeholder components for other roles
const ProfessorDashboard = () => <div className="p-8"><h1>Professor Dashboard</h1></div>;
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


