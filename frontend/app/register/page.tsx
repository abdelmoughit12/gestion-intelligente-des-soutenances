"use client";

import { useRouter } from "next/navigation";

export default function RegisterPage() {
    const router = useRouter();

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
                <h1 className="text-2xl font-bold text-center text-gray-900">Registration</h1>

                <div className="space-y-4 text-center">
                    <div className="p-6 bg-blue-50 rounded-lg">
                        <p className="text-gray-700">
                            Registration functionality is coming soon.
                        </p>
                        <p className="mt-2 text-sm text-gray-600">
                            Please contact your administrator to create an account.
                        </p>
                    </div>

                    <button
                        onClick={() => router.push("/login")}
                        className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Back to Login
                    </button>

                    <button
                        onClick={() => router.push("/welcome")}
                        className="w-full px-4 py-2 text-sm font-medium text-indigo-600 bg-white border border-indigo-600 rounded-md shadow-sm hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Back to Welcome
                    </button>
                </div>
            </div>
        </div>
    );
}
