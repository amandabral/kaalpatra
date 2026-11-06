"use client";

import React, { useState } from "react";
import { Sparkles, Calendar as CalendarIcon } from "lucide-react";

interface DatePickerFormProps {
  onSearch: (date: string) => void;
  isLoading: boolean;
}

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const PRESETS = [
  { label: "🇮🇳 Independence Day", date: "1947-08-15" },
  { label: "🏏 1983 World Cup Win", date: "1983-06-25" },
  { label: "⭐ Sachin Tendulkar Born", date: "1973-04-24" },
  { label: "🚀 Rakesh Sharma in Space", date: "1984-04-03" },
];

export default function DatePickerForm({ onSearch, isLoading }: DatePickerFormProps) {
  const [day, setDay] = useState("15");
  const [month, setMonth] = useState("8");
  const [year, setYear] = useState("1947");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formattedDate = `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    onSearch(formattedDate);
  };

  const handlePreset = (presetDate: string) => {
    const [y, m, d] = presetDate.split("-");
    setYear(y);
    setMonth(String(parseInt(m, 10)));
    setDay(String(parseInt(d, 10)));
    onSearch(presetDate);
  };

  // Generate years from 2025 down to 1925
  const years = Array.from({ length: 101 }, (_, i) => 2025 - i);
  // Generate days 1 to 31
  const days = Array.from({ length: 31 }, (_, i) => i + 1);

  return (
    <div className="w-full max-w-2xl mx-auto bg-stone-900/90 border border-amber-900/40 rounded-2xl p-6 shadow-2xl backdrop-blur">
      <div className="text-center mb-6">
        <h2 className="text-xl sm:text-2xl font-serif text-amber-100 flex items-center justify-center gap-2">
          <CalendarIcon className="w-5 h-5 text-amber-500" />
          Choose Your Birth Date
        </h2>
        <p className="text-sm text-stone-400 mt-1">
          Travel back in time to explore India on the exact day you were born
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-3 gap-3">
          {/* Day */}
          <div>
            <label className="block text-xs uppercase tracking-wider text-stone-400 mb-1">Day</label>
            <select
              value={day}
              onChange={(e) => setDay(e.target.value)}
              className="w-full bg-stone-800 border border-stone-700 text-stone-100 rounded-xl px-3 py-2.5 focus:outline-none focus:border-amber-500 font-mono text-sm"
            >
              {days.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          {/* Month */}
          <div>
            <label className="block text-xs uppercase tracking-wider text-stone-400 mb-1">Month</label>
            <select
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              className="w-full bg-stone-800 border border-stone-700 text-stone-100 rounded-xl px-3 py-2.5 focus:outline-none focus:border-amber-500 font-mono text-sm"
            >
              {MONTHS.map((m, idx) => (
                <option key={m} value={idx + 1}>
                  {m}
                </option>
              ))}
            </select>
          </div>

          {/* Year */}
          <div>
            <label className="block text-xs uppercase tracking-wider text-stone-400 mb-1">Year</label>
            <select
              value={year}
              onChange={(e) => setYear(e.target.value)}
              className="w-full bg-stone-800 border border-stone-700 text-stone-100 rounded-xl px-3 py-2.5 focus:outline-none focus:border-amber-500 font-mono text-sm"
            >
              {years.map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full mt-2 bg-gradient-to-r from-amber-600 via-amber-500 to-yellow-600 hover:from-amber-500 hover:to-yellow-500 text-stone-950 font-semibold py-3 px-6 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          <Sparkles className="w-5 h-5" />
          {isLoading ? "Opening Time Capsule..." : "Open Time Capsule"}
        </button>
      </form>

      {/* Presets */}
      <div className="mt-6 pt-4 border-t border-stone-800">
        <p className="text-xs text-stone-400 mb-2 text-center uppercase tracking-wider">
          Or try a legendary historic day:
        </p>
        <div className="flex flex-wrap justify-center gap-2">
          {PRESETS.map((p) => (
            <button
              key={p.date}
              type="button"
              onClick={() => handlePreset(p.date)}
              className="text-xs bg-stone-800 hover:bg-stone-700 text-stone-300 hover:text-amber-300 px-3 py-1.5 rounded-lg border border-stone-700/60 transition"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}