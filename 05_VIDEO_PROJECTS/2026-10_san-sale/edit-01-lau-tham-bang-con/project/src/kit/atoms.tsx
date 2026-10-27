import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { MONTSERRAT } from "./useMontserrat";
import { C, clamp, font, FPS, H, rnd, W } from "./theme";

// Graphic atoms of Louis Yoga reel style 1. All times are FRAMES unless a prop says seconds.

// ---------------------------------------------------------------- timing helpers

export const usePop = (start: number, damping = 12) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - start, fps, config: { damping, stiffness: 180, mass: 0.7 } });
};

// Visible window [start, end) with a short fade out; 0 outside.
export const useLife = (start: number, end: number, out = 6) => {
  const frame = useCurrentFrame();
  if (frame < start || frame >= end) return 0;
  return interpolate(frame, [end - out, end], [1, 0], clamp);
};

// ---------------------------------------------------------------- text

// Small spaced uppercase line above a title ("chất liệu", "khi quỳ gối · tì tay").
export const Kicker: React.FC<{ text: string; start: number; end: number; y: number; color?: string; left?: number; right?: number }> = ({
  text,
  start,
  end,
  y,
  color = C.white,
  left = 0,
  right = 0,
}) => {
  const life = useLife(start, end);
  const p = usePop(start, 14);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left,
        right,
        textAlign: "center",
        opacity: life * Math.min(1, p * 1.5),
        transform: `translateY(${(1 - p) * 30}px)`,
        ...font(800, 40),
        letterSpacing: 4,
        color,
      }}
    >
      {text}
    </div>
  );
};

// Big heavy title; slam = drops in from 1.7x with a short shake (pair with a punch SFX).
export const BigText: React.FC<{
  lines: { text: string; color: string; size: number }[];
  start: number;
  end: number;
  y: number;
  slam?: boolean;
}> = ({ lines, start, end, y, slam }) => {
  const frame = useCurrentFrame();
  const life = useLife(start, end);
  const p = usePop(start, 10);
  if (!life) return null;
  const s = slam ? interpolate(p, [0, 1], [1.7, 1]) : interpolate(p, [0, 1], [0.6, 1]);
  const shake = slam && frame - start < 8 ? (rnd(frame) - 0.5) * 14 : 0;
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: 40,
        right: 40,
        textAlign: "center",
        opacity: life * Math.min(1, p * 2),
        transform: `translate(${shake}px, ${shake * 0.6}px) scale(${s})`,
      }}
    >
      {lines.map((l, i) => (
        <div key={i} style={{ ...font(900, l.size), color: l.color, textShadow: "0 6px 0 rgba(0,0,0,0.55)" }}>
          {l.text}
        </div>
      ))}
    </div>
  );
};

// Gold rubber stamp that slams in (pair with punch; on the 1–2 biggest beats add shake/flash).
export const Stamp: React.FC<{ text: string; start: number; end: number; x: number; y: number; rot: number; size: number }> = ({
  text,
  start,
  end,
  x,
  y,
  rot,
  size,
}) => {
  const frame = useCurrentFrame();
  const life = useLife(start, end);
  const p = usePop(start, 9);
  if (!life) return null;
  const s = interpolate(p, [0, 1], [2.4, 1]);
  const shake = frame - start < 6 ? (rnd(frame + 5) - 0.5) * 18 : 0;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -50%) translate(${shake}px, ${shake}px) rotate(${rot}deg) scale(${s})`,
        opacity: life * Math.min(1, p * 3),
        border: `8px solid ${C.gold}`,
        borderRadius: 14,
        padding: "8px 26px",
        color: C.gold,
        ...font(900, size),
        whiteSpace: "nowrap",
        background: "rgba(244,194,91,0.08)",
        boxShadow: "inset 0 0 0 3px rgba(244,194,91,0.35)",
      }}
    >
      {text}
    </div>
  );
};

// Rounded label that pops (pair with pop / pop-2). x is the CENTRE.
export const Pill: React.FC<{ text: string; start: number; end: number; x: number; y: number; bg?: string; fg?: string; size?: number }> = ({
  text,
  start,
  end,
  x,
  y,
  bg = C.pinkDeep,
  fg = C.white,
  size = 34,
}) => {
  const life = useLife(start, end);
  const p = usePop(start, 13);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translateX(-50%) scale(${p})`,
        opacity: life,
        background: bg,
        color: fg,
        padding: "12px 28px",
        borderRadius: 999,
        ...font(900, size),
        letterSpacing: 1,
        whiteSpace: "nowrap",
        boxShadow: "0 10px 24px rgba(0,0,0,0.45)",
      }}
    >
      {text}
    </div>
  );
};

