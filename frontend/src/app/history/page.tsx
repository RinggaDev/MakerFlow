"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { listPlans, getPlan } from "@/lib/api";
import HistoryList from "@/components/HistoryList";
import type { PlanSummary } from "@/types";

export default function HistoryPage() {
  const router = useRouter();
  const [plans, setPlans] = useState<PlanSummary[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listPlans();
      setPlans(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal memuat riwayat.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectPlan = async (id: number) => {
    try {
      const detail = await getPlan(id);
      sessionStorage.setItem("makerflow_result", JSON.stringify(detail.result_json));
      router.push("/plan/result");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Gagal mengambil detail rencana.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-black font-sans py-8 px-4">
      <main className="max-w-3xl mx-auto border border-black bg-white p-6 flex flex-col gap-6 shadow-sm">
        <header className="border-b border-black pb-4 flex flex-col sm:flex-row justify-between items-center gap-4">
          <h1 className="font-bold text-xl uppercase tracking-wider">
            RIWAYAT RENCANA PRODUKSI
          </h1>
          <Link
            href="/plan"
            className="border border-black bg-black text-white px-4 py-2 font-bold uppercase text-xs hover:bg-gray-800 transition-colors"
          >
            + Rencana Baru
          </Link>
        </header>

        {isLoading ? (
          <div className="py-8 text-center text-sm font-semibold text-gray-600">
            Memuat riwayat rencana...
          </div>
        ) : error ? (
          <div className="p-4 border border-red-500 bg-red-50 text-red-700 text-sm font-medium">
            {error}
          </div>
        ) : (
          <HistoryList plans={plans} onSelectPlan={handleSelectPlan} />
        )}
      </main>
    </div>
  );
}
