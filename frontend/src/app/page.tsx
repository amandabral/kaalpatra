"use client";

import React, { useState } from "react";
import DatePickerForm from "@/components/DatePickerForm";
import TimeCapsuleView from "@/components/TimeCapsuleView";
import { getTimeCapsule } from "@/lib/api";
import { TimeCapsuleResponse } from "@/types/capsule";
import { Hourglass } from "lucide-react";

export default function Home() {
  const [capsuleData, setCapsuleData] = useState<TimeCapsuleResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (date: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getTimeCapsule(date);
      setCapsuleData(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to fetch time capsule.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setCapsuleData(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-stone-950 text-stone-100 px-4 py-12 sm:py-16 selection:bg-amber-500 selection:text-stone-950">
      {/* Brand Header */}
      <header className="max-w-4xl mx-auto text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-stone-900 border border-amber-900/50 text-amber-400 text-xs tracking-widest uppercase mb-4">
          <Hourglass className="w-3.5 h-3.5" />
          The Indian Time Machine (1925 – 2025)
        </div>
        <h1 className="text-4xl sm:text-6xl font-serif font-extrabold tracking-tight text-amber-100">
          KaalPatra <span className="text-amber-500 font-normal">कालपात्र</span>
        </h1>
        <p className="text-stone-400 text-sm sm:text-base max-w-xl mx-auto mt-3">
          Discover what India was like on the exact day you were born — historical headlines,
          retro commodity prices, Bollywood chartbusters, and your birthday twins.
        </p>
      </header>

      {/* Error Message */}
      {error && (
        <div className="max-w-xl mx-auto mb-6 p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-center text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Main Content Area */}
      {!capsuleData ? (
        <DatePickerForm onSearch={handleSearch} isLoading={isLoading} />
      ) : (
        <TimeCapsuleView data={capsuleData} onReset={handleReset} />
      )}

      {/* Footer */}
      <footer className="mt-20 text-center text-xs text-stone-600 border-t border-stone-900 pt-6">
        KaalPatra • Built with Django DRF, PostgreSQL, Next.js & Tailwind CSS
      </footer>
    </main>
  );
}