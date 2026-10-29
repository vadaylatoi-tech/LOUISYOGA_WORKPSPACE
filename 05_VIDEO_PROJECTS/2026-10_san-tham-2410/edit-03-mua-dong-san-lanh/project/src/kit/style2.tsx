import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { useLife, usePop } from "./atoms";
import { C, clamp, f, font, W } from "./theme";
import { MONTSERRAT } from "./useMontserrat";

// Louis Yoga reel style 2 — building blocks (first used on Săn thảm 24/10 · 03 "Mùa đông sàn lạnh", v5).
// Layout: every text that must be read stays in the Reels/TikTok safe zone x 108–886, y 269–1248.
// Technical/explainer parts become full-frame motion-graphic STAGES over the frosted footage
// (no grid backgrounds, no captions on a stage, content centred around y ≈ 830 via the stage's dy).

export const SAFE_L = 108;
export const SAFE_R = 886;
export const SAFE_CX = (SAFE_L + SAFE_R) / 2; // 497 — safe zone is shifted left (button column on the right)
export const CAP_Y = 1172; // one caption line, bottom edge ≈ 1245

// Dark gradient from the left edge so the left column reads over the wall/mats.
export const LeftShade: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, start + 6, end - 6, end], [0, 1, 1, 0], clamp);
  if (!o) return null;
  return <AbsoluteFill style={{ opacity: o, background: "linear-gradient(90deg, rgba(14,10,16,0.78) 0%, rgba(14,10,16,0.5) 30%, rgba(0,0,0,0) 52%)" }} />;
};

// Left-aligned slam title line in the left column (x from SAFE_L).
export const ColTitle: React.FC<{ text: string; color: string; size: number; start: number; end: number; y: number; slam?: boolean }> = ({ text, color, size, start, end, y, slam = true }) => {
  const life = useLife(start, end);
  const p = usePop(start, 10);
  if (!life) return null;
  const s = slam ? interpolate(p, [0, 1], [1.6, 1]) : interpolate(p, [0, 1], [0.6, 1]);
  return (
    <div style={{ position: "absolute", left: SAFE_L, top: y, transformOrigin: "0% 50%", transform: `scale(${s})`, opacity: life * Math.min(1, p * 2), ...font(900, size), color, whiteSpace: "nowrap", textShadow: "0 6px 0 rgba(0,0,0,0.55)" }}>
      {text}
    </div>
  );
};

// Panel kept inside the safe zone (kit Panel spans x 50–950).
export const SafePanel: React.FC<{ start: number; end: number; x: number; y: number; w: number; h: number; children: React.ReactNode }> = ({ start, end, x, y, w, h, children }) => {
  const life = useLife(start, end, 7);
  const p = usePop(start, 14);
  if (!life) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        borderRadius: 26,
        background: "rgba(22,17,26,0.84)",
        border: "2px solid rgba(255,90,174,0.55)",
        boxShadow: "0 20px 50px rgba(0,0,0,0.45)",
        transform: `translateX(${(1 - p) * -120}px) scale(${0.92 + 0.08 * p})`,
        opacity: life * Math.min(1, p * 1.6),
        overflow: "hidden",
      }}
    >
      {children}
    </div>
  );
};

export const MG_TOP = 290; // first line of a stage before its dy shift; keep the shifted block inside y 269–1248
export const WARM = "#F7A6CB";
export const ICY = "#8FD3FF";
export const FLOOR = "#4A5B72";

