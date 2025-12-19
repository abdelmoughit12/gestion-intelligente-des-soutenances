"use client";

import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { UserRole } from "@/types/soutenance"; // Assuming you have this type defined

// Define a role hierarchy for authorization
const roleHierarchy = {
  [UserRole.Student]: 1,
  [UserRole.Professor]: 2,
  [UserRole.Manager]: 3,
};

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
          // If authenticated, check for authorization
          const userLevel = roleHierarchy[user.role] || 0;
          const requiredLevel = roleHierarchy[minRequiredRole] || 0;

          if (userLevel < requiredLevel) {
            // If user's role is insufficient, redirect to an unauthorized page
            // It's good practice to have a dedicated page for this
            router.push("/unauthorized"); 
          }
        }
      }
    }, [user, loading, router, minRequiredRole]);

    // While loading, show a loading indicator
    if (loading) {
      return <div>Loading...</div>; // Or a more sophisticated skeleton loader
    }

    // If there's no user, return null to prevent rendering the component
    // before the redirect kicks in
    if (!user) {
      return null;
    }

    // Check role again before rendering to avoid flashing unauthorized content
    const userLevel = roleHierarchy[user.role] || 0;
    const requiredLevel = roleHierarchy[minRequiredRole] || 0;
    
    if (userLevel < requiredLevel) {
      // It's good to have a fallback here in case the redirect is slow
      return null; 
    }

    // If authenticated and authorized, render the wrapped component
    return <WrappedComponent {...props} />;
  };

  AuthComponent.displayName = `withAuth(${(WrappedComponent.displayName || WrappedComponent.name || 'Component')})`;

  return AuthComponent;
};

export default withAuth;
