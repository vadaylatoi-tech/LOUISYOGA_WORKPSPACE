import React, { useEffect, useState } from "react";
import { AbsoluteFill, Composition, continueRender, delayRender, Easing, Img, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import spec from "./spec.json";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SANS = "BeVN";
const SERIF = "SerifVN";
type Shot = { name: string; clip: string; from: number; dur: number; a: string; b: string; ink?: number; tl?: number; tr?: number; ts?: number; ty?: number; tear?: number; mist?: number[]; td?: number };
type V = { style: string; trans: number; beat: number; total: number; framed: number; intro: number; cta: number; shots: Shot[] };

const useFonts = () => {
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => {
    const add = (fam: string, file: string, weight: string, style = "normal") => new FontFace(fam, `url(${staticFile("fonts/" + file)})`, { weight, style }).load().then((f) => document.fonts.add(f));
    Promise.all([add(SANS, "BeVietnamPro-Light.ttf", "300"), add(SANS, "BeVietnamPro-Medium.ttf", "500"), add(SANS, "BeVietnamPro-Bold.ttf", "700"), add(SANS, "BeVietnamPro-ExtraBold.ttf", "800"), add(SERIF, "cambriai.ttf", "400", "italic")]).then(() => continueRender(h));
  }, [h]);
};

const SHADOW = "0 1px 3px rgba(0,0,0,0.45)"; // crisp only: no smudge under the text
const INK = "#2A2230";

// Clip with a slow push; a beat-cut style gets a short punch at the head of the shot.
const Clip: React.FC<{ s: Shot; style: string; len: number }> = ({ s, style, len }) => {
  const fr = useCurrentFrame();
  const push = interpolate(fr, [0, len], [1.02, 1.09], clamp);
  const punch = style === "beat" ? interpolate(fr, [0, 5], [0.05, 0], { ...clamp, easing: Easing.out(Easing.cubic) }) : 0;
  return (
    <AbsoluteFill style={{ transform: `scale(${push + punch})` }}>
      <OffthreadVideo src={staticFile(s.clip)} muted style={{ width: 1080, height: 1920 }} />
    </AbsoluteFill>
  );
};

// Word-by-word on the beat: each word lands with a small pop.
const BeatText: React.FC<{ s: Shot; beatF: number }> = ({ s, beatF }) => {
  const fr = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = s.a.split(" ");
  const out = interpolate(fr, [s.dur - 5, s.dur - 1], [1, 0], clamp);
  const bStart = Math.round(beatF * Math.max(1, words.length));
  const bp = spring({ frame: fr - bStart, fps, config: { damping: 16, stiffness: 160 } });
  return (
    <div style={{ position: "absolute", left: 90, right: 90, top: 420, textAlign: "center", opacity: out }}>
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, lineHeight: 1.12, color: "#fff", textShadow: SHADOW, letterSpacing: -2 }}>
        {words.map((w, i) => {
          const at = Math.round(i * beatF);
          const p = spring({ frame: fr - at, fps, config: { damping: 11, stiffness: 240 } });
          return <span key={i} style={{ display: "inline-block", margin: "0 12px", opacity: fr >= at ? 1 : 0, transform: `translateY(${(1 - p) * 34}px) scale(${0.72 + 0.28 * p})` }}>{w}</span>;
        })}
      </div>
      {s.b && <div style={{ marginTop: 10, fontFamily: SANS, fontWeight: 500, fontSize: 50, color: "#FFE9CC", textShadow: SHADOW, opacity: bp, transform: `translateY(${(1 - bp) * 18}px)` }}>{s.b}</div>}
    </div>
  );
};

// Letters appear one by one at TF frames each (spec.py places a key sound on each); layout stays fixed.
const TF = 2.2;
const Typed: React.FC<{ text: string; at: number }> = ({ text, at }) => {
  const fr = useCurrentFrame();
  return (
    <>
      {Array.from(text.normalize("NFC")).map((ch, i) => (
        <span key={i} style={{ opacity: interpolate(fr, [at + i * TF, at + i * TF + 2], [0, 1], clamp) }}>{ch}</span>
      ))}
    </>
  );
};

