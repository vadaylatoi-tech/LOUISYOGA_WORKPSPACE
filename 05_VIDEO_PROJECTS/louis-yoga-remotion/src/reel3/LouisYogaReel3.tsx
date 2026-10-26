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
  getInputProps,
  useCurrentFrame,
} from "remotion";
import { MONTSERRAT, useMontserrat } from "../shared/useMontserrat";
import {
  BigText,
  C,
  clamp,
  f,
  font,
  Kicker,
  ONSET,
  Pill,
  Polaroid,
  rnd,
  Stamp,
  useLife,
  usePop,
} from "../reel2/LouisYogaReel2";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// Reel 3 — "Thảm càng dày càng tốt? Chưa chắc" (source: Video ngắn - thảm yoga/05).
// Same documentary look as reel 2 (pink + gold), but the footage is NOT covered:
// it stays full-bleed, cuts are hidden by alternating zoom levels, B-roll from the
// Louis Yoga brand film fills the frame, and graphics live only in the shelf band
// above the head or the table band below the held mat.

const FPS = 30;
const W = 1080;
const H = 1920;
const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54;
const DURATION = VIDEO_FRAMES + TAIL;

// Audio stems: "all" (preview), "sfx" or "music" (rendered separately and mixed with the
// processed voice in ffmpeg so the voice always sits on top).
const STEM = ((getInputProps() as { stem?: string }).stem ?? "all") as "all" | "sfx" | "music" | "none";

const CAP_Y = 1196; // just under the mat she holds
const G = 1330; // top of the lower graphics band (table / towels)

// ---------------------------------------------------------------- talking head

// Base zoom per segment between cuts: alternating tight/wide hides every jump cut.
const SEG_ZOOM = [1.22, 1.1, 1.28, 1.14, 1.3, 1.16, 1.26, 1.12, 1.24, 1.14, 1.2];

// Emphasis punch-ins on top of the segment zoom: [start s, end s, extra zoom].
const PUNCHES: [number, number, number][] = [
  [1.45, 2.2, 0.22],
  [2.25, 3.45, 0.1],
  [6.36, 8.45, 0.08],
  [16.8, 17.7, 0.12],
  [30.68, 31.6, 0.14],
  [43.4, 45.0, 0.1],
];

// Moments where the camera moves off the face onto the mat she is holding.
const MAT_FOCUS: [number, number, number, number, number][] = [
  // [start s, end s, x, y, zoom]
  [36.75, 39.35, 600, 960, 1.42],
];

const faceAt = (t: number): [number, number] => {
  if (t <= FACE[0][0]) return [FACE[0][1], FACE[0][2]];
  for (let i = 1; i < FACE.length; i++) {
    if (FACE[i][0] >= t) {
      const [t0, x0, y0] = FACE[i - 1];
      const [t1, x1, y1] = FACE[i];
      const k = (t - t0) / Math.max(0.001, t1 - t0);
      return [x0 + (x1 - x0) * k, y0 + (y1 - y0) * k];
    }
  }
  const last = FACE[FACE.length - 1];
  return [last[1], last[2]];
};

const segIndex = (t: number) => {
  let i = 0;
  while (i < CUTS.length && t >= CUTS[i]) i++;
  return i;
};

