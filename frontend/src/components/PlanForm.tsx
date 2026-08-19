"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { postEstimate } from "@/lib/api";
import type { EstimateRequest } from "@/types";

const FIXED_PRODUCTS = [
  "Gelang Macramé / Bracelet Custom",
  "Kerajinan Miniatur Rajutan",
  "Key Chain Rajut Custom Karakter",
  "Key Chain Resin",
  "Figura Kayu",
  "Kemasan Gift Box",
  "Totebag Canvas (Custom Draw)",
  "Gantungan Kunci Resin Kayu Premium + Rumbai",
  "Pouch Kanvas Resleting dengan Gantungan Resin",
  "Paket Kado Figura Kayu & Boneka Rajut",
  "Totebag Kanvas dengan Tali Makrame & Pegangan Resin",
] as const;

export default function PlanForm() {
  const router = useRouter();
  const [productName, setProductName] = useState<string>(FIXED_PRODUCTS[0]);
  const [targetQty, setTargetQty] = useState<number | "">(10);
  const [availableBudget, setAvailableBudget] = useState<number | "">(300000);
  const [hasMandatory, setHasMandatory] = useState<boolean>(false);
  const [mandatoryName, setMandatoryName] = useState<string>("");
  const [allowSubstitution, setAllowSubstitution] = useState<boolean>(true);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    const req: EstimateRequest = {
      product_name: productName,
      target_qty: Number(targetQty) || 1,
      available_budget: Number(availableBudget) || 1,
      has_mandatory_material: hasMandatory,
      mandatory_material_name: hasMandatory ? mandatoryName.trim() || null : null,
      allow_substitution: hasMandatory ? allowSubstitution : null,
    };

    try {
      const result = await postEstimate(req);
      sessionStorage.setItem("makerflow_result", JSON.stringify(result));
      sessionStorage.setItem("makerflow_input", JSON.stringify(req));
      router.push("/plan/result");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Terjadi kesalahan saat menghubungi server.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 border border-black my-8 bg-white text-black shadow-sm">
      <h1 className="text-center font-bold uppercase text-xl mb-4 tracking-wide">
        MAKERFLOW — RENCANA PRODUKSI
      </h1>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-500 text-red-700 text-sm font-medium">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Field 1: Nama Produk */}
        <div className="flex flex-col gap-1">
          <label htmlFor="product_name" className="font-semibold text-sm">
            Pilih Produk*
          </label>
          <select
            id="product_name"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            required
            className="border border-black p-2 w-full bg-white focus:outline-none focus:ring-1 focus:ring-black"
          >
            {FIXED_PRODUCTS.map((prod) => (
              <option key={prod} value={prod}>
                {prod}
              </option>
            ))}
          </select>
        </div>

        {/* Field 2: Target Qty */}
        <div className="flex flex-col gap-1">
          <label htmlFor="target_qty" className="font-semibold text-sm">
            Target Jumlah Produksi (Unit)*
          </label>
          <input
            id="target_qty"
            type="number"
            min={1}
            required
            value={targetQty}
            onChange={(e) => setTargetQty(e.target.value === "" ? "" : Number(e.target.value))}
            className="border border-black p-2 w-full focus:outline-none focus:ring-1 focus:ring-black"
          />
        </div>

        {/* Field 3: Available Budget */}
        <div className="flex flex-col gap-1">
          <label htmlFor="available_budget" className="font-semibold text-sm">
            Budget yang Dimiliki (Available Budget) (Rp)*
          </label>
          <input
            id="available_budget"
            type="number"
            min={1}
            required
            value={availableBudget}
            onChange={(e) => setAvailableBudget(e.target.value === "" ? "" : Number(e.target.value))}
            placeholder="Contoh: 300000"
            className="border border-black p-2 w-full focus:outline-none focus:ring-1 focus:ring-black"
          />
        </div>

        {/* Field 4: Has Mandatory Material */}
        <div className="flex items-center gap-2 mt-1">
          <input
            id="has_mandatory_material"
            type="checkbox"
            checked={hasMandatory}
            onChange={(e) => setHasMandatory(e.target.checked)}
            className="border border-black h-4 w-4 accent-black cursor-pointer"
          />
          <label htmlFor="has_mandatory_material" className="font-semibold text-sm cursor-pointer">
            Ada Bahan Wajib (Tidak Boleh Diganti)?
          </label>
        </div>

        {/* Conditional Fields 5 & 6 */}
        {hasMandatory && (
          <div className="pl-4 border-l-2 border-black flex flex-col gap-3 my-1">
            <div className="flex flex-col gap-1">
              <label htmlFor="mandatory_material_name" className="font-semibold text-sm">
                Nama Bahan Wajib*
              </label>
              <input
                id="mandatory_material_name"
                type="text"
                required={hasMandatory}
                value={mandatoryName}
                onChange={(e) => setMandatoryName(e.target.value)}
                placeholder="Contoh: Tali Kur"
                className="border border-black p-2 w-full focus:outline-none focus:ring-1 focus:ring-black"
              />
            </div>

            <div className="flex items-center gap-2">
              <input
                id="allow_substitution"
                type="checkbox"
                checked={allowSubstitution}
                onChange={(e) => setAllowSubstitution(e.target.checked)}
                className="border border-black h-4 w-4 accent-black cursor-pointer"
              />
              <label htmlFor="allow_substitution" className="font-semibold text-sm cursor-pointer">
                Bolehkan Substitusi Bahan Lain?
              </label>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="border border-black bg-black text-white p-2 font-bold uppercase hover:bg-gray-800 transition-colors mt-2 disabled:bg-gray-400"
        >
          {isLoading ? "Menghitung Estimasi AI..." : "Hitung Estimasi Produksi"}
        </button>
      </form>
    </div>
  );
}