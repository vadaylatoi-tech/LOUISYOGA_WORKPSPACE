import type React from "react";
import { MONTSERRAT } from "./useMontserrat";

// Louis Yoga reel style 1 — shared constants.
// Canvas: 1080x1920 @30fps (TikTok / Reels / Shorts).
export const FPS = 30;
export const W = 1080;
export const H = 1920;

// Palette: hot pink accent + gold on a wine-tinted charcoal (approved by the brand owner).
export const C = {
  ink: "#16111A",
  accent: "#FF5AAE",
  pinkDeep: "#E2318B",
  gold: "#F4C25B",
  white: "#FFFFFF",
  paper: "#E7E1D3",
  dim: "rgba(255,255,255,0.55)",
};

export const f = (t: number) => Math.round(t * FPS);
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Deterministic pseudo-random (never Math.random in a composition).
export const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

// Heavy uppercase Montserrat (has full Vietnamese diacritics).
export const font = (weight: number, size: number): React.CSSProperties => ({
  fontFamily: MONTSERRAT,
  fontWeight: weight,
  fontSize: size,
  lineHeight: 1.05,
  textTransform: "uppercase",
  letterSpacing: -1,
});
