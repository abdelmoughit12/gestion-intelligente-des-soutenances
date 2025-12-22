"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { addProfessor, ProfessorCreateData } from "@/services/manager";
import { toast } from "sonner";
import withAuth from "@/components/withAuth";
import { UserRole } from "@/types/soutenance";

function AddProfessorPage() {
    const [formData, setFormData] = useState<ProfessorCreateData>({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        specialty: "",
    });
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        toast.info("Adding professor...");
        try {
            await addProfessor(formData);
            toast.success("Professor added successfully!");
            // Reset form
            setFormData({
                first_name: "",
                last_name: "",
                email: "",
                phone: "",
                password: "",
                specialty: "",
            });
        } catch (err: any) {
            toast.error(err.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">Add New Professor</h1>
            <div className="w-full max-w-2xl p-8 space-y-6 bg-white rounded-lg shadow-md">
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
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" type="email" value={formData.email} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input id="phone" type="tel" value={formData.phone} onChange={handleChange} required />
                    </div>
                     <div>
                        <Label htmlFor="specialty">Specialty / Domain</Label>
                        <Input id="specialty" type="text" value={formData.specialty} onChange={handleChange} required />
                    </div>
                    <div>
                        <Label htmlFor="password">Password</Label>
                        <Input id="password" type="password" value={formData.password} onChange={handleChange} required />
                        <p className="text-sm text-muted-foreground mt-1">
                            The professor can change this password later.
                        </p>
                    </div>

                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? "Adding..." : "Add Professor"}
                    </Button>
                </form>
            </div>
        </div>
    );
}

export default withAuth(AddProfessorPage, UserRole.Manager);
