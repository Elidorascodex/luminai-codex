import React from "react";

const variantForValue = (value: number) => {
  if (value >= 0.9) {
    return {
      gradient: "from-emerald-400 via-amber-200 to-yellow-400",
      ring: "ring-emerald-300",
      pulse: "resonance-pulse-strong",
    };
  }

  if (value >= 0.6) {
    return {
      gradient: "from-cyan-400 via-indigo-400 to-purple-500",
      ring: "ring-cyan-300",
      pulse: "resonance-pulse-soft",
    };
  }

  return {
    gradient: "from-rose-500 via-orange-400 to-amber-400",
    ring: "ring-rose-400",
    pulse: "resonance-pulse-alert",
  };
};

export type ResonanceBadgeProps = {
  r: number;
  size?: "sm" | "md";
};

const sizes = {
  sm: "h-12 w-12 text-sm",
  md: "h-16 w-16 text-base",
};

const ResonanceBadge: React.FC<ResonanceBadgeProps> = ({ r, size = "md" }) => {
  const value = Math.max(0, Math.min(r, 1));
  const { gradient, ring, pulse } = variantForValue(value);
  const display = Math.round(value * 100);

  return (
    <div
      aria-label={`Resonance score ${display} out of 100`}
      className={`relative flex items-center justify-center rounded-full bg-gradient-to-br ${gradient} ${sizes[size]} ring-2 ${ring} text-slate-950 font-semibold ${pulse}`}
    >
      <span>{display}</span>
    </div>
  );
};

export default ResonanceBadge;
