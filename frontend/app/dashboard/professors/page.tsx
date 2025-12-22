"use client"

import React, { useEffect, useState } from 'react';
import { ProfessorsDataTable, professorSchema } from '@/components/professors-data-table';
import { z } from 'zod';
import { api } from '@/services/api';

type Professor = z.infer<typeof professorSchema>;

const ProfessorsPage = () => {
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfessors = async () => {
      try {
        const response = await api.get('/api/v1/manager/professors');
        const validatedData = z.array(professorSchema).parse(response.data);
        setProfessors(validatedData);
      } catch (e: any) {
        setError(e.response?.data?.detail || e.message);
        console.error("Failed to fetch professors:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchProfessors();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <h1 className="text-2xl font-bold mb-4">Professors</h1>
        <p>Loading professors...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-10">
        <h1 className="text-2xl font-bold mb-4">Professors</h1>
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-4">Professors</h1>
      <p className="mb-4">This page displays a list of all professors.</p>
      <ProfessorsDataTable data={professors} />
    </div>
  );
};

export default ProfessorsPage;
