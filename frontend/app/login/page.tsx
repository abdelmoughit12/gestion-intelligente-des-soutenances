"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { login, getCurrentUser } from "@/services/auth";
import { useAuth } from "@/hooks/useAuth";
import { UserRole } from "@/types/soutenance";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user, loading } = useAuth();

  // Get redirect parameter from URL
  const redirectPath = searchParams.get("redirect");

  useEffect(() => {
    if (!loading && user) {
      // If user is already logged in, redirect based on redirect param or role
      if (redirectPath) {
        router.push(redirectPath);
      } else if (user.role === UserRole.Manager) {
        router.push("/dashboard");
      } else if (user.role === "student") {
        router.push("/student");
      } else if (user.role === "professor") {
        router.push("/professor/dashboard");
      } else {
        router.push("/");
      }
    }
  }, [user, loading, router, redirectPath]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      const loggedInUser = getCurrentUser();

      // Redirect to original route or default dashboard
      if (redirectPath) {
        router.push(redirectPath);
      } else if (loggedInUser && loggedInUser.role === UserRole.Manager) {
        router.push("/dashboard");
      } else if (loggedInUser && loggedInUser.role === "student") {
        router.push("/student");
      } else if (loggedInUser && loggedInUser.role === "professor") {
        router.push("/professor/dashboard");
      } else {
        router.push("/");
      }
    } catch (err: any) {
      // Display user-friendly error message from backend
      if (err.message) {
        setError(err.message);
      } else {
        setError("Login failed. Please try again.");
      }
    }
  };

  if (loading || user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">Login</h1>
        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="block w-full px-3 py-2 mt-1 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="block w-full px-3 py-2 mt-1 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
          </div>
          {error && (
            <div className="p-3 text-sm text-red-800 bg-red-100 border border-red-200 rounded-md">
              {error}
            </div>
          )}
          <div>
            <button
              type="submit"
              className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Sign in
            </button>
          </div>
        </form>

        <div className="text-center space-y-2">
          <p className="text-sm text-gray-600">
            Don't have an account?{" "}
            <button
              onClick={() => router.push("/register")}
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Register here
            </button>
          </p>
          <p className="text-sm text-gray-600">
            <button
              onClick={() => router.push("/welcome")}
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Back to Welcome
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