const TalkingHead: React.FC = () => {
  const frame = useCurrentFrame();
  const t = Math.min(frame, VIDEO_FRAMES - 1) / FPS;

  let zoom = SEG_ZOOM[segIndex(t)];
  for (const [a, b, z] of PUNCHES) {
    if (frame >= f(a) && frame < f(b) + 8) {
      zoom += interpolate(frame, [f(a), f(a) + 5, f(b), f(b) + 8], [0, z, z, 0], {
        ...clamp,
        easing: Easing.out(Easing.cubic),
      });
    }
  }
  let [ox, oy] = faceAt(t);
  for (const [a, b, mx, my, mz] of MAT_FOCUS) {
    const k = interpolate(frame, [f(a), f(a) + 9, f(b) - 6, f(b)], [0, 1, 1, 0], {
      ...clamp,
      easing: Easing.inOut(Easing.cubic),
    });
    if (k > 0) {
      ox += (mx - ox) * k;
      oy += (my - oy) * k;
      zoom += (mz - zoom) * k;
    }
  }
  // Tail: slow push while the CTA holds.
  if (frame >= VIDEO_FRAMES) zoom += interpolate(frame, [VIDEO_FRAMES, DURATION], [0, 0.06], clamp);

  // Zoom-blur at each cut (the reference's map "zoom punch"): ghost copies scaled up.
  let ghost = 0;
  for (const c of CUTS) {
    const d = frame - f(c);
    if (d >= 0 && d < 4) ghost = 1 - d / 4;
  }

  const layer = (z: number, opacity: number, muted: boolean) => (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: `${ox}px ${oy}px`, opacity }}>
      {frame < VIDEO_FRAMES ? (
        <OffthreadVideo src={staticFile("reel3/clean.mp4")} muted={muted} style={{ width: W, height: H }} />
      ) : (
        <Freeze frame={VIDEO_FRAMES - 1}>
          <OffthreadVideo src={staticFile("reel3/clean.mp4")} muted style={{ width: W, height: H }} />
        </Freeze>
      )}
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {layer(zoom, 1, STEM !== "all")}
      {ghost > 0.05 && layer(zoom * (1 + 0.06 * ghost), 0.35 * ghost, true)}
      {ghost > 0.05 && layer(zoom * (1 + 0.12 * ghost), 0.25 * ghost, true)}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- B-roll

type Broll = { start: number; end: number; film: number; cx: number; label: string };

// Cutaways from the Louis Yoga brand film (public/reel3/brand_film.mp4, 30fps, silent).
// film = source second; cx = horizontal subject centre in the 1920px-wide film.
const BROLL: Broll[] = [
  { start: 9.3, end: 12.25, film: 17.2, cx: 820, label: "Bài tập nâng cao" },
  { start: 12.75, end: 14.15, film: 7.3, cx: 860, label: "Quỳ gối" },
  { start: 14.15, end: 15.35, film: 58.3, cx: 1000, label: "Tì tay" },
  { start: 39.4, end: 41.0, film: 20.1, cx: 760, label: "Bài tập nâng cao" },
  { start: 49.3, end: 51.2, film: 70.3, cx: 900, label: "An tâm khi tập" },
];

const FILM_SCALE = H / 1080;
const FILM_W = 1920 * FILM_SCALE;

const BrollShot: React.FC<{ b: Broll }> = ({ b }) => {
  const frame = useCurrentFrame(); // local to the Sequence
  const len = f(b.end) - f(b.start);
  const push = interpolate(frame, [0, len], [1.04, 1.12]);
  // Horizontal whip in / out with ghost copies (the film is far wider than the frame, so no edge shows).
  const dx = interpolate(frame, [0, 5, len - 4, len], [520, 0, 0, -520], {
    ...clamp,
    easing: Easing.inOut(Easing.quad),
  });
  const moving = Math.abs(dx) > 8;
  const left = W / 2 - b.cx * FILM_SCALE;
  const shot = (offset: number, opacity: number) => (
    <AbsoluteFill style={{ transform: `translateX(${dx + offset}px) scale(${push})`, opacity }}>
      <OffthreadVideo
        src={staticFile("reel3/brand_film.mp4")}
        startFrom={f(b.film)}
        muted
        style={{ position: "absolute", left, top: 0, width: FILM_W, height: H }}
      />
    </AbsoluteFill>
  );
  const lp = usePop(3, 14);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {shot(0, 1)}
      {moving && shot(dx * 0.25, 0.4)}
      {moving && shot(dx * 0.5, 0.25)}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)" }} />
      <div
        style={{
          position: "absolute",
          left: 56,
          top: 250,
          display: "flex",
          alignItems: "center",
          transform: `translateX(${(1 - lp) * -300}px)`,
          opacity: lp,
        }}
      >
        <div style={{ width: 16, height: 16, borderRadius: 99, background: C.accent, marginRight: 14, boxShadow: `0 0 14px ${C.accent}` }} />
        <div style={{ ...font(900, 46), color: C.white, textShadow: "0 3px 10px rgba(0,0,0,0.6)" }}>{b.label}</div>
      </div>
    </AbsoluteFill>
  );
};

