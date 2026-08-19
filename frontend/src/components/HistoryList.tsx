"use client";

import React from "react";
import Link from "next/link";
import type { PlanSummary } from "@/types";

interface HistoryListProps {
  plans: PlanSummary[];
  onSelectPlan?: (id: number) => void;
}

export default function HistoryList({ plans, onSelectPlan }: HistoryListProps) {
  if (!plans || plans.length === 0) {
    return (
      <div className="border border-black p-6 bg-white text-center">
        <p className="text-gray-600 text-sm font-medium mb-3">Belum ada rencana produksi yang disimpan.</p>
        <Link
          href="/plan"
          className="inline-block border border-black bg-black text-white px-4 py-2 font-bold uppercase hover:bg-gray-800 text-xs transition-colors"
        >
          Buat Rencana Baru
        </Link>
      </div>
    );
  }

  const formatCurrency = (val: number) => `Rp ${val.toLocaleString("id-ID")}`;
  const formatDate = (isoStr: string) => {
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString("id-ID", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoStr;
    }
  };

  return (
    <div className="flex flex-col gap-3">
      {plans.map((plan) => (
        <div
          key={plan.id}
          className="border border-black p-4 bg-white flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 hover:bg-gray-50 transition-colors"
        >
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-bold uppercase bg-gray-200 border border-black px-2 py-0.5">
                ID #{plan.id}
              </span>
              <span className="text-xs text-gray-500 font-semibold">{plan.category}</span>
            </div>
            <h3 className="font-bold text-base leading-tight">{plan.product_name}</h3>
            <div className="text-xs text-gray-600 mt-1">
              Target: <span className="font-semibold text-black">{plan.target_qty} unit</span> | Anggaran:{" "}
              <span className="font-semibold text-black">{formatCurrency(plan.budget_max)}</span>
            </div>
          </div>

          <div className="flex flex-col sm:items-end gap-1 w-full sm:w-auto border-t sm:border-t-0 pt-2 sm:pt-0 border-gray-200">
            <span className="text-xs text-gray-500">{formatDate(plan.created_at)}</span>
            {onSelectPlan && (
              <button
                onClick={() => onSelectPlan(plan.id)}
                className="border border-black bg-black text-white px-3 py-1 text-xs font-bold uppercase hover:bg-gray-800 transition-colors"
              >
                Lihat Detail
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
