import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Easing,
  Freeze,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { MONTSERRAT, useMontserrat } from "../shared/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// "Documentary explainer" look learned from the reference reel
// (facebook.com/reel/1763428218100789): charcoal ground, accent + white heavy caps,
// stamps for numbers, polaroid photo drops, torn-paper edges, vertical whip-blur
// transitions, an SFX on almost every graphic beat and a continuous music bed.
// Footage: public/reel2/clean.mp4 = the Louis Yoga talk with fillers cut (see gen_data.py).

const FPS = 30;
const W = 1080;
const H = 1920;
const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 36; // hold on the CTA after the speech ends
const DURATION = VIDEO_FRAMES + TAIL;

// The source has a burned-in pink card from y≈1060; we only show the clean top part.
const WIN_H = 1062;

// Louis Yoga tone: hot pink accent + gold (from the brand card's gold rim and lotus), on a wine-tinted charcoal.
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

// Deterministic pseudo-random (no Math.random in compositions).
export const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

export const font = (weight: number, size: number): React.CSSProperties => ({
  fontFamily: MONTSERRAT,
  fontWeight: weight,
  fontSize: size,
  lineHeight: 1.05,
  textTransform: "uppercase",
  letterSpacing: -1,
});

// ---------------------------------------------------------------- helpers

export const usePop = (start: number, damping = 12) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - start, fps, config: { damping, stiffness: 180, mass: 0.7 } });
};

// Visible window [start, end) in frames with a short fade out.
export const useLife = (start: number, end: number, out = 6) => {
  const frame = useCurrentFrame();
  if (frame < start || frame >= end) return 0;
  return interpolate(frame, [end - out, end], [1, 0], clamp);
};

const faceAt = (t: number): [number, number] => {
  let best = FACE[0];
  for (const s of FACE) {
    if (Math.abs(s[0] - t) < Math.abs(best[0] - t)) best = s;
  }
  return [best[1], best[2]];
};

// ---------------------------------------------------------------- video window

// Punch-ins: [start s, end s, zoom]. Ramp in 6 frames, hold, ramp out 8 frames.
const PUNCHES: [number, number, number][] = [
  [0.0, 2.6, 1.1],
  [4.95, 5.95, 1.12],
  [14.85, 15.85, 1.1],
  [19.9, 20.85, 1.1],
  [25.7, 28.2, 1.18],
  [32.15, 33.0, 1.1],
  [37.0, 38.7, 1.12],
];

const WHIP_HALF = 4; // frames on each side of a cut

const VideoWindow: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;

  let zoom = 1;
  for (const [a, b, z] of PUNCHES) {
    const s = f(a);
    const e = f(b);
    if (frame >= s && frame < e + 8) {
      zoom = interpolate(frame, [s, s + 6, e, e + 8], [1, z, z, 1], {
        ...clamp,
        easing: Easing.out(Easing.cubic),
      });
    }
  }
  // Slow drift so the frame never sits dead still.
  zoom *= interpolate(frame, [0, DURATION], [1.02, 1.06]);
  const [fx, fy] = faceAt(Math.min(t, CLEAN_DURATION - 0.1));

  // Vertical whip at cuts: old shot leaves downward, new shot drops in from above.
  let dy = 0;
  let blur = 0;
  for (const c of CUTS) {
    const cf = f(c);
    const d = frame - cf;
    if (d >= -WHIP_HALF && d < WHIP_HALF) {
      const p = d < 0 ? (d + WHIP_HALF) / WHIP_HALF : 1 - d / WHIP_HALF;
      dy = d < 0 ? p * p * 260 : -p * p * 260;
      blur = p;
    }
  }

  // Only the main copy carries the voice; the whip ghost copies are muted.
  // The inner clip moves with the shot, so the burned-in card below WIN_H never shows during a whip.
  const videoEl = (offset: number, opacity: number, muted: boolean) => (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: W,
        height: WIN_H,
        overflow: "hidden",
        transform: `translateY(${dy + offset}px)`,
        opacity,
      }}
    >
      <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: `${fx}px ${Math.min(fy, 700)}px` }}>
        {frame < VIDEO_FRAMES ? (
          <OffthreadVideo src={staticFile("reel2/clean.mp4")} muted={muted} style={{ width: W, height: H }} />
        ) : (
          <Freeze frame={VIDEO_FRAMES - 1}>
            <OffthreadVideo src={staticFile("reel2/clean.mp4")} muted style={{ width: W, height: H }} />
          </Freeze>
        )}
      </AbsoluteFill>
    </div>
  );

  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: W, height: WIN_H, overflow: "hidden" }}>
      {videoEl(0, 1, false)}
      {blur > 0.05 && videoEl(-90 * blur, 0.45, true)}
      {blur > 0.05 && videoEl(90 * blur, 0.45, true)}
      {/* grade: slight contrast + vignette toward the documentary look */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)",
        }}
      />
      <AbsoluteFill
        style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 18%)" }}
      />
    </div>
  );
};

