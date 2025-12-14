"use client";

import { useEffect, useState, useCallback } from "react";
import { DataTable } from "@/components/data-table";
import { z } from "zod";
import { schema } from "@/components/data-table";
import { getDefenses } from "@/services/api";

export default function Page() {
  const [data, setData] = useState<z.infer<typeof schema>[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const jsonData = await getDefenses();
      setData(jsonData);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Loading requests...</div>;
  }

  if (error) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Error: {error}</div>;
  }

  return (
    <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
      <DataTable data={data} onUpdate={fetchData} />
    </div>
  );
}
