"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { savePlan } from "@/lib/api";
import type { EstimateResponse } from "@/types";

export default function ResultPage() {
  const [data, setData] = useState<EstimateResponse | null>(null);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveMessage, setSaveMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    try {
      const stored = sessionStorage.getItem("makerflow_result");
      if (stored) {
        const parsed = JSON.parse(stored) as EstimateResponse;
        if (parsed && typeof parsed === "object") {
          setData(parsed);
        }
      }
    } catch (e) {
      console.error("Failed to parse sessionStorage item 'makerflow_result'", e);
    }
  }, []);

  const formatCurrency = (val: number) => {
    return `Rp ${val.toLocaleString("id-ID")}`;
  };

  const handleSave = async () => {
    if (!data) return;
    setIsSaving(true);
    setSaveMessage(null);
    try {
      const res = await savePlan({
        product_name: data.product_name,
        target_qty: data.target_qty,
        budget_max: data.available_budget,
        category: data.detected_category_labels.join(" & "),
        result_json: data,
      });
      setSaveMessage({
        type: "success",
        text: `Rencana berhasil disimpan! (ID Plan: ${res.plan_id})`,
      });
    } catch (err) {
      setSaveMessage({
        type: "error",
        text: err instanceof Error ? err.message : "Gagal menyimpan rencana.",
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-50 text-black font-sans flex flex-col items-center justify-center p-4">
        <div className="max-w-md w-full border border-black p-6 bg-white text-center">
          <h2 className="text-lg font-bold mb-2 uppercase">Belum Ada Data Estimasi</h2>
          <p className="text-sm text-gray-600 mb-4">
            Silakan isi form rencana produksi terlebih dahulu.
          </p>
          <Link
            href="/plan"
            className="inline-block border border-black bg-black text-white px-4 py-2 font-bold uppercase hover:bg-gray-800 transition-colors"
          >
            Isi Form Rencana
          </Link>
        </div>
      </div>
    );
  }

  const isSufficient = data.budget_status === "sufficient";

  return (
    <div className="min-h-screen bg-gray-50 text-black font-sans py-8 px-4">
      {/* Main Container */}
      <main className="max-w-3xl mx-auto border border-black bg-white p-6 flex flex-col gap-6 shadow-sm">
        <header className="border-b border-black pb-4 text-center">
          <h1 className="font-bold text-xl uppercase tracking-wider">
            HASIL ESTIMASI PRODUKSI AI
          </h1>
        </header>

        {/* Section A — Input Summary */}
        <section className="border border-black p-4 bg-gray-50 flex flex-col gap-2">
          <h2 className="font-bold text-xs uppercase text-gray-500 tracking-wider">
            SECTION A — RINGKASAN INPUT
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="block text-xs text-gray-500 font-semibold uppercase">Kategori</span>
              <span className="font-bold">{data.detected_category_labels.join(" & ")}</span>
            </div>
            <div>
              <span className="block text-xs text-gray-500 font-semibold uppercase">Produk</span>
              <span className="font-bold">{data.product_name}</span>
            </div>
            <div>
              <span className="block text-xs text-gray-500 font-semibold uppercase">Jumlah</span>
              <span className="font-bold">{data.target_qty} unit</span>
            </div>
            <div>
              <span className="block text-xs text-gray-500 font-semibold uppercase">Anggaran Max</span>
              <span className="font-bold">{formatCurrency(data.available_budget)}</span>
            </div>
          </div>
        </section>

        {/* Section B — Budget Status Card */}
        <section className="border border-black p-4 bg-white flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <span className="text-xs font-semibold uppercase text-gray-500 block">
                SECTION B — ESTIMASI TOTAL BIAYA
              </span>
              <span className="text-2xl font-bold">
                {formatCurrency(data.total_cost_min)} – {formatCurrency(data.total_cost_max)}
              </span>
            </div>
            <div>
              <span className="text-xs font-semibold uppercase text-gray-500 block mb-1">
                STATUS ANGGARAN
              </span>
              <span
                className={`text-sm font-bold uppercase inline-block border border-black px-3 py-1 text-white ${
                  isSufficient ? "bg-emerald-600" : "bg-rose-600"
                }`}
              >
                {isSufficient ? "SUFFICIENT (CUKUP)" : "INSUFFICIENT (TIDAK CUKUP)"}
              </span>
            </div>
          </div>

          {/* Reverse Calculation — only shown when budget insufficient */}
          {!isSufficient && data.estimated_affordable_qty !== null && (
            <div className="border border-amber-400 bg-amber-50 px-4 py-3 flex items-center gap-3">
              <span className="text-amber-600 font-bold text-lg">⚠</span>
              <div>
                <span className="text-xs font-semibold uppercase text-amber-700 block">
                  ESTIMASI QTY MAMPU
                </span>
                <span className="font-bold text-amber-800 text-sm">
                  {data.estimated_affordable_qty} unit{" "}
                  <span className="font-normal text-amber-700">(dengan budget saat ini)</span>
                </span>
              </div>
            </div>
          )}
        </section>

        {/* Section C — Material Cards (horizontal scroll) */}
        <section className="flex flex-col gap-2">
          <h2 className="font-bold text-xs uppercase text-gray-500 tracking-wider">
            SECTION C — DAFTAR RINGKAS BAHAN
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {data.materials_needed.map((item, idx) => (
              <div
                key={idx}
                className="min-w-[200px] border border-black p-3 bg-gray-50 flex flex-col justify-between"
              >
                <div>
                  <h3 className="font-bold text-sm leading-tight">{item.name}</h3>
                  <span className="text-xs text-gray-600 block mt-1">Grade: {item.grade}</span>
                </div>
                <div className="mt-3 pt-2 border-t border-gray-300 text-xs font-semibold">
                  {formatCurrency(item.cost_min)} – {formatCurrency(item.cost_max)} / {item.unit}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Section D — Detailed Material Table */}
        <section className="flex flex-col gap-2">
          <h2 className="font-bold text-xs uppercase text-gray-500 tracking-wider">
            SECTION D — RINCIAN BAHAN BAKU
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-black text-left text-sm">
              <thead>
                <tr className="bg-gray-100 border-b border-black">
                  <th className="border-r border-black p-2 font-bold">Nama Bahan</th>
                  <th className="border-r border-black p-2 font-bold">Per Unit</th>
                  <th className="border-r border-black p-2 font-bold">Total Unit</th>
                  <th className="p-2 font-bold">Estimasi Harga</th>
                </tr>
              </thead>
              <tbody>
                {data.materials_needed.map((item, index) => (
                  <tr key={index} className="border-b border-black last:border-b-0">
                    <td className="border-r border-black p-2 font-medium">{item.name}</td>
                    <td className="border-r border-black p-2">
                      {item.qty_per_unit} {item.unit}
                    </td>
                    <td className="border-r border-black p-2 font-semibold">
                      {item.qty_total} {item.unit}
                    </td>
                    <td className="p-2 font-semibold">
                      {formatCurrency(item.cost_min)} – {formatCurrency(item.cost_max)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Section E — Substitution Recommendations (Conditional) */}
        {data.substitution_suggestions && data.substitution_suggestions.length > 0 && (
          <section className="border border-black p-4 bg-amber-50 flex flex-col gap-2">
            <h2 className="font-bold text-xs uppercase text-amber-900 tracking-wider">
              SECTION E — REKOMENDASI SUBSTITUSI BAHAN
            </h2>
            <div className="flex flex-col gap-3">
              {data.substitution_suggestions.map((sub, idx) => (
                <div key={idx} className="text-sm border-l-2 border-amber-600 pl-3">
                  <div className="font-bold">
                    {sub.original_name} &rarr; <span className="text-amber-800">{sub.substitute_name}</span>
                  </div>
                  <div className="text-xs text-gray-700 mt-1">{sub.reason}</div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Section F — Procurement Advice */}
        {data.procurement_advice && (
          <section className="border border-black p-4 bg-gray-50 flex flex-col gap-1">
            <h2 className="font-bold text-xs uppercase text-gray-500 tracking-wider">
              SECTION F — SARAN PENGADAAN (PROCUREMENT ADVICE)
            </h2>
            <p className="text-sm leading-relaxed">{data.procurement_advice}</p>
          </section>
        )}

        {/* Section G — Save & Actions */}
        <section className="flex flex-col gap-3 pt-2 border-t border-black">
          {saveMessage && (
            <div
              className={`p-3 text-sm font-semibold border border-black ${
                saveMessage.type === "success" ? "bg-emerald-100 text-emerald-800" : "bg-red-100 text-red-800"
              }`}
            >
              {saveMessage.text}
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex-1 bg-black text-white p-3 border border-black font-bold uppercase hover:bg-gray-800 transition-colors disabled:bg-gray-400"
            >
              {isSaving ? "Menyimpan Rencana..." : "Simpan Rencana Produksi"}
            </button>
            <Link
              href="/history"
              className="flex-1 border border-black bg-gray-100 text-black p-3 font-bold uppercase hover:bg-gray-200 text-center transition-colors"
            >
              Lihat Riwayat Rencana
            </Link>
            <Link
              href="/plan"
              className="border border-black bg-white text-black p-3 font-bold uppercase hover:bg-gray-100 text-center transition-colors"
            >
              Buat Baru
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