const BrollLayer: React.FC = () => (
  <>
    {BROLL.map((b, i) => (
      <Sequence key={i} from={f(b.start)} durationInFrames={f(b.end) - f(b.start)}>
        <BrollShot b={b} />
      </Sequence>
    ))}
  </>
);

// ---------------------------------------------------------------- captions

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t < 2.2 || t >= CLEAN_DURATION) return null;
  const line = CAPTIONS.find((l) => t >= l.start - 0.05 && t < l.end + 0.15);
  if (!line) return null;
  const enter = interpolate(t, [line.start - 0.05, line.start + 0.08], [0, 1], clamp);
  return (
    <div
      style={{
        position: "absolute",
        top: CAP_Y,
        left: 60,
        right: 60,
        textAlign: "center",
        transform: `translateY(${(1 - enter) * 16}px)`,
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
              ...font(900, 62),
              display: "inline-block",
              margin: "0 9px",
              color: active ? C.accent : said ? C.white : "rgba(255,255,255,0.72)",
              transform: `scale(${active ? 1.08 : 1})`,
              textShadow:
                "0 0 2px #000, 3px 3px 0 rgba(0,0,0,0.85), -2px -2px 0 rgba(0,0,0,0.85), 2px -2px 0 rgba(0,0,0,0.85), -2px 2px 0 rgba(0,0,0,0.85), 0 8px 20px rgba(0,0,0,0.6)",
            }}
          >
            {w.w}
          </span>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------- panels

const Panel: React.FC<{ start: number; end: number; y: number; h: number; children: React.ReactNode }> = ({
  start,
  end,
  y,
  h,
  children,
}) => {
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

// Foam texture for the TPE slab (deterministic bubbles).
const Bubbles: React.FC<{ w: number; h: number; seed: number }> = ({ w, h, seed }) => (
  <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0 }}>
    {Array.from({ length: 26 }).map((_, i) => (
      <circle key={i} cx={rnd(seed + i) * w} cy={rnd(seed + i + 50) * h} r={3 + rnd(seed + i + 99) * 7} fill="rgba(255,255,255,0.35)" />
    ))}
  </svg>
);