// Torn paper strip separating the footage from the graphics ground.
const tornPath = (y: number, amp: number, seed: number, down: boolean) => {
  const pts: string[] = [];
  const n = 54;
  for (let i = 0; i <= n; i++) {
    const x = (i / n) * W;
    const yy = y + (rnd(seed + i) - 0.5) * amp + (i % 2 ? amp * 0.25 : 0);
    pts.push(`${x.toFixed(1)},${yy.toFixed(1)}`);
  }
  return down
    ? `M0,${H} L${pts.join(" L")} L${W},${H} Z`
    : `M0,0 L${pts.join(" L")} L${W},0 Z`;
};

const TornEdge: React.FC = () => (
  <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
    <path d={tornPath(1018, 22, 3, true)} fill={C.paper} />
    <path d={tornPath(1046, 18, 91, true)} fill={C.ink} />
  </svg>
);

// ---------------------------------------------------------------- ground

const Ground: React.FC = () => {
  const frame = useCurrentFrame();
  const lines = [];
  for (let i = 0; i < 9; i++) {
    const y0 = 1120 + i * 95;
    let d = `M-20,${y0}`;
    for (let x = 0; x <= W + 40; x += 40) {
      const y = y0 + Math.sin(x / 140 + i * 1.7 + frame / 90) * 18 + Math.sin(x / 57 + i) * 6;
      d += ` L${x},${y.toFixed(1)}`;
    }
    lines.push(<path key={i} d={d} stroke="rgba(255,90,174,0.06)" strokeWidth={2} fill="none" />);
  }
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 75%, #2B1D27 0%, ${C.ink} 70%)` }}>
      <svg width={W} height={H}>{lines}</svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- captions

const CAP_Y = 1095;

const Captions: React.FC<{ hideUntil: number }> = ({ hideUntil }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t < hideUntil || t >= 39.55) return null;
  const line = CAPTIONS.find((l) => t >= l.start - 0.05 && t < l.end + 0.15);
  if (!line) return null;
  const enter = interpolate(t, [line.start - 0.05, line.start + 0.08], [0, 1], clamp);
  return (
    <div
      style={{
        position: "absolute",
        top: CAP_Y,
        left: 50,
        right: 50,
        textAlign: "center",
        transform: `translateY(${(1 - enter) * 18}px)`,
        opacity: enter,
      }}
    >
      {line.words.map((w, i) => {
        const active = t >= w.s - 0.03 && t < w.e + 0.05;
        const said = t >= w.s;
        return (
          <span
            key={i}
            style={{
              ...font(900, 64),
              display: "inline-block",
              margin: "0 10px",
              color: active ? C.accent : said ? C.white : C.dim,
              transform: `scale(${active ? 1.08 : 1})`,
              textShadow: "0 4px 0 rgba(0,0,0,0.65), 0 0 18px rgba(0,0,0,0.5)",
            }}
          >
            {w.w}
          </span>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------- graphic atoms

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
        <div
          key={i}
          style={{ ...font(900, l.size), color: l.color, textShadow: "0 6px 0 rgba(0,0,0,0.55)" }}
        >
          {l.text}
        </div>
      ))}
    </div>
  );
};

export const Polaroid: React.FC<{
  img: string;
  label: string;
  start: number;
  end: number;
  x: number;
  y: number;
  w: number;
  h: number;
  rot: number;
  credit?: string;
}> = ({ img, label, start, end, x, y, w, h, rot, credit }) => {
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
      <Img src={staticFile(`reel2/img/${img}`)} style={{ width: w, height: h, objectFit: "cover", display: "block" }} />
      <div style={{ ...font(800, 30), color: "#1b1b1b", textAlign: "center", padding: "16px 0 18px", letterSpacing: 0 }}>
        {label}
      </div>
      {credit && (
        <div style={{ position: "absolute", right: 24, top: h - 6, fontFamily: MONTSERRAT, fontSize: 13, color: "rgba(255,255,255,0.85)", textShadow: "0 1px 3px rgba(0,0,0,0.9)" }}>
          {credit}
        </div>
      )}
    </div>
  );
};

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
        boxShadow: `0 0 26px rgba(255,90,174,0.45)`,
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

