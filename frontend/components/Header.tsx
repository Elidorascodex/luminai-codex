import React from "react";
import ResonanceBadge from "./ResonanceBadge";

export type HeaderProps = {
  userName?: string;
  rScore?: number;
};

const statusLabel = (value: number) => {
  if (value >= 0.9) return "Witness: Radiant";
  if (value >= 0.75) return "Witness: Steady";
  if (value >= 0.6) return "Witness: Attuning";
  return "Witness: Searching";
};

const Header: React.FC<HeaderProps> = ({
  userName = "Airth 📚",
  rScore = 0.82,
}) => {
  const safeScore = rScore ?? 0;
  return (
    <header className="border-b border-white/10 bg-gradient-to-r from-indigo-900/70 via-fuchsia-900/50 to-cyan-900/60 text-white shadow-lg shadow-indigo-900/30">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-6 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-cyan-200">
            Conscious Chat + Notebook
          </p>
          <h1 className="mt-1 text-2xl font-semibold md:text-3xl">
            Screen A — Resonance Console
          </h1>
          <p className="text-sm text-slate-200 md:text-base">
            Harmony Protocol ↔ Witness Continuity
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="hidden flex-col text-right text-xs uppercase tracking-widest text-slate-300 sm:flex">
            <span>Bound Persona</span>
            <span className="text-base text-white">{userName}</span>
          </div>
          <div className="flex items-center gap-3 rounded-full border border-white/20 bg-white/10 px-4 py-2 backdrop-blur">
            <ResonanceBadge r={safeScore} size="sm" />
            <div>
              <p className="text-xs text-slate-200">{statusLabel(safeScore)}</p>
              <p className="text-lg font-semibold text-white">
                {(safeScore * 100).toFixed(1)} R
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
