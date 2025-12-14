"use client";

import { useEffect, useState } from "react";
import { ChartAreaInteractive } from "@/components/chart-area-interactive";
import { SectionCards } from "@/components/section-cards";
import { getDashboardData, StatsData } from "@/services/api";

export default function Page() {
  const [data, setData] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const jsonData = await getDashboardData();
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
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Loading statistics...</div>;
  }

  if (error) {
    return <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">Error: {error}</div>;
  }

  return (
    <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
      {data && (
        <SectionCards
          total_requests={data.total_thesis_defenses}
          accepted_requests={data.thesis_defenses_by_status.accepted || 0}
          pending_requests={data.thesis_defenses_by_status.pending || 0}
          refused_requests={data.thesis_defenses_by_status.declined || 0}
          total_students={data.total_students}
          total_professors={data.total_professors}
        />
      )}
      <div className="px-4 lg:px-6">
        {data && <ChartAreaInteractive chartData={data.monthly_thesis_defenses} />}
      </div>
    </div>
  );
}