// Full-frame stage: circle wipe in, quick fade out. Background only — content is passed in.
export const MgStage: React.FC<{ start: number; end: number; dy: number; children: React.ReactNode }> = ({ start, end, dy, children }) => {
  const frame = useCurrentFrame();
  if (frame < start || frame >= end) return null;
  const r = interpolate(frame, [start, start + 9], [0, 120], { ...clamp, easing: Easing.out(Easing.cubic) });
  const o = interpolate(frame, [end - 6, end], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ clipPath: `circle(${r}% at 46% 45%)`, opacity: o }}>
      {/* the real shop stays behind, frosted (FrostFootage blurs the footage itself) — no generic grid */}
      <AbsoluteFill style={{ background: "rgba(24,16,28,0.5)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 70% 45% at 46% 44%, rgba(255,90,174,0.16) 0%, rgba(0,0,0,0) 70%)" }} />
      <AbsoluteFill style={{ transform: `translateY(${dy}px)` }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

// Centered stage title (inside the safe zone width 778).
export const MgTitle: React.FC<{ start: number; children: React.ReactNode; y?: number; size?: number }> = ({ start, children, y = MG_TOP, size = 60 }) => {
  const p = usePop(start, 12);
  return (
    <div style={{ position: "absolute", left: SAFE_L, width: SAFE_R - SAFE_L, top: y, textAlign: "center", ...font(900, size), color: C.white, transform: `translateY(${(1 - p) * -40}px)`, opacity: Math.min(1, p * 2), whiteSpace: "nowrap" }}>
      {children}
    </div>
  );
};

export const Snowflake: React.FC<{ x: number; y: number; r: number; o: number }> = ({ x, y, r, o }) => (
  <g opacity={o} stroke={ICY} strokeWidth={4} strokeLinecap="round">
    {[0, 60, 120].map((a) => {
      const dx = Math.cos((a * Math.PI) / 180) * r;
      const dy = Math.sin((a * Math.PI) / 180) * r;
      return <line key={a} x1={x - dx} y1={y - dy} x2={x + dx} y2={y + dy} />;
    })}
  </g>
);

// Cross-section: body on top, mat in the middle, cold floor below. Cold waves rise from the floor
// either THROUGH a thin mat into the body (body cools down) or are BLOCKED under a thick one.
export const Section: React.FC<{ x: number; y: number; w: number; matH: number; matLabel: string; through: boolean; flowFrom: number; start: number; dim?: string }> = ({
  x,
  y,
  w,
  matH,
  matLabel,
  through,
  flowFrom,
  start,
  dim,
}) => {
  const frame = useCurrentFrame();
  const grow = interpolate(frame, [start, start + 12], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  const bodyH = 150;
  const matY = bodyH + 22;
  const floorY = matY + matH + 14;
  const floorH = 86;
  const cold = through ? interpolate(frame, [flowFrom + 10, flowFrom + 70], [0, 1], clamp) : 0;
  const body = cold > 0 ? `color-mix(in srgb, ${ICY} ${Math.round(cold * 100)}%, ${WARM})` : WARM;
  const flowing = frame >= flowFrom;
  const top = through ? 46 : matY + matH + 6;
  const n = w > 500 ? 5 : 3;
  return (
    <svg width={W} height={1920} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
      <defs>
        <linearGradient id={`mat-${x}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={C.accent} />
          <stop offset="1" stopColor={C.pinkDeep} />
        </linearGradient>
      </defs>
      <g transform={`translate(${x}, ${y}) translate(${w / 2}, ${floorY}) scale(${0.85 + 0.15 * grow}) translate(${-w / 2}, ${-floorY})`} opacity={Math.min(1, grow * 1.5)}>
        {/* body */}
        <rect x={w * 0.1} y={0} width={w * 0.8} height={bodyH} rx={36} fill={body} />
        {!through && flowing && <rect x={w * 0.1 - 6} y={-6} width={w * 0.8 + 12} height={bodyH + 12} rx={42} fill="none" stroke={C.gold} strokeWidth={4} opacity={0.5 + 0.3 * Math.sin((frame - flowFrom) / 5)} />}
        <text x={w / 2} y={bodyH / 2 + 12} textAnchor="middle" fontFamily={MONTSERRAT} fontWeight={900} fontSize={w > 500 ? 40 : 30} fill={C.ink}>
          NGƯỜI TẬP
        </text>
        {/* mat */}
        <rect x={0} y={matY} width={w} height={matH} rx={Math.min(12, matH / 2)} fill={`url(#mat-${x})`} />
        {/* floor */}
        <rect x={0} y={floorY} width={w} height={floorH} rx={8} fill={FLOOR} />
        {Array.from({ length: Math.floor(w / 90) }).map((_, i) => (
          <line key={i} x1={(i + 1) * 90} y1={floorY} x2={(i + 1) * 90} y2={floorY + floorH} stroke="rgba(255,255,255,0.18)" strokeWidth={3} />
        ))}
        <text x={w / 2} y={floorY + floorH / 2 + 11} textAnchor="middle" fontFamily={MONTSERRAT} fontWeight={900} fontSize={w > 500 ? 32 : 26} fill="rgba(255,255,255,0.9)" letterSpacing={3}>
          SÀN LẠNH
        </text>
        {/* cold waves */}
        {flowing &&
          Array.from({ length: n }).map((_, i) => {
            const k = (((frame - flowFrom + i * 9) % 32) + 32) % 32 / 32;
            const cx = (w / (n + 1)) * (i + 1);
            const cy = interpolate(k, [0, 1], [floorY - 4, top]);
            const o = interpolate(k, [0, 0.15, 0.8, 1], [0, 1, 1, 0]);
            return (
              <g key={i} opacity={o} stroke={ICY} strokeWidth={6} fill="none" strokeLinecap="round">
                <path d={`M${cx},${cy + 30} q-10,-10 0,-18 q10,-8 0,-18`} />
                <path d={`M${cx - 11},${cy - 2} L${cx},${cy - 14} L${cx + 11},${cy - 2}`} />
              </g>
            );
          })}
        {/* blocked: little bursts under the mat */}
        {!through && flowing && (
          <g stroke={C.gold} strokeWidth={5} strokeLinecap="round" opacity={0.6 + 0.4 * Math.sin((frame - flowFrom) / 3)}>
            {Array.from({ length: n }).map((_, i) => {
              const cx = (w / (n + 1)) * (i + 1);
              const by = matY + matH + 4;
              return <path key={i} d={`M${cx - 18},${by + 6} L${cx - 8},${by} M${cx + 18},${by + 6} L${cx + 8},${by}`} />;
            })}
          </g>
        )}
        {/* mat label + thickness bracket */}
        {matH >= 40 ? (
          <text x={w / 2} y={matY + matH / 2 + 12} textAnchor="middle" fontFamily={MONTSERRAT} fontWeight={900} fontSize={w > 500 ? 34 : 26} fill={C.white}>
            {matLabel}
          </text>
        ) : (
          <g>
            <rect x={w / 2 - (matLabel.length * 9 + 26)} y={matY + matH / 2 - 22} width={matLabel.length * 18 + 52} height={44} rx={22} fill={C.white} />
            <text x={w / 2} y={matY + matH / 2 + 9} textAnchor="middle" fontFamily={MONTSERRAT} fontWeight={900} fontSize={24} fill={C.pinkDeep}>
              {matLabel}
            </text>
          </g>
        )}
        {dim && (
          <g stroke={C.gold} strokeWidth={4} fill="none">
            <path d={`M${w + 14},${matY} h14 v${matH} h-14`} />
            <text x={w + 40} y={matY + matH / 2 + 12} fontFamily={MONTSERRAT} fontWeight={900} fontSize={34} fill={C.gold} stroke="none">
              {dim}
            </text>
          </g>
        )}
      </g>
    </svg>
  );
};

// Footage frosted while a motion-graphic stage is up (blur ramps with the circle wipe).
export type MgWindow = [number, number]; // [start s, end s] of a stage

export const FrostFootage: React.FC<{ windows: MgWindow[]; children: React.ReactNode }> = ({ windows, children }) => {
  const frame = useCurrentFrame();
  const k = Math.max(0, ...windows.map(([a, b]) => interpolate(frame, [f(a), f(a) + 9, f(b) - 6, f(b)], [0, 1, 1, 0], clamp)));
  return <AbsoluteFill style={k ? { filter: `blur(${k * 38}px) brightness(${1 - 0.35 * k})`, transform: `scale(${1 + 0.08 * k})` } : undefined}>{children}</AbsoluteFill>;
};

// Captions centred on the safe zone (x 108–886), scaled a touch so 20-char lines fit on one line;
// hidden while a motion-graphic stage is on screen (the graphic carries the idea there).
export const CaptionsOffMg: React.FC<{ windows: MgWindow[]; children: React.ReactNode }> = ({ windows, children }) => {
  const frame = useCurrentFrame();
  const o = Math.min(1, ...windows.map(([a, b]) => interpolate(frame, [f(a) - 1, f(a) + 3, f(b) - 4, f(b)], [1, 0, 0, 1], clamp)));
  return (
    <div style={{ position: "absolute", left: SAFE_CX - 474, width: 948, top: 0, height: 1920, opacity: o, transform: "scale(0.94)", transformOrigin: `474px ${CAP_Y + 34}px` }}>
      {children}
    </div>
  );
};
