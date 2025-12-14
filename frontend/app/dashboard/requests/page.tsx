"use client";

import { useEffect, useState } from "react";
import { DataTable } from "@/components/data-table";
import { z } from "zod";
import { schema } from "@/components/data-table";

export default function Page() {
  const [data, setData] = useState<z.infer<typeof schema>[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/defenses/");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        setData(jsonData);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Loading requests...</div>;
  }

  if (error) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Error: {error}</div>;
  }

  return (
    <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
      <DataTable data={data} />
    </div>
  );
}