// 2.25–8.6s: rubber 4,5–5 ly vs TPE 6·8·9 ly.
const CompareScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(2.25);
  const e = f(8.6);
  const tpeIn = interpolate(frame, [f(4.3), f(4.3) + 8], [0, 1], clamp);
  const tpeThick = interpolate(frame, [f(6.36), f(6.6), f(7.36), f(7.6), f(8.06), f(8.3)], [40, 60, 60, 80, 80, 92], clamp);
  const tpeNum = frame < f(7.36) ? "6" : frame < f(8.06) ? "8" : "9";
  return (
    <Panel start={s} end={e} y={G} h={320}>
      {/* rubber */}
      <div style={{ position: "absolute", left: 40, top: 28, width: 380 }}>
        <div style={{ ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Cao su</div>
        <div style={{ marginTop: 6 }}>
          <span style={{ ...font(900, 92), color: C.accent }}>4,5–5</span>
          <span style={{ ...font(900, 46), color: C.white, marginLeft: 10 }}>ly</span>
        </div>
        <div style={{ marginTop: 22, width: 340, height: 30, borderRadius: 8, background: `linear-gradient(180deg, ${C.accent}, ${C.pinkDeep})`, boxShadow: "0 8px 18px rgba(0,0,0,0.4)" }} />
      </div>
      <div style={{ position: "absolute", left: 425, top: 110, ...font(900, 40), color: C.gold }}>VS</div>
      {/* TPE */}
      <div style={{ position: "absolute", left: 510, top: 28, width: 360, opacity: tpeIn, transform: `translateX(${(1 - tpeIn) * 60}px)` }}>
        <div style={{ ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Thảm TPE</div>
        <div style={{ marginTop: 6 }}>
          <span style={{ ...font(900, 92), color: C.white }}>{frame < f(6.36) ? "6–9" : tpeNum}</span>
          <span style={{ ...font(900, 46), color: C.white, marginLeft: 10 }}>ly</span>
        </div>
        <div
          style={{
            position: "relative",
            marginTop: 22,
            width: 340,
            height: tpeThick,
            borderRadius: 10,
            background: "linear-gradient(180deg, #CDB8E6, #9C86C4)",
            boxShadow: "0 8px 18px rgba(0,0,0,0.4)",
            overflow: "hidden",
          }}
        >
          <Bubbles w={340} h={tpeThick} seed={7} />
        </div>
      </div>
    </Panel>
  );
};

// 18.2–33.0s: real photos (foam mat vs Louis Yoga rubber rolls, DSC00985 product shot) + a sink gauge.
// Foam photo: "Yoga mat.jpg" by Gausanchennai, Wikimedia Commons, CC BY-SA 4.0.
const PressScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(18.2);
  const e = f(33.05);
  const press = (at: number) =>
    interpolate(frame, [f(at), f(at) + 7, f(at) + 22, f(at) + 30], [0, 1, 1, 0], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const p = Math.max(press(25.5), press(26.4), press(30.7));
  const card = (x: number, img: string, label: string, sink: number, thick: number, foam: boolean, hi: boolean) => {
    const dent = sink * p;
    const kb = interpolate(frame, [s, e], [1.04, 1.14]);
    return (
      <div style={{ position: "absolute", left: x, top: 56, width: 390 }}>
        <div style={{ position: "relative", width: 390, height: 190, borderRadius: 18, overflow: "hidden", border: `3px solid ${hi ? C.accent : "rgba(255,255,255,0.85)"}`, boxShadow: "0 10px 24px rgba(0,0,0,0.45)" }}>
          <Img src={staticFile(`reel3/img/${img}`)} style={{ width: 390, height: 190, objectFit: "cover", transform: `scale(${kb})` }} />
          <div style={{ position: "absolute", left: 12, bottom: 10, background: "rgba(14,10,16,0.78)", color: hi ? C.accent : C.white, padding: "6px 14px", borderRadius: 10, ...font(900, 28) }}>{label}</div>
        </div>
        <svg width={390} height={110} style={{ position: "absolute", left: 0, top: 200 }}>
          <defs>
            <linearGradient id={`pg${x}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor={foam ? "#E3C3D6" : C.accent} />
              <stop offset="1" stopColor={foam ? "#A98399" : C.pinkDeep} />
            </linearGradient>
          </defs>
          <path d={`M6,14 L140,14 C165,14 165,${14 + dent} 195,${14 + dent} C225,${14 + dent} 225,14 250,14 L384,14 L384,${14 + thick} L6,${14 + thick} Z`} fill={`url(#pg${x})`} />
          {foam &&
            Array.from({ length: 18 }).map((_, i) => (
              <circle key={i} cx={16 + rnd(i + 3) * 360} cy={20 + dent * 0.4 + rnd(i + 40) * Math.max(4, thick - 14 - dent * 0.4)} r={2 + rnd(i + 77) * 5} fill="rgba(255,255,255,0.4)" />
            ))}
          <path d={`M195,0 L195,${4 + dent}`} stroke={C.white} strokeWidth={4} />
          <path d={`M186,${dent - 6} L195,${dent + 6} L204,${dent - 6}`} stroke={C.white} strokeWidth={4} fill="none" opacity={p} />
        </svg>
      </div>
    );
  };
  const tpeHi = frame >= f(22.1) && frame < f(23.4);
  return (
    <Panel start={s} end={e} y={G - 20} h={360}>
      <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(800, 28), color: C.dim, letterSpacing: 4 }}>Khi quỳ gối · tì tay</div>
      {card(40, "foam_mat.jpg", "TPE foam", 52, 80, true, tpeHi)}
      {card(470, "rubber_rolls.jpg", "Cao su 5 ly", 6, 34, false, false)}
      <Pill text="Độ nén thấp" start={f(19.6)} end={e} x={150} y={66} bg="rgba(14,10,16,0.8)" fg={C.white} size={24} />
      <Pill text="6–9 ly" start={f(28.85)} end={e} x={358} y={66} bg={C.white} fg={C.ink} size={26} />
      <Stamp text="Dễ lún!" start={f(30.75)} end={e} x={235} y={150} rot={-10} size={66} />
      <Pill text="✓ Ổn định" start={f(31.6)} end={e} x={760} y={66} size={26} />
      <div style={{ position: "absolute", right: 14, bottom: 6, fontFamily: MONTSERRAT, fontSize: 12, color: "rgba(255,255,255,0.45)" }}>Ảnh foam: Gausanchennai · CC BY-SA 4.0</div>
    </Panel>
  );
};

// 33.35–38.4s: call-out on the real mat she is holding.
const MatCallout: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(33.35);
  const e = f(38.45);
  const life = useLife(s, e);
  if (!life) return null;
  const draw = interpolate(frame, [s + 4, s + 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ opacity: life }}>
      <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d="M300,1395 C250,1300 330,1200 470,1080" stroke={C.accent} strokeWidth={7} fill="none" strokeLinecap="round" strokeDasharray="700" strokeDashoffset={700 * (1 - draw)} />
        <circle cx={470} cy={1080} r={14 * draw} fill={C.accent} />
      </svg>
      <div style={{ position: "absolute", left: 60, top: G + 70 }}>
        <Pill text="Thảm Basic · cao su 5 mm" start={s + 2} end={e} x={330} y={0} size={38} />
        <Pill text="Độ nén chắc" start={f(36.5)} end={e} x={250} y={92} bg={C.gold} fg={C.ink} size={38} />
      </div>
    </div>
  );
};

const AdviceTitle: React.FC = () => (
  <>
    <Kicker text="tập nâng cao thì nên chọn" start={f(41.1)} end={f(46.1)} y={G + 10} color={C.white} />
    <BigText start={f(43.45)} end={f(46.1)} y={G + 70} slam lines={[{ text: "Độ nén chắc", color: C.accent, size: 110 }]} />
  </>
);

const Checklist: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(46.15);
  const e = f(54.35);
  const items: [string, number][] = [
    ["Thoải mái", 46.2],
    ["Ổn định", 47.36],
    ["An tâm", 52.0],
    ["Hiệu quả", 52.64],
  ];
  return (
    <Panel start={s} end={e} y={G} h={300}>
      {items.map(([label, at], i) => {
        const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
        if (frame < f(at)) return null;
        const x = 50 + (i % 2) * 430;
        const y = 50 + Math.floor(i / 2) * 120;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, display: "flex", alignItems: "center", transform: `scale(${0.6 + 0.4 * p})`, opacity: Math.min(1, p * 2) }}>
            <div style={{ width: 80, height: 80, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 44), boxShadow: `0 0 22px rgba(255,90,174,0.5)` }}>✓</div>
            <div style={{ marginLeft: 22, ...font(900, 52), color: C.white }}>{label}</div>
          </div>
        );
      })}
    </Panel>
  );
};

