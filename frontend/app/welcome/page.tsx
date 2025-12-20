"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { UserRole } from "@/types/soutenance";

export default function WelcomePage() {
    const router = useRouter();
    const { user, loading } = useAuth();

    useEffect(() => {
        // If user is already logged in, redirect to appropriate dashboard
        if (!loading && user) {
            if (user.role === UserRole.Manager) {
                router.push("/dashboard");
            } else if (user.role === "student") {
                router.push("/student");
            } else if (user.role === "professor") {
                router.push("/professor/dashboard");
            } else {
                router.push("/");
            }
        }
    }, [user, loading, router]);

    if (loading) {
        return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
    }

    if (user) {
        return null; // Will redirect via useEffect
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <div className="w-full max-w-2xl p-12 space-y-8 bg-white rounded-2xl shadow-2xl">
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-bold text-gray-900">
                        Welcome to Soutenance Manager
                    </h1>
                    <p className="text-lg text-gray-600">
                        Manage thesis defenses efficiently and effectively
                    </p>
                </div>

                <div className="space-y-4 pt-8">
                    <button
                        onClick={() => router.push("/login")}
                        className="w-full px-6 py-4 text-lg font-semibold text-white bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                    >
                        Login
                    </button>

                    <button
                        onClick={() => router.push("/register")}
                        className="w-full px-6 py-4 text-lg font-semibold text-indigo-600 bg-white border-2 border-indigo-600 rounded-lg shadow-md hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                    >
                        Register
                    </button>
                </div>

                <div className="pt-6 text-center">
                    <p className="text-sm text-gray-500">
                        Streamline your academic defense management
                    </p>
                </div>
            </div>
        </div>
    );
}
