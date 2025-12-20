"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import StudentDashboard from "@/components/StudentDashboard";
import ProfessorDashboard from "@/components/professor/ProfessorDashboard";
import { useAuth } from "@/hooks/useAuth";

// Placeholder component for Manager role
const ManagerDashboard = () => <div className="p-8"><h1>Manager Dashboard</h1></div>;

function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Redirect unauthenticated users to welcome page
    if (!loading && !user) {
      router.push("/welcome");
    }
  }, [user, loading, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null; // Will redirect via useEffect
  }

  switch (user.role) {
    case "student":
      router.push("/student");
      return null;
    case "professor":
      router.push("/professor/dashboard");
      return null;
    case "manager":
      return <ManagerDashboard />;
    default:
      return <div>Unknown role</div>;
  }
}

export default Home;
