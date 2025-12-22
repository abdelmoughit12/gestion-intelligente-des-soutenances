"use client";

import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { UserRole } from "@/types/soutenance";

// Define a role hierarchy for authorization
const roleHierarchy: Record<UserRole, number> = {
  [UserRole.Student]: 1,
  [UserRole.Professor]: 2,
  [UserRole.Manager]: 3,
};

// Function to get the dashboard route for a given role
const getDashboardRoute = (role: UserRole): string => {
  switch (role) {
    case UserRole.Student:
      return "/student";
    case UserRole.Professor:
      return "/professor/dashboard";
    case UserRole.Manager:
      return "/dashboard";
    default:
      return "/login"; // Fallback
  }
};

// ... (imports and roleHierarchy remain the same)

const withAuth = (
  WrappedComponent,
  minRequiredRole: UserRole = UserRole.Student
) => {
  const AuthComponent = (props) => {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!loading) {
        if (!user) {
          // If not authenticated, redirect to login
          router.push("/login");
        } else {
          // If authenticated, check for exact role match
          if (user.role !== minRequiredRole) {
            // If user's role is not the exact required role, redirect to their own dashboard
            const userDashboard = getDashboardRoute(user.role as UserRole);
            router.push(userDashboard);
          }
        }
      }
    }, [user, loading, router, minRequiredRole]);

    if (loading || !user) {
      return <div>Loading...</div>;
    }
    
    // Final check before rendering to avoid content flashing
    if (user.role !== minRequiredRole) {
        return null;
    }

    return <WrappedComponent {...props} />;
  };

  AuthComponent.displayName = `withAuth(${(WrappedComponent.displayName || WrappedComponent.name || 'Component')})`;

  return AuthComponent;
};

export default withAuth;