// ---------------------------------------------------------------- scenes

const G = 1300; // top of the graphics area under the captions

const HookScene: React.FC = () => (
  <>
    <BigText
      start={0}
      end={f(2.65)}
      y={G - 120}
      slam
      lines={[
        { text: "Thảm nào", color: C.white, size: 132 },
      ]}
    />
    <BigText
      start={f(0.75)}
      end={f(2.65)}
      y={G + 30}
      slam
      lines={[
        { text: "hút mồ hôi", color: C.accent, size: 110 },
        { text: "tốt nhất?", color: C.accent, size: 110 },
      ]}
    />
  </>
);

const MaterialScene: React.FC = () => (
  <>
    <Polaroid img="rubber_latex.jpg" label="Mủ cao su tự nhiên" credit="Ảnh: V. Argenberg · CC BY 4.0" start={f(2.85)} end={f(6.1)} x={70} y={G} w={360} h={360} rot={-6} />
    <Kicker text="chất liệu" start={f(2.75)} end={f(6.1)} y={G + 30} color={C.dim} left={490} right={20} />
    <div style={{ position: "absolute", left: 480, right: 0, top: G + 90 }}>
      <BigText start={f(3.1)} end={f(6.1)} y={0} lines={[{ text: "Cao su", color: C.white, size: 88 }, { text: "tự nhiên", color: C.accent, size: 76 }]} />
    </div>
    <Pill text="✓ Thấm hút tốt" start={f(5.0)} end={f(6.1)} x={760} y={G + 300} />
  </>
);

