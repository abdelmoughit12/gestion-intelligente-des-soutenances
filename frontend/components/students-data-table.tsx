"use client"

import * as React from "react"
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  useReactTable,
} from "@tanstack/react-table"
import { z } from "zod"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"

export const studentUserSchema = z.object({
  email: z.string().email(),
  first_name: z.string(),
  last_name: z.string(),
  id: z.number(),
  cni: z.string().nullable(),
  role: z.string(),
});

export const studentSchema = z.object({
  major: z.string(),
  cne: z.string(),
  year: z.number(),
  user: studentUserSchema,
});

  type Student = z.infer<typeof studentSchema>;

export const columns: ColumnDef<Student>[] = [
    {
        accessorKey: "fullName",
        header: "Full Name",
        cell: ({ row }) => `${row.original.user.first_name} ${row.original.user.last_name}`,
    },
    {
        accessorKey: "user.email",
        header: "Email",
    },
    {
        accessorKey: "cne",
        header: "CNE",
    },
    {
        accessorKey: "major",
        header: "Major",
    },
    {
        accessorKey: "year",
        header: "Year",
    },
];

interface StudentsDataTableProps {
  data: Student[];
}

export function StudentsDataTable({ data }: StudentsDataTableProps) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })

  return (
    <div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </Button>
      </div>
    </div>
  )
}
