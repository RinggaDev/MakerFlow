"use client";

import Link from "next/link";
import PlanForm from "@/components/PlanForm";

// ponytail: single responsibility — render the form and nav, nothing else
export default function PlanPage() {
  return (
    <div className="min-h-screen bg-gray-50 text-black font-sans">
      <header className="border-b border-black p-4 bg-white flex items-center justify-between">
        <h1 className="font-bold text-lg uppercase tracking-wider">MakerFlow</h1>
        <Link
          href="/history"
          className="border border-black px-3 py-1 text-xs font-bold uppercase hover:bg-gray-100 transition-colors"
        >
          Riwayat Rencana
        </Link>
      </header>

      <main className="max-w-xl mx-auto mt-8 px-4">
        <PlanForm />
      </main>
    </div>
  );
}