export const NumberCircle: React.FC<{ n: string; start: number; end: number; x: number; y: number }> = ({ n, start, end, x, y }) => {
  const life = useLife(start, end);
  const p = usePop(start, 10);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: 110,
        height: 110,
        borderRadius: 999,
        border: `6px solid ${C.accent}`,
        boxShadow: "0 0 26px rgba(255,90,174,0.45)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: C.accent,
        ...font(900, 64),
        transform: `scale(${p})`,
        opacity: life,
      }}
    >
      {n}
    </div>
  );
};

// ---------------------------------------------------------------- images

// White-frame photo that drops in with a tilt (pair with camera-shutter). src is relative to public/.
export const Polaroid: React.FC<{
  src: string;
  label: string;
  start: number;
  end: number;
  x: number;
  y: number;
  w: number;
  h: number;
  rot: number;
  credit?: string;
}> = ({ src, label, start, end, x, y, w, h, rot, credit }) => {
  const life = useLife(start, end);
  const p = usePop(start, 11);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w + 36,
        padding: "18px 18px 0 18px",
        background: "#FAFAF7",
        boxShadow: "0 24px 50px rgba(0,0,0,0.6)",
        transform: `translateY(${(1 - p) * -500}px) rotate(${rot + (1 - p) * -20}deg) scale(${interpolate(p, [0, 1], [1.25, 1])})`,
        opacity: life,
      }}
    >
      <Img src={staticFile(src)} style={{ width: w, height: h, objectFit: "cover", display: "block" }} />
      <div style={{ ...font(800, 30), color: "#1b1b1b", textAlign: "center", padding: "16px 0 18px", letterSpacing: 0 }}>{label}</div>
      {credit && (
        <div style={{ position: "absolute", right: 24, top: h - 6, fontFamily: MONTSERRAT, fontSize: 13, color: "rgba(255,255,255,0.85)", textShadow: "0 1px 3px rgba(0,0,0,0.9)" }}>
          {credit}
        </div>
      )}
    </div>
  );
};

// Rounded photo card with a label chip, slow Ken Burns. Used inside Panels for real-photo comparisons.
export const PhotoCard: React.FC<{ src: string; label: string; x: number; y: number; w: number; h: number; start: number; end: number; highlight?: boolean }> = ({
  src,
  label,
  x,
  y,
  w,
  h,
  start,
  end,
  highlight,
}) => {
  const frame = useCurrentFrame();
  const kb = interpolate(frame, [start, end], [1.04, 1.14], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        borderRadius: 18,
        overflow: "hidden",
        border: `3px solid ${highlight ? C.accent : "rgba(255,255,255,0.85)"}`,
        boxShadow: "0 10px 24px rgba(0,0,0,0.45)",
      }}
    >
      <Img src={staticFile(src)} style={{ width: w, height: h, objectFit: "cover", transform: `scale(${kb})` }} />
      <div style={{ position: "absolute", left: 12, bottom: 10, background: "rgba(14,10,16,0.78)", color: highlight ? C.accent : C.white, padding: "6px 14px", borderRadius: 10, ...font(900, 28) }}>
        {label}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- containers & shades

// Dark rounded panel that rises into the lower band (pair with quick-swoosh).
export const Panel: React.FC<{ start: number; end: number; y: number; h: number; children: React.ReactNode }> = ({ start, end, y, h, children }) => {
  const life = useLife(start, end, 7);
  const p = usePop(start, 14);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: 50,
        width: 900,
        top: y,
        height: h,
        borderRadius: 30,
        background: "rgba(22,17,26,0.84)",
        border: "2px solid rgba(255,90,174,0.55)",
        boxShadow: "0 20px 50px rgba(0,0,0,0.45)",
        transform: `translateY(${(1 - p) * 120}px) scale(${0.92 + 0.08 * p})`,
        opacity: life * Math.min(1, p * 1.6),
        overflow: "hidden",
      }}
    >
      {children}
    </div>
  );
};

// Darkens the top band (titles over the shelf) — frames.
export const TopShade: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, start + 6, end - 6, end], [0, 1, 1, 0], clamp);
  if (!o) return null;
  return <AbsoluteFill style={{ opacity: o, background: "linear-gradient(180deg, rgba(14,10,16,0.82) 0%, rgba(14,10,16,0.55) 20%, rgba(0,0,0,0) 34%)" }} />;
};