// Slow, breathing: serif line typed on; small spaced line follows.
const BreathText: React.FC<{ s: Shot }> = ({ s }) => {
  const fr = useCurrentFrame();
  const at = s.td ?? 4;
  const at2 = at + s.a.normalize("NFC").length * TF + 6;
  const out = interpolate(fr, [s.dur - 14, s.dur - 2], [1, 0], clamp);
  const ts = s.ts ?? 1;
  return (
    <div style={{ position: "absolute", left: s.tl ?? 90, right: s.tr ?? 90, top: s.ty ?? 420, textAlign: "center", opacity: out }}>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", whiteSpace: "nowrap", fontSize: 112 * ts, lineHeight: 1.15, color: s.ink ? INK : "#FFF3DF", textShadow: s.ink ? "none" : SHADOW }}><Typed text={s.a} at={at} /></div>
      {s.b && <div style={{ marginTop: 16, fontFamily: SANS, fontWeight: 500, fontSize: 44 * Math.max(0.85, ts), letterSpacing: 5, color: s.ink ? INK : "#fff", textTransform: "uppercase", textShadow: s.ink ? "none" : SHADOW }}><Typed text={s.b} at={at2} /></div>}
    </div>
  );
};

// Typed out letter by letter with a caret; the second line fades in under a hairline.
const TypeText: React.FC<{ s: Shot }> = ({ s }) => {
  const fr = useCurrentFrame();
  const n = Math.min(s.a.length, Math.floor(fr / 1.4));
  const done = n >= s.a.length;
  const start = s.a.length * 1.4;
  const line = interpolate(fr, [start, start + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const out = interpolate(fr, [s.dur - 9, s.dur - 1], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: 90, right: 90, top: 430, textAlign: "center", opacity: out }}>
      <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 80, lineHeight: 1.15, color: "#fff", textShadow: SHADOW }}>
        {s.a.slice(0, n)}
        <span style={{ opacity: !done || Math.floor(fr / 8) % 2 ? 1 : 0, marginLeft: 4 }}>|</span>
      </div>
      {s.b && (
        <>
          <div style={{ margin: "18px auto 0", width: 300 * line, height: 3, background: "#fff", boxShadow: SHADOW }} />
          <div style={{ marginTop: 16, fontFamily: SANS, fontWeight: 500, fontSize: 42, color: "#fff", textShadow: SHADOW, opacity: line }}>{s.b}</div>
        </>
      )}
    </div>
  );
};

const Badge: React.FC<{ end: number }> = ({ end }) => {
  const fr = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: fr - 4, fps, config: { damping: 15, stiffness: 150 } });
  const o = interpolate(fr, [end - 12, end], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: 90, top: 262, display: "flex", alignItems: "center", height: 104, padding: "0 34px 0 14px", borderRadius: 60, background: "rgba(250,244,234,0.93)", boxShadow: "0 8px 26px rgba(0,0,0,0.28)", opacity: o, transform: `translateX(${(1 - p) * -60}px)` }}>
      <Img src={staticFile("lotus.png")} style={{ width: 78, height: 78, marginRight: 14 }} />
      <div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, lineHeight: 1.05, color: "#261E28", letterSpacing: 1 }}>YOGALIFE</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 21, color: "#BE2878", letterSpacing: 2 }}>REVIEW SẢN PHẨM</div>
      </div>
    </div>
  );
};

const CTA: React.FC<{ style: string; len: number }> = ({ style, len }) => {
  const fr = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = (at: number) => spring({ frame: fr - at, fps, config: { damping: 14, stiffness: 170 } });
  const dim = interpolate(fr, [0, 14], [0, 0.42], clamp);
  const out = interpolate(fr, [len - 16, len - 1], [1, 0], clamp);
  const title = style === "breath" ? { fontFamily: SERIF, fontStyle: "italic", fontSize: 104, fontWeight: 400 } : { fontFamily: SANS, fontSize: 88, fontWeight: 800 };
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <AbsoluteFill style={{ background: `rgba(18,13,20,${dim})` }} />
      <div style={{ position: "absolute", left: 90, right: 90, top: 400, textAlign: "center" }}>
        <Img src={staticFile("lotus.png")} style={{ width: 150, height: 150, transform: `scale(${pop(6)})` }} />
        <div style={{ ...title, marginTop: 14, color: "#fff", textShadow: SHADOW, opacity: pop(12) } as React.CSSProperties}>Thảm Louis Yoga</div>
        <div style={{ margin: "34px auto 0", display: "inline-block", padding: "20px 46px", borderRadius: 70, background: "#FFF3DF", fontFamily: SANS, fontWeight: 700, fontSize: 42, color: "#BE2878", boxShadow: "0 10px 30px rgba(0,0,0,0.35)", transform: `scale(${pop(24)})` }}>Xem chi tiết ở link dưới bài</div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 500, fontSize: 36, color: "#fff", textShadow: SHADOW, opacity: pop(34) }}>louisyoga.vn</div>
      </div>
    </AbsoluteFill>
  );
};