// Video window overlay while the speaker walks out of frame (raw 8–11s).
const HotYogaOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(6.1);
  const e = f(12.2);
  if (frame < s || frame >= e) return null;
  const scrim = interpolate(frame, [s, s + 6, e - 5, e], [0, 0.78, 0.78, 0], clamp);
  const thermoStart = f(9.6);
  const level = interpolate(frame, [thermoStart, f(11.38)], [0.15, 0.95], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const thermoIn = interpolate(frame, [thermoStart - 6, thermoStart + 4], [0, 1], clamp);
  const drops = [];
  for (let i = 0; i < 12; i++) {
    const t0 = f(8.25) + i * 3;
    const y = interpolate(frame, [t0, t0 + 40], [-60, WIN_H + 60], clamp);
    if (frame < t0) continue;
    drops.push(
      <svg key={i} width={34} height={48} style={{ position: "absolute", left: 80 + rnd(i) * 900, top: y, opacity: 0.8 }}>
        <path d="M17 2 C 17 2, 2 22, 2 31 a15 15 0 0 0 30 0 C 32 22, 17 2, 17 2 Z" fill={i % 3 ? "#9EDCFF" : C.white} />
      </svg>,
    );
  }
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: W, height: WIN_H, overflow: "hidden" }}>
      <AbsoluteFill style={{ background: `rgba(10,10,10,${scrim})` }} />
      {frame >= f(8.25) && frame < f(11.3) && drops}
      <BigText start={f(6.25)} end={f(8.2)} y={330} lines={[{ text: "Khi tập luyện", color: C.white, size: 96 }, { text: "vận động mạnh", color: C.accent, size: 96 }]} />
      <BigText start={f(8.25)} end={f(9.55)} y={360} slam lines={[{ text: "Ra nhiều", color: C.white, size: 120 }, { text: "mồ hôi", color: C.accent, size: 130 }]} />
      {/* thermometer */}
      <div style={{ position: "absolute", left: 170, top: 210, opacity: thermoIn, transform: `scale(${0.7 + 0.3 * thermoIn})` }}>
        <svg width={150} height={600} viewBox="0 0 150 600">
          <rect x={45} y={10} width={60} height={470} rx={30} fill="#fff" stroke="#222" strokeWidth={6} />
          <rect x={60} y={20 + 450 * (1 - level)} width={30} height={450 * level} rx={15} fill="#FF3B5C" />
          <circle cx={75} cy={520} r={65} fill="#FF3B5C" stroke="#fff" strokeWidth={10} />
          {[0, 1, 2, 3, 4, 5, 6].map((i) => (
            <rect key={i} x={110} y={60 + i * 60} width={26} height={6} fill="#fff" />
          ))}
        </svg>
      </div>
      <Pill text={`${Math.round(interpolate(level, [0.15, 0.95], [28, 40]))}°C`} start={f(9.7)} end={f(12.2)} x={620} y={300} bg={C.white} fg={C.ink} size={70} />
      <Stamp text="Hot yoga" start={f(11.38)} end={f(12.2)} x={620} y={560} rot={-8} size={104} />
    </div>
  );
};

const ThicknessScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(12.3);
  const e = f(15.9);
  const life = useLife(s, e);
  if (!life) return null;
  const grow = interpolate(frame, [f(14.85), f(15.25)], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  const inA = interpolate(frame, [s, s + 8], [0, 1], clamp);
  const slab = (label: string, thick: number, color: string, y: number, o: number) => (
    <div style={{ position: "absolute", left: 120, top: y, opacity: o }}>
      <div style={{ width: 620, height: thick, background: color, borderRadius: 10, boxShadow: "0 12px 26px rgba(0,0,0,0.5)" }} />
      <div style={{ position: "absolute", left: 650, top: thick / 2 - 26, ...font(900, 48), color, whiteSpace: "nowrap" }}>{label}</div>
    </div>
  );
  return (
    <div style={{ opacity: life }}>
      <Kicker text="chọn thảm có" start={s} end={e} y={G - 10} color={C.dim} />
      <BigText start={s + 4} end={e} y={G + 45} lines={[{ text: "Độ dày tốt hơn", color: C.white, size: 76 }]} />
      {slab("Mỏng", 18, "#8a8a8a", G + 190, inA)}
      {slab("Dày hơn", 18 + 52 * grow, C.accent, G + 250, Math.min(1, grow * 3))}
    </div>
  );
};

