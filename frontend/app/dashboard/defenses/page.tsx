"use client";

import { useEffect, useState } from "react";
import { DefensesDataTable } from "@/components/defenses-data-table";
import { z } from "zod";
import { schema } from "@/components/defenses-data-table";
import { getDefenses } from "@/services/api"; // Import the new API function

export default function Page() {
  const [data, setData] = useState<z.infer<typeof schema>[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const jsonData = await getDefenses(); // Use the API function
        const acceptedDefenses = jsonData.filter((defense: any) => defense.status === 'accepted');
        setData(acceptedDefenses);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Loading defenses...</div>;
  }

  if (error) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Error: {error}</div>;
  }

  return (
    <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
      <DefensesDataTable data={data} />
    </div>
  );
}
