"use client";

import { useEffect, useState } from "react";
import {
  approveStudent,
  getPendingStudents,
  PendingStudent,
  rejectStudent,
} from "@/services/manager";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";
import { Badge } from "@/components/ui/badge";
import withAuth from "@/components/withAuth";
import { UserRole } from "@/types/soutenance";

function StudentRequestsTable({
  students,
  onApprove,
  onReject,
}: {
  students: PendingStudent[];
  onApprove: (id: number) => void;
  onReject: (id: number) => void;
}) {
  return (
    <div className="border rounded-lg w-full">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>CNI</TableHead>
            <TableHead>Phone</TableHead>
            <TableHead>Registration Date</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {students.length > 0 ? (
            students.map((student) => (
              <TableRow key={student.id}>
                <TableCell>{`${student.first_name} ${student.last_name}`}</TableCell>
                <TableCell>{student.email}</TableCell>
                <TableCell>{student.cni}</TableCell>
                <TableCell>{student.phone}</TableCell>
                <TableCell>
                  {new Date(student.creation_date).toLocaleDateString()}
                </TableCell>
                <TableCell className="text-right space-x-2">
                  <Button
                    size="sm"
                    variant="outline"
                    className="border-green-500 text-green-500 hover:bg-green-500 hover:text-white"
                    onClick={() => onApprove(student.id)}
                  >
                    Approve
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                    onClick={() => onReject(student.id)}
                  >
                    Reject
                  </Button>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={6} className="h-24 text-center">
                No pending requests.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}

function ManagerRequestsPage() {
  const [pendingStudents, setPendingStudents] = useState<PendingStudent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = async () => {
    setLoading(true);
    try {
      const students = await getPendingStudents();
      setPendingStudents(students);
    } catch (err: any) {
      setError(err.message);
      toast.error("Failed to load pending requests.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleApprove = async (id: number) => {
    toast.info("Approving student...");
    try {
      await approveStudent(id);
      toast.success("Student approved successfully!");
      fetchStudents(); // Refresh the list
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  const handleReject = async (id: number) => {
    toast.info("Rejecting student...");
    try {
      await rejectStudent(id);
      toast.success("Student rejected successfully.");
      fetchStudents(); // Refresh the list
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Student Registration Requests</h1>
        <Badge>{pendingStudents.length} Pending</Badge>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && (
        <StudentRequestsTable
          students={pendingStudents}
          onApprove={handleApprove}
          onReject={handleReject}
        />
      )}
    </div>
  );
}

export default withAuth(ManagerRequestsPage, UserRole.Manager);