const ChoiceScene: React.FC = () => (
  <>
    {/* choice 1: regular practitioners — blue mat */}
    <NumberCircle n="1" start={f(15.95)} end={f(20.9)} x={560} y={G - 20} />
    <Polaroid img="mat_basic_blue.jpg" label="Basic · 5 mm" start={f(17.55)} end={f(20.9)} x={80} y={G - 30} w={330} h={420} rot={-5} />
    <Kicker text="tham khảo mẫu" start={f(16.6)} end={f(20.9)} y={G + 110} color={C.dim} left={460} right={20} />
    <div style={{ position: "absolute", left: 480, right: 40, top: G + 170 }}>
      <BigText start={f(18.85)} end={f(20.9)} y={0} lines={[{ text: "Người tập", color: C.white, size: 64 }, { text: "thường xuyên", color: C.accent, size: 64 }]} />
    </div>
    {/* choice 2: beginners — black mat */}
    <NumberCircle n="2" start={f(20.95)} end={f(23.45)} x={560} y={G - 20} />
    <Polaroid img="mat_asana_black.jpg" label="Asana · 4,5 mm" start={f(21.05)} end={f(23.45)} x={80} y={G - 30} w={330} h={420} rot={5} />
    <div style={{ position: "absolute", left: 480, right: 40, top: G + 150 }}>
      <BigText start={f(21.5)} end={f(23.45)} y={0} slam lines={[{ text: "Người", color: C.white, size: 72 }, { text: "mới tập", color: C.accent, size: 80 }]} />
    </div>
  </>
);

const CounterScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(23.5);
  const e = f(29.55);
  const life = useLife(s, e);
  if (!life) return null;
  const v = interpolate(frame, [f(24.4), f(25.95)], [0, 4.5], { ...clamp, easing: Easing.out(Easing.cubic) });
  const done = frame >= f(25.95);
  const bump = done ? interpolate(frame, [f(25.95), f(26.15)], [1.15, 1], clamp) : 1;
  const ticks = [];
  for (let i = 0; i <= 10; i++) {
    const on = i / 10 <= v / 4.5 + 0.001 && frame >= f(24.4);
    ticks.push(
      <div
        key={i}
        style={{
          position: "absolute",
          left: 140 + i * 72,
          top: i % 5 === 0 ? 0 : 14,
          width: 8,
          height: i % 5 === 0 ? 56 : 32,
          background: on ? C.accent : "rgba(255,255,255,0.25)",
          borderRadius: 4,
        }}
      />,
    );
  }
  return (
    <div style={{ opacity: life }}>
      <Kicker text="thảm asana · độ dày" start={s} end={e} y={G - 10} color={C.dim} />
      <div
        style={{
          position: "absolute",
          top: G + 30,
          left: 0,
          right: 0,
          textAlign: "center",
          transform: `scale(${bump})`,
          opacity: interpolate(frame, [s, s + 6], [0, 1], clamp),
        }}
      >
        <span style={{ ...font(900, 230), color: C.accent, letterSpacing: -6, textShadow: "0 0 40px rgba(255,90,174,0.35)" }}>
          {v.toFixed(1).replace(".", ",")}
        </span>
        <span style={{ ...font(900, 110), color: C.white, marginLeft: 18 }}>ly</span>
      </div>
      <div style={{ position: "absolute", top: G + 300, left: 0, width: W }}>{ticks}</div>
      <Stamp text="Vừa đủ" start={f(27.7)} end={e} x={790} y={G + 270} rot={-10} size={72} />
      <Pill text="Thậm chí còn dư!" start={f(28.55)} end={e} x={W / 2} y={G + 400} bg={C.white} fg={C.ink} size={48} />
    </div>
  );
};

const FeatureScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(29.6);
  const e = f(36.3);
  const life = useLife(s, e);
  if (!life) return null;
  const items: [string, number][] = [
    ["Êm ái", 32.2],
    ["Thấm hút mồ hôi", 33.0],
    ["Bám sàn · bám tay", 35.1],
  ];
  const lineH = interpolate(frame, [f(32.2), f(35.3)], [0, 230], clamp);
  return (
    <div style={{ opacity: life }}>
      <BigText start={s + 3} end={e} y={G - 20} lines={[{ text: "Bề mặt thảm cần", color: C.white, size: 64 }]} />
      <div style={{ position: "absolute", left: 172, top: G + 110, width: 6, height: lineH, background: C.accent, borderRadius: 3 }} />
      {items.map(([label, at], i) => {
        const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
        if (frame < f(at)) return null;
        return (
          <div key={i} style={{ position: "absolute", left: 130, top: G + 90 + i * 115, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -80}px)`, opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 90, height: 90, borderRadius: 999, background: C.ink, border: `6px solid ${C.accent}`, display: "flex", alignItems: "center", justifyContent: "center", color: C.accent, ...font(900, 50), transform: `scale(${p})` }}>✓</div>
            <div style={{ marginLeft: 30, ...font(900, 62), color: i === 2 ? C.accent : C.white }}>{label}</div>
          </div>
        );
      })}
    </div>
  );
};

const BrandScene: React.FC = () => {
  const s = f(36.35);
  const e = f(39.55);
  const life = useLife(s, e);
  const p = usePop(f(36.95), 10);
  if (!life) return null;
  return (
    <div style={{ opacity: life }}>
      <div style={{ position: "absolute", left: W / 2 - 110, top: G - 30, transform: `scale(${p}) rotate(${(1 - p) * -90}deg)`, borderRadius: 999, boxShadow: "0 0 50px rgba(215,33,130,0.55)" }}>
        <Img src={staticFile("reel2/img/lotus.png")} style={{ width: 220, height: 220 }} />
      </div>
      <BigText start={f(37.0)} end={e} y={G + 210} lines={[{ text: "Louis Yoga", color: C.white, size: 96 }]} />
      <Pill text="Đáp ứng đủ cả 3" start={f(38.4)} end={e} x={W / 2} y={G + 330} />
    </div>
  );
};

const EndCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(39.55);
  if (frame < s) return null;
  const scrim = interpolate(frame, [s, s + 8], [0, 0.82], clamp);
  return (
    <>
      <AbsoluteFill style={{ background: `rgba(14,14,14,${scrim})` }} />
      <div style={{ position: "absolute", left: W / 2 - 100, top: 360, transform: `scale(${interpolate(frame, [s, s + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) })})` }}>
        <Img src={staticFile("reel2/img/lotus.png")} style={{ width: 200, height: 200 }} />
      </div>
      <Kicker text="muốn chọn đúng thảm?" start={s + 4} end={DURATION + 1} y={640} />
      <BigText start={s + 8} end={DURATION + 1} y={720} slam lines={[{ text: "Follow", color: C.white, size: 120 }, { text: "Louis Yoga", color: C.accent, size: 120 }]} />
      <Pill text="Xem thêm mẹo chọn thảm" start={s + 16} end={DURATION + 1} x={W / 2} y={1040} bg={C.gold} fg={C.ink} size={44} />
    </>
  );
};

// Persistent series tag (like the reference's date/location label).
const SeriesTag: React.FC = () => {
  const frame = useCurrentFrame();
  const p = usePop(6, 14);
  if (frame >= f(39.55)) return null;
  return (
    <div style={{ position: "absolute", left: 48, top: 150, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -400}px)` }}>
      <div style={{ background: C.pinkDeep, color: C.white, ...font(900, 30), padding: "10px 20px", borderRadius: 8, letterSpacing: 1 }}>Mẹo chọn thảm</div>
      <div style={{ marginLeft: 12, color: C.white, ...font(800, 28), letterSpacing: 2, textShadow: "0 2px 8px rgba(0,0,0,0.8)" }}>Louis Yoga</div>
    </div>
  );
};

// ---------------------------------------------------------------- audio

type Cue = [number, string, number]; // [time s where the hit should land, file, volume]

// Onset of each file (seconds of lead-in before the transient), measured with ffmpeg.
export const ONSET: Record<string, number> = {
  "swoosh.mp3": 0.07,
  "quick-swoosh.mp3": 0.04,
  "pop.mp3": 0.23,
  "pop-2.mp3": 0.066,
  "punch.mp3": 0.107,
  "riser-metallic.mp3": 1.809,
  "camera-shutter.mp3": 0.04,
  "digital-counting-1.mp3": 0.063,
  "ding.mp3": 0.149,
  "quick-ting.mp3": 0.019,
  "correct.mp3": 0.079,
};

