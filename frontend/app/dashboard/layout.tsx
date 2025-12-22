"use client";

import * as React from "react";
import { UnifiedSidebar } from "@/components/unified-sidebar";
import { SiteHeader } from "@/components/site-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { useAuth } from "@/hooks/useAuth";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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
            {children}
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