// Darkens the bottom band so gold/pink reads over busy footage — frames.
export const BottomShade: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, start + 3, end - 4, end], [0, 1, 1, 0], clamp);
  if (!o) return null;
  return <AbsoluteFill style={{ opacity: o, background: "linear-gradient(0deg, rgba(14,10,16,0.85) 0%, rgba(14,10,16,0.7) 22%, rgba(0,0,0,0) 38%)" }} />;
};

// Animated gold line, e.g. crossing out a myth in the hook. d = SVG path in frame pixels.
export const StrikeLine: React.FC<{ d: string; start: number; end: number; width?: number; length?: number }> = ({ d, start, end, width = 16, length = 600 }) => {
  const frame = useCurrentFrame();
  if (frame < start || frame >= end) return null;
  const draw = interpolate(frame, [start, start + 5], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const fade = interpolate(frame, [end - 6, end], [1, 0], clamp);
  return (
    <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, opacity: fade }}>
      <path d={d} stroke={C.gold} strokeWidth={width} strokeLinecap="round" fill="none" strokeDasharray={length} strokeDashoffset={length * (1 - draw)} />
    </svg>
  );
};

// Hand-drawn pointer line from a label to a real object in the footage (pair with chirp-like/pop).
export const CalloutLine: React.FC<{ d: string; tip: [number, number]; start: number; end: number }> = ({ d, tip, start, end }) => {
  const frame = useCurrentFrame();
  const life = useLife(start, end);
  if (!life) return null;
  const draw = interpolate(frame, [start + 4, start + 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, opacity: life }}>
      <path d={d} stroke={C.accent} strokeWidth={7} fill="none" strokeLinecap="round" strokeDasharray="700" strokeDashoffset={700 * (1 - draw)} />
      <circle cx={tip[0]} cy={tip[1]} r={14 * draw} fill={C.accent} />
    </svg>
  );
};

// 2x2 checklist inside a Panel; items appear at their own seconds (pair each with quick-ting, last with correct).
export const CheckGrid: React.FC<{ items: [string, number][]; start: number; end: number; y: number }> = ({ items, start, end, y }) => {
  const frame = useCurrentFrame();
  return (
    <Panel start={start} end={end} y={y} h={300}>
      {items.map(([label, at], i) => {
        const p = spring({ frame: frame - Math.round(at * FPS), fps: FPS, config: { damping: 12, stiffness: 180 } });
        if (frame < Math.round(at * FPS)) return null;
        const x = 50 + (i % 2) * 430;
        const yy = 50 + Math.floor(i / 2) * 120;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: yy, display: "flex", alignItems: "center", transform: `scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 80, height: 80, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 44), boxShadow: "0 0 22px rgba(255,90,174,0.5)" }}>✓</div>
            <div style={{ marginLeft: 22, ...font(900, 52), color: C.white }}>{label}</div>
          </div>
        );
      })}
    </Panel>
  );
};

// Small top-left series tag ("Mẹo chọn thảm · Louis Yoga") — frames.
export const SeriesTag: React.FC<{ start: number; end: number; tag: string; brand: string }> = ({ start, end, tag, brand }) => {
  const frame = useCurrentFrame();
  const p = usePop(start, 14);
  if (frame < start || frame >= end) return null;
  return (
    <div style={{ position: "absolute", left: 48, top: 150, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -420}px)` }}>
      <div style={{ background: C.pinkDeep, color: C.white, ...font(900, 30), padding: "10px 20px", borderRadius: 8, letterSpacing: 1 }}>{tag}</div>
      <div style={{ marginLeft: 12, color: C.white, ...font(800, 28), letterSpacing: 2, textShadow: "0 2px 8px rgba(0,0,0,0.8)" }}>{brand}</div>
    </div>
  );
};

// ---------------------------------------------------------------- impacts

// Screen shake + white flash on the heaviest hits: [time s, frames, amplitude px, flash opacity].
export type Impact = [number, number, number, number];

export const useImpact = (impacts: Impact[]) => {
  const frame = useCurrentFrame();
  let dx = 0;
  let dy = 0;
  let flash = 0;
  for (const [t, len, amp, fl] of impacts) {
    const d = frame - Math.round(t * FPS);
    if (d >= 0 && d < len) {
      const k = 1 - d / len;
      dx += (rnd(frame * 3 + 1) - 0.5) * 2 * amp * k;
      dy += (rnd(frame * 7 + 2) - 0.5) * 2 * amp * k;
    }
    if (fl > 0 && d >= 0 && d < 4) flash = Math.max(flash, fl * (1 - d / 4));
  }
  return { dx, dy, flash };
};
