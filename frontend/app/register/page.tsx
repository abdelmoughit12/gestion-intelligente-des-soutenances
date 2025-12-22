"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { StudentRegistration, registerStudent } from "@/services/auth";

export default function RegisterPage() {
    const router = useRouter();
    const [formData, setFormData] = useState<StudentRegistration>({
        first_name: "",
        last_name: "",
        cni: "",
        cne: "",
        email: "",
        phone: "",
        password: "",
    });
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await registerStudent(formData);
            setSuccess(true);
        } catch (err: any) {
            setError(err.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <div className="w-full max-w-md p-8 space-y-6 text-center bg-white rounded-lg shadow-md">
                    <h1 className="text-2xl font-bold text-green-600">Registration Successful!</h1>
                    <p className="text-gray-700">
                        Your account has been created and is now pending approval from an administrator.
                    </p>
                    <Button onClick={() => router.push("/login")} className="w-full">
                        Return to Login
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
                <h1 className="text-2xl font-bold text-center text-gray-900">Student Registration</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <Label htmlFor="first_name">First Name</Label>
                            <Input id="first_name" type="text" value={formData.first_name} onChange={handleChange} required />
                        </div>
                        <div>
                            <Label htmlFor="last_name">Last Name</Label>
                            <Input id="last_name" type="text" value={formData.last_name} onChange={handleChange} required />
                        </div>
                    </div>
                     <div>
                        <Label htmlFor="cni">CNI (National ID)</Label>
                        <Input id="cni" type="text" value={formData.cni} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="cne">CNE (Student ID)</Label>
                        <Input id="cne" type="text" value={formData.cne} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" type="email" value={formData.email} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input id="phone" type="tel" value={formData.phone} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="password">Password</Label>
                        <Input id="password" type="password" value={formData.password} onChange={handleChange} required />
                    </div>

                    {error && <p className="text-sm text-red-600">{error}</p>}

                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? "Registering..." : "Register"}
                    </Button>
                     <Button variant="outline" type="button" className="w-full" onClick={() => router.push('/login')}>
                        Back to Login
                    </Button>
                </form>
            </div>
        </div>
    );
}
