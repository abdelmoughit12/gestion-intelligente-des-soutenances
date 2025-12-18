"use client"

import * as React from "react"
import Image from "next/image"
import {
    HomeIcon,
    LayoutDashboardIcon,
    ListIcon,
    UploadIcon,
    HistoryIcon,
    BellIcon,
    FileTextIcon,
    UsersIcon,
    CalendarIcon,
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavUser } from "@/components/nav-user"
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"

type UserRole = 'student' | 'professor' | 'manager'

interface UnifiedSidebarProps extends React.ComponentProps<typeof Sidebar> {
    role?: UserRole
    userName?: string
    userEmail?: string
}

const getRoleNavigation = (role: UserRole) => {
    switch (role) {
        case 'student':
            return [
                {
                    title: "Dashboard",
                    url: "/student",
                    icon: HomeIcon,
                },
                {
                    title: "New Request",
                    url: "/student?page=upload",
                    icon: UploadIcon,
                },
                {
                    title: "My Requests",
                    url: "/student?page=history",
                    icon: HistoryIcon,
                },
            ]
        case 'professor':
            return [
                {
                    title: "Dashboard",
                    url: "/professor/dashboard",
                    icon: HomeIcon,
                },
                {
                    title: "Assigned Defenses",
                    url: "/professor/dashboard?tab=assigned",
                    icon: FileTextIcon,
                },
                {
                    title: "Notifications",
                    url: "/professor/notifications",
                    icon: BellIcon,
                },
            ]
        case 'manager':
            return [
                {
                    title: "Dashboard",
                    url: "/dashboard",
                    icon: HomeIcon,
                },
                {
                    title: "Requests",
                    url: "/dashboard/requests",
                    icon: LayoutDashboardIcon,
                },
                {
                    title: "Soutenances",
                    url: "/dashboard/defenses",
                    icon: ListIcon,
                },
            ]
        default:
            return []
    }
}

const getRoleTitle = (role: UserRole) => {
    switch (role) {
        case 'student':
            return 'Student Portal'
        case 'professor':
            return 'Professor Space'
        case 'manager':
            return 'Manager Dashboard'
        default:
            return 'Portal'
    }
}

export function UnifiedSidebar({
    role = 'student',
    userName = 'User',
    userEmail = 'user@example.com',
    ...props
}: UnifiedSidebarProps) {
    const navItems = getRoleNavigation(role)
    const user = {
        name: userName,
        email: userEmail,
        avatar: "/avatars/shadcn.jpg",
    }

    return (
        <Sidebar collapsible="offcanvas" {...props}>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <div className="flex flex-col items-center justify-center w-full py-4 px-4">
                            <div className="w-24 h-24 relative mb-2">
                                <Image
                                    src="/images/logov2.svg"
                                    alt="Logo"
                                    width={96}
                                    height={96}
                                    className="object-contain"
                                />
                            </div>
                            <p className="text-sm font-medium text-muted-foreground text-center">
                                {getRoleTitle(role)}
                            </p>
                        </div>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                <NavMain items={navItems} />
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={user} />
            </SidebarFooter>
        </Sidebar>
    )
}
