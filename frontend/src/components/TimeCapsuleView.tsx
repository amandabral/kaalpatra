"use client";

import React from "react";
import { motion } from "framer-motion";
import { TimeCapsuleResponse } from "@/types/capsule";
import {
  Moon,
  Coins,
  Film,
  Music,
  Landmark,
  Sparkles,
  Calendar,
  RotateCcw,
  Star,
  Flame,
  Radio
} from "lucide-react";

interface TimeCapsuleViewProps {
  data: TimeCapsuleResponse;
  onReset: () => void;
}

export default function TimeCapsuleView({ data, onReset }: TimeCapsuleViewProps) {
  const { calendar, leadership, annual_snapshot, exact_events, exact_twins, calendar_twins } = data;

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.12, duration: 0.6 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="w-full max-w-4xl mx-auto space-y-6"
    >
      {/* 1. Masthead / Hero Header */}
      <motion.div
        variants={itemVariants}
        className="text-center bg-gradient-to-b from-stone-900 to-stone-950 border border-amber-900/40 rounded-3xl p-8 shadow-2xl relative overflow-hidden"
      >
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-600 via-amber-400 to-amber-600" />
        
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800/60 text-amber-300 text-xs tracking-wider uppercase mb-3">
          <Sparkles className="w-3.5 h-3.5" />
          {annual_snapshot?.era_badge || "Indian Historical Era"}
        </div>

        <h1 className="text-3xl sm:text-5xl font-serif text-amber-100 font-bold tracking-tight">
          {calendar.formatted_date}
        </h1>
        <p className="text-stone-400 text-base sm:text-lg mt-2 font-mono">
          It was a <span className="text-amber-400 font-semibold">{calendar.day_of_week}</span> • {calendar.days_ago.toLocaleString()} days ago
        </p>

        {/* Moon Phase & Day summary pill */}
        <div className="mt-4 flex flex-wrap items-center justify-center gap-3 text-xs sm:text-sm text-stone-300">
          <div className="flex items-center gap-1.5 bg-stone-800/80 px-3 py-1.5 rounded-xl border border-stone-700/50">
            <Moon className="w-4 h-4 text-amber-400" />
            <span>Moon: <strong className="text-stone-100">{calendar.moon_phase}</strong></span>
          </div>
          <div className="flex items-center gap-1.5 bg-stone-800/80 px-3 py-1.5 rounded-xl border border-stone-700/50">
            <Landmark className="w-4 h-4 text-amber-400" />
            <span>Leader: <strong className="text-stone-100">{leadership.head_of_state}</strong></span>
          </div>
        </div>
      </motion.div>

      {/* 2. Exact Date Twin & Headlines (If Any) */}
      {(exact_twins.length > 0 || exact_events.length > 0) && (
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {exact_twins.length > 0 && (
            <div className="bg-amber-950/30 border border-amber-600/40 rounded-2xl p-5 shadow-lg relative overflow-hidden">
              <div className="flex items-center gap-2 text-amber-400 font-serif text-lg font-bold mb-2">
                <Star className="w-5 h-5 text-amber-400 fill-amber-400" />
                Exact Date Twin!
              </div>
              <p className="text-xs text-amber-200/80 mb-3">
                Born on the exact same day, month, and year:
              </p>
              {exact_twins.map((t) => (
                <div key={t.id} className="bg-stone-900/80 rounded-xl p-3 border border-amber-800/40">
                  <h4 className="font-semibold text-stone-100">{t.name}</h4>
                  <p className="text-xs text-amber-400/90 font-mono mb-1">{t.field_display}</p>
                  <p className="text-xs text-stone-300 leading-relaxed">{t.bio}</p>
                </div>
              ))}
            </div>
          )}

          {exact_events.length > 0 && (
            <div className="bg-stone-900/90 border border-red-900/40 rounded-2xl p-5 shadow-lg">
              <div className="flex items-center gap-2 text-red-400 font-serif text-lg font-bold mb-2">
                <Flame className="w-5 h-5" />
                Historic National Event
              </div>
              {exact_events.map((e) => (
                <div key={e.id} className="bg-stone-950/80 rounded-xl p-3 border border-stone-800">
                  <h4 className="font-semibold text-stone-100">{e.title}</h4>
                  <p className="text-xs text-red-400 font-mono mb-1">{e.category_display}</p>
                  <p className="text-xs text-stone-300 leading-relaxed">{e.description}</p>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* 3. The Nostalgia Price Index */}
      {annual_snapshot && (
        <motion.div
          variants={itemVariants}
          className="bg-stone-900/80 border border-stone-800 rounded-3xl p-6 shadow-xl"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-serif text-amber-100 flex items-center gap-2">
              <Coins className="w-5 h-5 text-amber-400" />
              Cost of Living in {annual_snapshot.year}
            </h3>
            <span className="text-xs font-mono text-stone-400 bg-stone-800 px-2.5 py-1 rounded-lg">
              RBI & Bullion Index
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-stone-950/70 p-4 rounded-xl border border-stone-800/80">
              <p className="text-xs text-stone-400 uppercase tracking-wider">10g Gold</p>
              <p className="text-lg sm:text-2xl font-bold text-amber-300 font-mono mt-1">
                ₹{Number(annual_snapshot.gold_price_10g).toLocaleString()}
              </p>
              <p className="text-[11px] text-stone-500 mt-1">vs ₹78,000+ today</p>
            </div>

            <div className="bg-stone-950/70 p-4 rounded-xl border border-stone-800/80">
              <p className="text-xs text-stone-400 uppercase tracking-wider">1L Petrol</p>
              <p className="text-lg sm:text-2xl font-bold text-stone-100 font-mono mt-1">
                ₹{Number(annual_snapshot.petrol_price_litre).toFixed(2)}
              </p>
              <p className="text-[11px] text-stone-500 mt-1">vs ₹96+ today</p>
            </div>

            <div className="bg-stone-950/70 p-4 rounded-xl border border-stone-800/80">
              <p className="text-xs text-stone-400 uppercase tracking-wider">USD to INR</p>
              <p className="text-lg sm:text-2xl font-bold text-stone-100 font-mono mt-1">
                $1 = ₹{Number(annual_snapshot.usd_inr_rate).toFixed(2)}
              </p>
              <p className="text-[11px] text-stone-500 mt-1">vs ₹83+ today</p>
            </div>

            <div className="bg-stone-950/70 p-4 rounded-xl border border-stone-800/80">
              <p className="text-xs text-stone-400 uppercase tracking-wider">Cinema Ticket</p>
              <p className="text-lg sm:text-2xl font-bold text-stone-100 font-mono mt-1">
                ₹{Number(annual_snapshot.cinema_ticket_avg).toFixed(2)}
              </p>
              <p className="text-[11px] text-stone-500 mt-1">Avg single-screen</p>
            </div>
          </div>

          {annual_snapshot.typical_salary && (
            <p className="text-xs text-stone-400 mt-3 text-center italic">
              Typical monthly clerk pay: {annual_snapshot.typical_salary}
            </p>
          )}
        </motion.div>
      )}

      {/* 4. Cinema & Cassette Player */}
      {annual_snapshot && (
        <motion.div
          variants={itemVariants}
          className="grid grid-cols-1 md:grid-cols-2 gap-4"
        >
          {/* Movie & Music */}
          <div className="bg-stone-900/80 border border-stone-800 rounded-2xl p-5 shadow-lg space-y-3">
            <h3 className="text-lg font-serif text-amber-200 flex items-center gap-2">
              <Film className="w-5 h-5 text-amber-400" />
              Theatres & Radio
            </h3>
            
            <div className="bg-stone-950/70 p-3 rounded-xl border border-stone-800">
              <p className="text-xs text-stone-400 uppercase tracking-wider">Blockbuster Film</p>
              <p className="font-semibold text-stone-100 text-sm mt-0.5">{annual_snapshot.top_movie}</p>
            </div>

            <div className="bg-stone-950/70 p-3 rounded-xl border border-stone-800">
              <p className="text-xs text-stone-400 uppercase tracking-wider flex items-center gap-1">
                <Music className="w-3.5 h-3.5 text-amber-400" /> Hit Song / Binaca Geetmala
              </p>
              <p className="font-semibold text-amber-300 text-sm mt-0.5">{annual_snapshot.top_song}</p>
            </div>
          </div>

          {/* Way of Life */}
          <div className="bg-stone-900/80 border border-stone-800 rounded-2xl p-5 shadow-lg space-y-3">
            <h3 className="text-lg font-serif text-amber-200 flex items-center gap-2">
              <Radio className="w-5 h-5 text-amber-400" />
              Way of Life
            </h3>
            <div className="bg-stone-950/70 p-4 rounded-xl border border-stone-800 h-[calc(100%-2.5rem)] flex items-center">
              <p className="text-stone-300 text-sm leading-relaxed italic">
                &ldquo;{annual_snapshot.lifestyle_summary}&rdquo;
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* 5. Indian Calendar Birthday Twins */}
      {calendar_twins.length > 0 && (
        <motion.div
          variants={itemVariants}
          className="bg-stone-900/80 border border-stone-800 rounded-3xl p-6 shadow-xl"
        >
          <h3 className="text-xl font-serif text-amber-100 flex items-center gap-2 mb-4">
            <Calendar className="w-5 h-5 text-amber-400" />
            Who Shares Your Birthday?
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {calendar_twins.slice(0, 6).map((twin) => (
              <div
                key={twin.id}
                className="bg-stone-950/70 p-3 rounded-xl border border-stone-800/80 hover:border-amber-700/50 transition"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold text-sm text-stone-100">{twin.name}</h4>
                  <span className="text-[10px] font-mono text-amber-400 bg-amber-950/80 px-2 py-0.5 rounded">
                    {twin.dob.slice(0, 4)}
                  </span>
                </div>
                <p className="text-xs text-stone-400 font-mono mt-0.5">{twin.field_display}</p>
                <p className="text-xs text-stone-400 mt-2 line-clamp-2 leading-relaxed">
                  {twin.bio}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* 6. Reset / Explore Another Date */}
      <motion.div variants={itemVariants} className="text-center pt-4">
        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 bg-stone-800 hover:bg-stone-700 text-stone-200 px-6 py-3 rounded-xl border border-stone-700 transition cursor-pointer font-medium text-sm"
        >
          <RotateCcw className="w-4 h-4 text-amber-400" />
          Explore Another Date
        </button>
      </motion.div>
    </motion.div>
  );
}