const Shots: React.FC<{ v: V }> = ({ v }) => {
  const beatF = Math.round(v.beat * 30);
  const last = v.shots.length - 1;
  return (
    <>
      {v.shots.map((s, i) => {
        const len = s.dur + (i < last ? v.trans : 0);
        return (
          <Sequence key={i} from={s.from} durationInFrames={len} layout="none">
            <Layer s={s} v={v} len={len} first={i === 0} />
            {(s.mist ?? []).map((at, k) => (
              <Sequence key={k} from={Math.round(at * 30)} durationInFrames={18} layout="none">
                <Mist seed={k + 1} />
              </Sequence>
            ))}
          </Sequence>
        );
      })}
      {v.shots.map((s, i) =>
        s.a ? (
          <Sequence key={"t" + i} from={s.from + (v.style === "beat" ? 0 : Math.round(v.trans / 2))} durationInFrames={s.dur} layout="none">
            {v.style === "beat" ? <BeatText s={s} beatF={beatF} /> : v.style === "breath" ? <BreathText s={s} /> : <TypeText s={s} />}
          </Sequence>
        ) : null,
      )}
      {!v.framed && <Badge end={v.shots[last].from} />}
      {!v.framed && (
        <Sequence from={v.shots[last].from} durationInFrames={v.shots[last].dur} layout="none">
          <CTA style={v.style} len={v.shots[last].dur} />
        </Sequence>
      )}
    </>
  );
};

const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

// Soft spray leaving the nozzle (position measured on the shot): a faint fog plume plus very fine
// droplets that drift and sink, so it reads as mist rather than sparks.
const Mist: React.FC<{ seed: number }> = ({ seed }) => {
  const fr = useCurrentFrame();
  const NX = 665;
  const NY = 1345;
  const g = interpolate(fr, [0, 26], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const fog = interpolate(fr, [0, 5, 26], [0, 0.26, 0], clamp);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      <defs>
        <filter id={`fog${seed}`} x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation={34} /></filter>
        <filter id={`drop${seed}`}><feGaussianBlur stdDeviation={1} /></filter>
      </defs>
      <ellipse cx={NX + 30 + g * 70} cy={NY + 40 + g * 120} rx={60 + g * 170} ry={34 + g * 100} fill="#fff" opacity={fog} filter={`url(#fog${seed})`} />
      <g filter={`url(#drop${seed})`}>
        {Array.from({ length: 150 }).map((_, i) => {
          const r = (j: number) => rnd(seed * 100 + i * 3 + j);
          const age = (fr - r(0) * 7) / (15 + r(4) * 9);
          if (age <= 0 || age > 1) return null;
          const ang = 0.35 + r(1) * 1.5;
          const dist = (30 + r(2) * 250) * (1 - (1 - age) ** 3);
          return <circle key={i} cx={NX + Math.cos(ang) * dist} cy={NY + Math.sin(ang) * dist * 0.75 + age * age * 60} r={1 + r(3) * 1.8} fill="#fff" opacity={Math.sin(Math.min(age * 6, 1) * 1.57) * (1 - age) * 0.6} />;
        })}
      </g>
    </svg>
  );
};

