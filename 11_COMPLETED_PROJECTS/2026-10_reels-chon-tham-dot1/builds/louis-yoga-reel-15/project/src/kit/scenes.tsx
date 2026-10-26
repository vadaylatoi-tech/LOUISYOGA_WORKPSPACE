import React from "react";
import { Easing, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { Panel } from "./atoms";
import { C, clamp, f, font, FPS } from "./theme";

// Ready-made scene blocks proven on reels 01–02 (approved). All times in SECONDS.
// Product avatars: crop the web avatars (white bg, mat in the middle) to public/img/<model>.jpg, 440x920:
//   Image.crop((w*.27, h*.02, w*.73, h*.98)).resize((440, 920)) — see references/03 "Ảnh".

// Real Louis Yoga product card that pops in at `at`; optional label under it; `line` (s) draws a pink
// guide over the centre line of the mat (e.g. Aura's single straight line).
export const MatCard: React.FC<{ src: string; label?: string; x: number; y: number; w: number; h: number; at: number; active?: boolean; line?: number; labelSize?: number }> = ({
  src,
  label,
  x,
  y,
  w,
  h,
  at,
  active,
  line,
  labelSize = 26,
}) => {
  const frame = useCurrentFrame();
  if (frame < f(at)) return null;
  const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
  const draw = line === undefined ? 0 : interpolate(frame, [f(line), f(line) + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, transform: `translateY(${(1 - p) * 60}px) scale(${0.7 + 0.3 * p})`, opacity: Math.min(1, p * 2) }}>
      <div
        style={{
          position: "relative",
          width: w,
          height: h,
          borderRadius: 12,
          overflow: "hidden",
          background: "#F2F0EC",
          border: `3px solid ${active ? C.accent : "rgba(255,255,255,0.85)"}`,
          boxShadow: active ? "0 0 26px rgba(255,90,174,0.55)" : "0 8px 18px rgba(0,0,0,0.45)",
        }}
      >
        <Img src={staticFile(src)} style={{ width: w, height: h, objectFit: "cover" }} />
        {draw > 0 && <div style={{ position: "absolute", left: w / 2 - 4, top: h * 0.06, width: 8, height: h * 0.88 * draw, borderRadius: 4, background: C.accent, boxShadow: `0 0 14px ${C.accent}` }} />}
      </div>
      {label && <div style={{ ...font(900, labelSize), color: active ? C.accent : C.white, textAlign: "center", marginTop: 8, letterSpacing: 0 }}>{label}</div>}
    </div>
  );
};

// Conclusion panel that answers the hook: title + rows "✓ need → pick" appearing at their seconds
// (pair rows with quick-ting, the last with correct). Keep `need` ≤ 13 chars and `pick` ≤ 13 chars.
export const RecapRows: React.FC<{ title: string; rows: [string, string, number][]; start: number; end: number; y: number; footer?: [string, number] }> = ({
  title,
  rows,
  start,
  end,
  y,
  footer,
}) => {
  const frame = useCurrentFrame();
  const h = 110 + rows.length * 96 + (footer ? 40 : 0);
  return (
    <Panel start={f(start)} end={f(end)} y={y} h={h}>
      <div style={{ position: "absolute", top: 18, left: 0, right: 0, textAlign: "center", ...font(900, 34), color: C.accent, letterSpacing: 2 }}>{title}</div>
      {rows.map(([need, pick, at], i) => {
        if (frame < f(at)) return null;
        const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
        return (
          <div key={need} style={{ position: "absolute", left: 44, top: 82 + i * 96, display: "flex", alignItems: "center", transform: `scale(${0.7 + 0.3 * p})`, transformOrigin: "left center", opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 66, height: 66, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 36), boxShadow: "0 0 18px rgba(255,90,174,0.5)" }}>✓</div>
            <div style={{ marginLeft: 18, width: 330, ...font(900, 40), color: C.white }}>{need}</div>
            <div style={{ ...font(900, 40), color: C.dim }}>→</div>
            <div style={{ marginLeft: 16, ...font(900, 42), color: C.gold }}>{pick}</div>
          </div>
        );
      })}
      {footer && frame >= f(footer[1]) && (
        <div style={{ position: "absolute", bottom: 16, left: 0, right: 0, textAlign: "center", ...font(800, 28), color: C.white, letterSpacing: 2 }}>{footer[0]}</div>
      )}
    </Panel>
  );
};

// Numbered criteria rows ("Chọn theo: 1 … 2 …") inside a panel.
export const NumberRows: React.FC<{ title: string; rows: [string, number][]; start: number; end: number; y: number }> = ({ title, rows, start, end, y }) => {
  const frame = useCurrentFrame();
  return (
    <Panel start={f(start)} end={f(end)} y={y} h={90 + rows.length * 104}>
      <div style={{ position: "absolute", top: 22, left: 0, right: 0, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>{title}</div>
      {rows.map(([label, at], i) => {
        if (frame < f(at)) return null;
        const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
        return (
          <div key={label} style={{ position: "absolute", left: 110, top: 80 + i * 104, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -80}px)`, opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 80, height: 80, borderRadius: 99, border: `5px solid ${C.accent}`, display: "flex", alignItems: "center", justifyContent: "center", color: C.accent, ...font(900, 44) }}>{i + 1}</div>
            <div style={{ marginLeft: 26, ...font(900, 56), color: i % 2 ? C.gold : C.white }}>{label}</div>
          </div>
        );
      })}
    </Panel>
  );
};

// Do / don't checklist ("Lưu ý"): rows [text, seconds, ok]; ok=true → pink ✓, false → dark ✕ (pair ✓ with quick-ting, ✕ with pop).
export const DoDont: React.FC<{ title: string; rows: [string, number, boolean][]; start: number; end: number; y: number; size?: number }> = ({ title, rows, start, end, y, size = 42 }) => {
  const frame = useCurrentFrame();
  const h = 90 + rows.length * 84;
  return (
    <Panel start={f(start)} end={f(end)} y={y} h={h}>
      <div style={{ position: "absolute", top: 16, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.gold, letterSpacing: 2 }}>{title}</div>
      {rows.map(([text, at, ok], i) => {
        if (frame < f(at)) return null;
        const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
        return (
          <div key={text} style={{ position: "absolute", left: 50, top: 74 + i * 84, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -60}px)`, opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 60, height: 60, borderRadius: 99, background: ok ? C.pinkDeep : "#3A3340", border: ok ? "none" : "3px solid rgba(255,255,255,0.5)", display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 34) }}>{ok ? "✓" : "✕"}</div>
            <div style={{ marginLeft: 22, ...font(900, size), color: ok ? C.white : "rgba(255,255,255,0.75)", textDecoration: ok ? "none" : "line-through", textDecorationColor: C.accent }}>{text}</div>
          </div>
        );
      })}
    </Panel>
  );
};
