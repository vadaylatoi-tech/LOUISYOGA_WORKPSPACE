import React, { useEffect, useState } from "react";
import { AbsoluteFill, Composition, continueRender, delayRender, Easing, Img, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import spec from "./spec.json";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const SANS = "BeVN";
const SERIF = "SerifVN";
type Shot = { name: string; clip: string; from: number; dur: number; a: string; b: string };
type V = { style: string; trans: number; beat: number; total: number; shots: Shot[] };

const useFonts = () => {
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => {
    const add = (fam: string, file: string, weight: string, style = "normal") => new FontFace(fam, `url(${staticFile("fonts/" + file)})`, { weight, style }).load().then((f) => document.fonts.add(f));
    Promise.all([add(SANS, "BeVietnamPro-Light.ttf", "300"), add(SANS, "BeVietnamPro-Medium.ttf", "500"), add(SANS, "BeVietnamPro-Bold.ttf", "700"), add(SANS, "BeVietnamPro-ExtraBold.ttf", "800"), add(SERIF, "cambriai.ttf", "400", "italic")]).then(() => continueRender(h));
  }, [h]);
};

const SHADOW = "0 2px 6px rgba(0,0,0,0.75), 0 6px 34px rgba(0,0,0,0.6)";

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

// Slow, breathing: serif line clears from blur while the letters settle; small spaced line follows.
const BreathText: React.FC<{ s: Shot }> = ({ s }) => {
  const fr = useCurrentFrame();
  const k = interpolate(fr, [4, 30], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const k2 = interpolate(fr, [20, 44], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const out = interpolate(fr, [s.dur - 14, s.dur - 2], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: 90, right: 90, top: 420, textAlign: "center", opacity: out }}>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 112, lineHeight: 1.15, color: "#FFF3DF", textShadow: SHADOW, opacity: k, filter: `blur(${(1 - k) * 12}px)`, letterSpacing: (1 - k) * 12 }}>{s.a}</div>
      {s.b && <div style={{ marginTop: 16, fontFamily: SANS, fontWeight: 500, fontSize: 36, letterSpacing: 7 - k2 * 2, color: "#fff", textTransform: "uppercase", textShadow: SHADOW, opacity: k2 }}>{s.b}</div>}
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

// Soft dark glow behind the text so thin type still reads on the bright wall (no visible box).
const Scrim: React.FC<{ len: number }> = ({ len }) => {
  const fr = useCurrentFrame();
  const o = interpolate(fr, [0, 8, len - 8, len], [0, 1, 1, 0], clamp);
  return <AbsoluteFill style={{ opacity: o, background: "radial-gradient(ellipse 62% 17% at 50% 25%, rgba(16,11,18,0.62) 0%, rgba(16,11,18,0.32) 55%, rgba(16,11,18,0) 100%)" }} />;
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
          </Sequence>
        );
      })}
      {v.shots.map((s, i) =>
        s.a ? (
          <Sequence key={"t" + i} from={s.from + (v.style === "beat" ? 0 : Math.round(v.trans / 2))} durationInFrames={s.dur} layout="none">
            <Scrim len={s.dur} />
            {v.style === "beat" ? <BeatText s={s} beatF={beatF} /> : v.style === "breath" ? <BreathText s={s} /> : <TypeText s={s} />}
          </Sequence>
        ) : null,
      )}
      <Badge end={v.shots[last].from} />
      <Sequence from={v.shots[last].from} durationInFrames={v.shots[last].dur} layout="none">
        <CTA style={v.style} len={v.shots[last].dur} />
      </Sequence>
    </>
  );
};

// Later shots sit on top and fade/clear in over the transition; beat style hard-cuts.
const Layer: React.FC<{ s: Shot; v: V; len: number; first: boolean }> = ({ s, v, len, first }) => {
  const fr = useCurrentFrame();
  const t = v.trans;
  const k = first || !t ? 1 : interpolate(fr, [0, t], [0, 1], clamp);
  const blur = v.style === "type" && !first ? (1 - k) * 26 : 0;
  return (
    <AbsoluteFill style={{ opacity: k, filter: blur ? `blur(${blur}px)` : undefined }}>
      <Clip s={s} style={v.style} len={len} />
    </AbsoluteFill>
  );
};

const Comp: React.FC<{ id: string }> = ({ id }) => {
  useFonts();
  const v = (spec as unknown as Record<string, V>)[id];
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
