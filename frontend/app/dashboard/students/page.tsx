"use client"

import React, { useEffect, useState } from 'react';
import { StudentsDataTable, studentSchema } from '@/components/students-data-table';
import { z } from 'zod';

type Student = z.infer<typeof studentSchema>;

const StudentsPage = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/students/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const validatedData = z.array(studentSchema).parse(data);
        setStudents(validatedData);
      } catch (e: any) {
        setError(e.message);
        console.error("Failed to fetch students:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <h1 className="text-2xl font-bold mb-4">Students</h1>
        <p>Loading students...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-10">
        <h1 className="text-2xl font-bold mb-4">Students</h1>
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-4">Students</h1>
      <p className="mb-4">This page displays a list of all students.</p>
      <StudentsDataTable data={students} />
    </div>
  );
};

export default StudentsPage;