// ---------------------------------------------------------------- hook + CTA

const TopShade: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, start + 6, end - 6, end], [0, 1, 1, 0], clamp);
  if (!o) return null;
  return <AbsoluteFill style={{ opacity: o, background: "linear-gradient(180deg, rgba(14,10,16,0.82) 0%, rgba(14,10,16,0.55) 20%, rgba(0,0,0,0) 34%)" }} />;
};

// Dark band behind the hook stamp so gold reads over the pastel towels.
const BottomShade: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [start, start + 3, end - 4, end], [0, 1, 1, 0], clamp);
  if (!o) return null;
  return <AbsoluteFill style={{ opacity: o, background: "linear-gradient(0deg, rgba(14,10,16,0.85) 0%, rgba(14,10,16,0.7) 22%, rgba(0,0,0,0) 38%)" }} />;
};

// Hook beats: title slam (0s) → "càng tốt?" slam (0.55s) → riser → the myth is crossed out and
// "CHƯA CHẮC!" drops with a boom, flash, shake and a hard punch-in on her face (1.45s).
const HOOK_DROP = 1.45;

const Strike: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(HOOK_DROP);
  if (frame < s || frame >= f(4.1)) return null;
  const draw = interpolate(frame, [s, s + 5], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const fade = interpolate(frame, [f(4.1) - 6, f(4.1)], [1, 0], clamp);
  return (
    <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, opacity: fade }}>
      <path d="M250,330 L830,282" stroke={C.gold} strokeWidth={16} strokeLinecap="round" strokeDasharray="600" strokeDashoffset={600 * (1 - draw)} />
    </svg>
  );
};

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(4.1)} />
    <BigText start={0} end={f(4.1)} y={120} slam lines={[{ text: "Thảm càng dày", color: C.white, size: 100 }]} />
    <BigText start={f(0.55)} end={f(4.1)} y={230} slam lines={[{ text: "càng tốt?", color: C.accent, size: 124 }]} />
    <Strike />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.3)} />
    <Stamp text="Chưa chắc!" start={f(HOOK_DROP)} end={f(2.3)} x={540} y={G + 140} rot={-8} size={136} />
  </>
);