const CUES: Cue[] = [
  // hook
  [0.0, "swoosh.mp3", 0.55],
  [0.07, "punch.mp3", 0.75],
  [0.2, "pop-2.mp3", 0.35],
  [0.8, "punch.mp3", 0.6],
  [2.667, "swoosh.mp3", 0.45],
  [2.9, "camera-shutter.mp3", 0.55],
  [3.15, "pop-2.mp3", 0.4],
  [5.0, "quick-ting.mp3", 0.45],
  [6.1, "quick-swoosh.mp3", 0.5],
  [6.3, "pop-2.mp3", 0.35],
  [8.25, "punch.mp3", 0.55],
  [11.38, "riser-metallic.mp3", 0.4],
  [11.38, "punch.mp3", 0.9],
  [12.2, "swoosh.mp3", 0.5],
  [14.88, "pop-2.mp3", 0.5],
  [15.9, "swoosh.mp3", 0.45],
  [15.98, "pop.mp3", 0.45],
  [17.6, "camera-shutter.mp3", 0.55],
  [18.067, "swoosh.mp3", 0.3],
  [18.9, "quick-ting.mp3", 0.4],
  [20.9, "quick-swoosh.mp3", 0.45],
  [21.0, "pop.mp3", 0.45],
  [21.55, "punch.mp3", 0.5],
  [22.9, "camera-shutter.mp3", 0.5],
  [23.433, "swoosh.mp3", 0.4],
  [24.4, "digital-counting-1.mp3", 0.45],
  [24.9, "digital-counting-1.mp3", 0.45],
  [25.4, "digital-counting-1.mp3", 0.45],
  [25.95, "ding.mp3", 0.4],
  [27.7, "punch.mp3", 0.85],
  [28.267, "swoosh.mp3", 0.3],
  [28.6, "pop-2.mp3", 0.45],
  [29.65, "quick-swoosh.mp3", 0.4],
  [32.2, "quick-ting.mp3", 0.45],
  [33.0, "quick-ting.mp3", 0.45],
  [35.1, "correct.mp3", 0.4],
  [36.3, "swoosh.mp3", 0.4],
  [36.95, "pop.mp3", 0.5],
  [38.4, "pop-2.mp3", 0.45],
  [39.55, "quick-swoosh.mp3", 0.5],
  [39.85, "punch.mp3", 0.7],
  [40.1, "ding.mp3", 0.35],
];

const SoundLayer: React.FC = () => (
  <>
    <Audio
      src={staticFile("reel2/music_inspired.mp3")}
      volume={(fr) => interpolate(fr, [0, 4, f(2.6), f(3.2), VIDEO_FRAMES, VIDEO_FRAMES + 8, DURATION - 12, DURATION], [0, 0.22, 0.22, 0.14, 0.14, 0.32, 0.32, 0], clamp)}
    />
    {CUES.map(([t, file, vol], i) => {
      const from = Math.max(0, f(t - (ONSET[file] ?? 0)));
      return (
        <Sequence key={i} from={from} durationInFrames={f(3)} layout="none">
          <Audio src={staticFile(`reel2/sfx/${file}`)} volume={vol} />
        </Sequence>
      );
    })}
  </>
);

// ---------------------------------------------------------------- root

export const LouisYogaReel2: React.FC = () => {
  useMontserrat();
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Ground />
      <VideoWindow />
      <HotYogaOverlay />
      <TornEdge />
      <SeriesTag />
      <Captions hideUntil={2.65} />
      <HookScene />
      <MaterialScene />
      <ThicknessScene />
      <ChoiceScene />
      <CounterScene />
      <FeatureScene />
      <BrandScene />
      <EndCTA />
      <SoundLayer />
    </AbsoluteFill>
  );
};

export const LouisYogaReel2Composition: React.FC = () => (
  <Composition
    id="LouisYogaReel2"
    component={LouisYogaReel2}
    durationInFrames={DURATION}
    fps={FPS}
    width={W}
    height={H}
  />
);