// Torn-paper wipe: the next shot is revealed behind a jagged white paper edge moving across the frame.
const tearPts = (x: number, off: number) => {
  const p: [number, number][] = [];
  for (let i = 0; i <= 26; i++) {
    const y = (i / 26) * 1920;
    p.push([x + (y - 960) * 0.16 + (rnd(i) - 0.5) * 46 + (rnd(i + 40) - 0.5) * 18 + off * (0.6 + rnd(i + 80) * 0.9), y]);
  }
  return p;
};

const TearEdge: React.FC<{ x: number }> = ({ x }) => {
  const a = tearPts(x, 0);
  const b = tearPts(x, -34);
  const pts = [...a, ...b.reverse()].map(([px, py]) => `${px},${py}`).join(" ");
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      <polygon points={pts} fill="#FBF8F2" stroke="rgba(0,0,0,0.12)" strokeWidth={2} />
    </svg>
  );
};

// Later shots sit on top and fade/clear in over the transition; beat style hard-cuts.
const Layer: React.FC<{ s: Shot; v: V; len: number; first: boolean }> = ({ s, v, len, first }) => {
  const fr = useCurrentFrame();
  const t = v.trans;
  const k = first || !t ? 1 : interpolate(fr, [0, t], [0, 1], clamp);
  const blur = v.style === "type" && !first ? (1 - k) * 26 : 0;
  if (s.tear) {
    const e = interpolate(fr, [0, t], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
    const x = interpolate(e, [0, 1], [1320, -260]);
    const poly = [...tearPts(x, 0), [2000, 1920], [2000, 0]].map(([px, py]) => `${px}px ${py}px`).join(",");
    return (
      <>
        <AbsoluteFill style={{ clipPath: `polygon(${poly})` }}>
          <Clip s={s} style={v.style} len={len} />
        </AbsoluteFill>
        {fr < t && <TearEdge x={x} />}
      </>
    );
  }
  return (
    <AbsoluteFill style={{ opacity: k, filter: blur ? `blur(${blur}px)` : undefined }}>
      <Clip s={s} style={v.style} len={len} />
    </AbsoluteFill>
  );
};

// Layout "khung": blurred copy of the shot as background, the video in a rounded card (safe zone,
// drawn smaller so it looks sharper), brand logos on top, product name + photo card at the bottom right.
const CARD = { x: 132, y: 235, w: 816 };
const K = CARD.w / 1080;

const BgShot: React.FC<{ s: Shot; first: boolean }> = ({ s, first }) => {
  const fr = useCurrentFrame();
  const o = first ? 1 : interpolate(fr, [0, 12], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <OffthreadVideo src={staticFile(s.clip)} muted style={{ width: 1080, height: 1920, transform: "scale(1.3)", filter: "blur(44px) brightness(1.08)" }} />
    </AbsoluteFill>
  );
};

const Framed: React.FC<{ v: V }> = ({ v }) => {
  const fr = useCurrentFrame();
  const { fps } = useVideoConfig();
  const intro = !!v.intro;
  const p = spring({ frame: fr - (intro ? 32 : 8), fps, config: { damping: 14, stiffness: 130 } });
  // Opening: full-bleed shot clears from blur, then draws back into the card on the first music accent.
  const q = intro ? spring({ frame: fr - 15, fps, config: { damping: 15, stiffness: 95, mass: 0.8 } }) : 1;
  const S = 1 + (1 / K - 1) * (1 - q);
  const cardT = `translate(${-CARD.x * (1 - q)}px, ${-CARD.y * (1 - q)}px) scale(${S})`;
  const clearK = intro ? interpolate(fr, [0, 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) }) : 1;
  const glow = intro ? interpolate(fr, [25, 27, 46], [0, 0.42, 0], clamp) : 0;
  const logo = intro ? spring({ frame: fr - 27, fps, config: { damping: 16, stiffness: 120 } }) : 1;
  // Closing: shot blurs under a pale veil and the product card travels to the centre.
  const cf = fr - v.cta;
  const cOn = v.cta > 0 && cf >= 0;
  const veil = cOn ? interpolate(cf, [0, 18], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) }) : 0;
  const fly = cOn ? spring({ frame: cf - 2, fps, config: { damping: 17, stiffness: 95 } }) : 0;
  const btn = cOn ? spring({ frame: cf - 35, fps, config: { damping: 12, stiffness: 170 } }) : 0;
  const lerp = (a: number, b: number) => a + (b - a) * fly;
  const filter = clearK < 1 || veil > 0 ? `blur(${(1 - clearK) * 22 + veil * 16}px) brightness(${1 + (1 - clearK) * 0.3})` : undefined;
  return (
    <AbsoluteFill style={{ background: "#9AA09F", overflow: "hidden" }}>
      {v.shots.map((s, i) => (
        <Sequence key={i} from={s.from} durationInFrames={s.dur + 12} layout="none">
          <BgShot s={s} first={i === 0} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ background: "rgba(255,255,255,0.1)" }} />
      <Img src={staticFile("brand/logo_edit_white.svg")} style={{ position: "absolute", left: CARD.x - 8, top: 58, width: 370, opacity: logo, transform: `translateY(${(1 - logo) * -46}px)` }} />
      <AbsoluteFill style={{ transform: cardT, transformOrigin: `${CARD.x}px ${CARD.y}px` }}>
        <div style={{ position: "absolute", left: CARD.x - 8, top: CARD.y - 8, width: CARD.w + 16, height: Math.round(1920 * K) + 16, borderRadius: 58, background: "rgba(255,255,255,0.85)", boxShadow: "0 18px 50px rgba(0,0,0,0.22)" }} />
        <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: Math.round(1920 * K), borderRadius: 50 * Math.min(1, q), overflow: "hidden", background: "#111" }}>
          <div style={{ width: 1080, height: 1920, transform: `scale(${K})`, transformOrigin: "0 0", filter }}>
            <Shots v={v} />
          </div>
          <AbsoluteFill style={{ background: "#FAF7F1", opacity: veil * 0.8 }} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "#FFF3DF", opacity: glow }} />
      <div style={{ position: "absolute", right: 150, top: 1372, textAlign: "right", color: "#fff", fontFamily: SANS, textShadow: SHADOW, opacity: p * (1 - veil), transform: `translateX(${(1 - p) * 40}px)` }}>
        <div style={{ fontWeight: 300, fontSize: 32, letterSpacing: 2 }}>THẢM</div>
        <div style={{ fontWeight: 300, fontSize: 60, lineHeight: 1.0, letterSpacing: 2 }}>AURA</div>
      </div>
      <div style={{ position: "absolute", left: lerp(772, 350), top: lerp(1478, 262), width: lerp(200, 380), height: lerp(216, 440), borderRadius: 24, background: "#fff", overflow: "hidden", boxShadow: "0 10px 26px rgba(0,0,0,0.25)", transform: `rotate(${lerp(3, -2)}deg) scale(${p})` }}>
        <Img src={staticFile("brand/aura.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 0" }} />
      </div>
      {cOn && (
        <div style={{ position: "absolute", left: CARD.x, width: CARD.w, top: 708, textAlign: "center", color: INK }}>
          <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 96, lineHeight: 1.1 }}><Typed text="Thảm Aura" at={v.cta + 12} /></div>
          <div style={{ display: "inline-block", marginTop: 14, padding: "18px 36px", borderRadius: 60, background: INK, color: "#FFF3DF", fontFamily: SANS, fontWeight: 500, fontSize: 32, opacity: Math.min(1, btn), transform: `scale(${0.8 + 0.2 * btn})` }}>Xem chi tiết ở link dưới bài</div>
          <div style={{ marginTop: 20, fontFamily: SANS, fontWeight: 500, fontSize: 34, letterSpacing: 1 }}><Typed text="louisyoga.vn" at={v.cta + 44} /></div>
        </div>
      )}
    </AbsoluteFill>
  );
};

const Comp: React.FC<{ id: string }> = ({ id }) => {
  useFonts();
  const v = (spec as unknown as Record<string, V>)[id];
  if (v.framed) return <Framed v={v} />;
  return (
    <AbsoluteFill style={{ background: "#0F0B11" }}>
      <Shots v={v} />
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => (
  <>
    {["1", "2", "3"].map((id) => (
      <Composition key={id} id={"Review" + id} component={Comp} defaultProps={{ id }} durationInFrames={(spec as unknown as Record<string, V>)[id].total} fps={30} width={1080} height={1920} />
    ))}
  </>
);