// Screen shake + white flash on the heaviest hits: [time s, frames, amplitude px, flash opacity].
const IMPACTS: [number, number, number, number][] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [30.75, 7, 9, 0],
  [43.45, 5, 7, 0],
];

const useImpact = () => {
  const frame = useCurrentFrame();
  let dx = 0;
  let dy = 0;
  let flash = 0;
  for (const [t, len, amp, fl] of IMPACTS) {
    const d = frame - f(t);
    if (d >= 0 && d < len) {
      const k = 1 - d / len;
      dx += (rnd(frame * 3 + 1) - 0.5) * 2 * amp * k;
      dy += (rnd(frame * 7 + 2) - 0.5) * 2 * amp * k;
    }
    if (fl > 0 && d >= 0 && d < 4) flash = Math.max(flash, fl * (1 - d / 4));
  }
  return { dx, dy, flash };
};

const SeriesTag: React.FC = () => {
  const frame = useCurrentFrame();
  const p = usePop(f(4.15), 14);
  if (frame < f(4.15) || frame >= VIDEO_FRAMES) return null;
  return (
    <div style={{ position: "absolute", left: 48, top: 150, display: "flex", alignItems: "center", transform: `translateX(${(1 - p) * -420}px)` }}>
      <div style={{ background: C.pinkDeep, color: C.white, ...font(900, 30), padding: "10px 20px", borderRadius: 8, letterSpacing: 1 }}>Mẹo chọn thảm</div>
      <div style={{ marginLeft: 12, color: C.white, ...font(800, 28), letterSpacing: 2, textShadow: "0 2px 8px rgba(0,0,0,0.8)" }}>Louis Yoga</div>
    </div>
  );
};

const EndCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const s = VIDEO_FRAMES - 4;
  if (frame < s) return null;
  const dim = interpolate(frame, [s, s + 10], [0, 0.45], clamp);
  return (
    <>
      <AbsoluteFill style={{ background: `rgba(14,10,16,${dim})` }} />
      <TopShade start={s} end={DURATION + 20} />
      <div style={{ position: "absolute", left: W / 2 - 70, top: 100, transform: `scale(${interpolate(frame, [s, s + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) })})` }}>
        <Img src={staticFile("reel3/img/lotus.png")} style={{ width: 140, height: 140 }} />
      </div>
      <BigText start={s + 6} end={DURATION + 1} y={260} slam lines={[{ text: "Follow Louis Yoga", color: C.white, size: 84 }]} />
      <Kicker text="xem thêm mẹo chọn thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid img="mat_basic_blue.jpg" label="Basic · 5 mm" start={s + 8} end={DURATION + 1} x={90} y={G - 40} w={230} h={290} rot={-7} />
      <Polaroid img="mat_asana_black.jpg" label="Asana · 4,5 mm" start={s + 12} end={DURATION + 1} x={700} y={G - 30} w={230} h={290} rot={6} />
      <div style={{ position: "absolute", left: 360, right: 360, top: G + 90, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Cao su</div>
        <div style={{ ...font(900, 40), color: C.white }}>tự nhiên</div>
        <div style={{ ...font(900, 46), color: C.accent, marginTop: 8 }}>4,5–5 mm</div>
      </div>
    </>
  );
};

// ---------------------------------------------------------------- audio

type Cue = [number, string, number];

// SFX follow reel 2 (the user's reference for "enough, not overused"): the same 11 library sounds,
// ~0.65 sounding events per second, one sound per beat (no layering except riser→punch), quiet
// everyday ticks/pops and loud punches only on slams and stamps. Each effect keeps its own sound:
//   slam/stamp → punch   pill/label → pop   number → digital-counting   B-roll/panel → swoosh
//   ✓ → quick-ting, last ✓ → correct   polaroid → camera-shutter
const CUES: Cue[] = [
  // hook: slam, slam, riser into the "CHƯA CHẮC!" punch
  [0.0, "swoosh.mp3", 0.55],
  [0.05, "punch.mp3", 0.8],
  [0.58, "pop-2.mp3", 0.5],
  [1.45, "riser-metallic.mp3", 0.45],
  [1.45, "punch.mp3", 0.95],
  // rubber vs TPE
  [2.25, "quick-swoosh.mp3", 0.45],
  [4.3, "pop-2.mp3", 0.45],
  [6.36, "digital-counting-1.mp3", 0.45],
  [8.06, "digital-counting-1.mp3", 0.45],
  // B-roll
  [9.3, "swoosh.mp3", 0.5],
  [9.5, "punch.mp3", 0.75],
  [12.75, "quick-swoosh.mp3", 0.4],
  [14.15, "swoosh.mp3", 0.35],
  [16.8, "correct.mp3", 0.45],
  // press scene
  [18.2, "quick-swoosh.mp3", 0.45],
  [19.6, "pop.mp3", 0.4],
  [22.16, "quick-ting.mp3", 0.4],
  [28.85, "pop-2.mp3", 0.4],
  [30.75, "punch.mp3", 0.85],
  [31.6, "correct.mp3", 0.4],
  // callout on the real mat
  [33.45, "quick-swoosh.mp3", 0.4],
  [36.5, "pop-2.mp3", 0.45],
  // advice
  [39.4, "swoosh.mp3", 0.5],
  [43.45, "punch.mp3", 0.8],
  // checklist
  [46.2, "quick-ting.mp3", 0.45],
  [47.36, "quick-ting.mp3", 0.45],
  [49.3, "swoosh.mp3", 0.4],
  [52.0, "quick-ting.mp3", 0.45],
  [52.64, "correct.mp3", 0.45],
  // CTA
  [54.4, "quick-swoosh.mp3", 0.5],
  [54.65, "punch.mp3", 0.7],
  [54.9, "camera-shutter.mp3", 0.45],
  [55.2, "ding.mp3", 0.35],
];

// A cue lands its transient (ONSET) on time t; sounds whose lead-in is longer than t's distance from
// the clip start (the riser) are trimmed from the front instead of shifted late.
const SoundLayer: React.FC = () => (
  <>
    {(STEM === "all" || STEM === "music") && (
      <Audio
        src={staticFile("reel2/music_inspired.mp3")}
        volume={(fr) =>
          interpolate(fr, [0, 4, f(2.2), f(2.8), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION], [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0], clamp)
        }
      />
    )}
    {(STEM === "all" || STEM === "sfx") &&
      CUES.map(([t, file, vol], i) => {
        const lead = ONSET[file] ?? 0;
        const from = f(t - lead);
        return (
          <Sequence key={i} from={Math.max(0, from)} durationInFrames={f(3)} layout="none">
            <Audio src={staticFile(`reel2/sfx/${file}`)} startFrom={Math.max(0, -from)} volume={vol} />
          </Sequence>
        );
      })}
  </>
);

// ---------------------------------------------------------------- root

export const LouisYogaReel3: React.FC = () => {
  useMontserrat();
  const { dx, dy, flash } = useImpact();
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, fontFamily: MONTSERRAT }}>
      <AbsoluteFill style={{ transform: `translate(${dx}px, ${dy}px) scale(${dx || dy ? 1.03 : 1})` }}>
        <TalkingHead />
        <BrollLayer />
        <Hook />
        <SeriesTag />
        <CompareScene />
        <PressScene />
        <MatCallout />
        <AdviceTitle />
        <Checklist />
        <Stamp text="Chuẩn 5 ly" start={f(9.5)} end={f(12.25)} x={540} y={G + 150} rot={-6} size={96} />
        <Pill text="✓ Hạn chế lún thảm" start={f(16.8)} end={f(17.95)} x={W / 2} y={G + 110} size={46} />
        <Captions />
        <EndCTA />
      </AbsoluteFill>
      {flash > 0 && <AbsoluteFill style={{ background: "#fff", opacity: flash }} />}
      <SoundLayer />
    </AbsoluteFill>
  );
};

export const LouisYogaReel3Composition: React.FC = () => (
  <Composition id="LouisYogaReel3" component={LouisYogaReel3} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
);
