"use client";

import React, { useState } from "react";

interface ProductInputProps {
  onSubmit: (description: string) => void;
  isLoading?: boolean;
}

export default function ProductInput({
  onSubmit,
  isLoading = false,
}: ProductInputProps) {
  const [description, setDescription] = useState<string>("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = description.trim();
    if (trimmed && !isLoading) {
      onSubmit(trimmed);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="flex flex-col gap-2">
        <label
          htmlFor="product-description"
          className="font-semibold text-sm uppercase tracking-wide text-black"
        >
          Ceritakan produk yang ingin Anda buat...
        </label>
        <textarea
          id="product-description"
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isLoading}
          placeholder="Contoh: Saya ingin membuat gelang tangan macrame custom dengan tali goni dan hiasan manik kayu..."
          className="w-full border border-black p-3 bg-white text-black placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-black disabled:bg-gray-100 disabled:cursor-not-allowed resize-none"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading || !description.trim()}
        className="w-full border border-black bg-black text-white p-3 font-bold uppercase text-sm tracking-wider hover:bg-gray-800 transition-colors disabled:bg-gray-300 disabled:border-gray-300 disabled:cursor-not-allowed"
      >
        {isLoading ? "Memproses..." : "Lanjutkan ke Klasifikasi"}
      </button>
    </form>
  );
}
