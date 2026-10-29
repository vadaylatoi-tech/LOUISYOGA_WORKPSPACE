import React from "react";
import { AbsoluteFill, Easing, Freeze, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { usePop } from "./atoms";
import { C, clamp, f, font, FPS, H, W, ZONE } from "./theme";

// ---------------------------------------------------------------- talking head (full-bleed)

export type Punch = [number, number, number]; // [start s, end s, extra zoom]
export type Focus = [number, number, number, number, number]; // [start s, end s, x, y, zoom] — move off the face onto an object
export type FaceSample = [number, number, number]; // [t s, x, y] in 1080x1920 frame pixels

const faceAt = (face: FaceSample[], t: number): [number, number] => {
  if (!face.length) return [W / 2, H * 0.35];
  if (t <= face[0][0]) return [face[0][1], face[0][2]];
  for (let i = 1; i < face.length; i++) {
    if (face[i][0] >= t) {
      const [t0, x0, y0] = face[i - 1];
      const [t1, x1, y1] = face[i];
      const k = (t - t0) / Math.max(0.001, t1 - t0);
      return [x0 + (x1 - x0) * k, y0 + (y1 - y0) * k];
    }
  }
  const last = face[face.length - 1];
  return [last[1], last[2]];
};

// Full-frame footage. Hides every jump cut with an alternating zoom level per segment (segZoom),
// a 4-frame zoom-blur ghost at each cut, emphasis punch-ins, optional focus moves onto objects,
// a freeze + slow push during the CTA tail. Zoom origin follows the tracked face.
export const TalkingHead: React.FC<{
  src: string; // relative to public/, e.g. "footage/clean.mp4"
  videoFrames: number;
  duration: number;
  cuts: number[];
  face: FaceSample[];
  segZoom: number[];
  punches?: Punch[];
  focus?: Focus[];
  muted?: boolean;
}> = ({ src, videoFrames, duration, cuts, face, segZoom, punches = [], focus = [], muted }) => {
  const frame = useCurrentFrame();
  const t = Math.min(frame, videoFrames - 1) / FPS;
  let seg = 0;
  while (seg < cuts.length && t >= cuts[seg]) seg++;
  let zoom = segZoom[seg % segZoom.length];
  for (const [a, b, z] of punches) {
    if (frame >= f(a) && frame < f(b) + 8) {
      zoom += interpolate(frame, [f(a), f(a) + 5, f(b), f(b) + 8], [0, z, z, 0], { ...clamp, easing: Easing.out(Easing.cubic) });
    }
  }
  let [ox, oy] = faceAt(face, t);
  for (const [a, b, mx, my, mz] of focus) {
    const k = interpolate(frame, [f(a), f(a) + 9, f(b) - 6, f(b)], [0, 1, 1, 0], { ...clamp, easing: Easing.inOut(Easing.cubic) });
    if (k > 0) {
      ox += (mx - ox) * k;
      oy += (my - oy) * k;
      zoom += (mz - zoom) * k;
    }
  }
  if (frame >= videoFrames) zoom += interpolate(frame, [videoFrames, duration], [0, 0.06], clamp);
  let ghost = 0;
  for (const c of cuts) {
    const d = frame - f(c);
    if (d >= 0 && d < 4) ghost = 1 - d / 4;
  }
  const layer = (z: number, opacity: number, mute: boolean) => (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: `${ox}px ${oy}px`, opacity }}>
      {frame < videoFrames ? (
        <OffthreadVideo src={staticFile(src)} muted={mute} style={{ width: W, height: H }} />
      ) : (
        <Freeze frame={videoFrames - 1}>
          <OffthreadVideo src={staticFile(src)} muted style={{ width: W, height: H }} />
        </Freeze>
      )}
    </AbsoluteFill>
  );
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {layer(zoom, 1, !!muted)}
      {ghost > 0.05 && layer(zoom * (1 + 0.06 * ghost), 0.35 * ghost, true)}
      {ghost > 0.05 && layer(zoom * (1 + 0.12 * ghost), 0.25 * ghost, true)}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- B-roll (full-bleed cutaways)

// film = second in the source clip; cx = subject centre (px) in a 1920x1080 film (crop mode only).
// mode: "fit"   (default) whole 16:9 frame visible over a blurred copy — full-body poses stay readable
//       "crop"  fill 9:16 by cropping ~607 px around cx — ONLY for close-ups (hands on mat, texture, logo)
//       "cover" vertical 9:16 clip filling the frame
//       "photo" still image (Louis Yoga lifestyle/product photo) with a slow push — src = "img/…jpg"
// src: other clip in public/ (e.g. "broll/web/xyz.mp4"); default = the layer's src (brand film).
export type Broll = { start: number; end: number; film: number; cx?: number; label: string; mode?: "fit" | "crop" | "cover" | "photo"; src?: string };

const FILM_SCALE = H / 1080;
const FILM_W = 1920 * FILM_SCALE;

const BrollShot: React.FC<{ b: Broll; src: string }> = ({ b, src }) => {
  const frame = useCurrentFrame();
  const len = f(b.end) - f(b.start);
  const push = interpolate(frame, [0, len], [1.04, 1.12]);
  // Horizontal whip in/out with ghost copies; the film is wider than the frame so no edge shows.
  const dx = interpolate(frame, [0, 5, len - 4, len], [520, 0, 0, -520], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const moving = Math.abs(dx) > 8;
  const mode = b.mode ?? "fit";
  const clip = staticFile(b.src ?? src);
  const left = W / 2 - (b.cx ?? 960) * FILM_SCALE;
  const fitH = Math.round((W * 1.12 * 1080) / 1920); // 16:9 frame at 112 % width, centred on the face band
  const shot = (offset: number, opacity: number) => (
    <AbsoluteFill style={{ transform: `translateX(${dx + offset}px) scale(${push})`, opacity }}>
      {mode === "crop" && <OffthreadVideo src={clip} startFrom={f(b.film)} muted style={{ position: "absolute", left, top: 0, width: FILM_W, height: H }} />}
      {mode === "photo" && (
        <>
          <Img src={clip} style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "cover", filter: "blur(28px) brightness(0.55)" }} />
          <Img src={clip} style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "contain" }} />
        </>
      )}
      {mode === "cover" && <OffthreadVideo src={clip} startFrom={f(b.film)} muted style={{ position: "absolute", left: 0, top: 0, width: W, height: H, objectFit: "cover" }} />}
      {mode === "fit" && (
        <>
          <OffthreadVideo src={clip} startFrom={f(b.film)} muted style={{ position: "absolute", left, top: 0, width: FILM_W, height: H, filter: "blur(28px) brightness(0.55)" }} />
          <OffthreadVideo
            src={clip}
            startFrom={f(b.film)}
            muted
            style={{ position: "absolute", left: (W - W * 1.12) / 2, top: 820 - fitH / 2, width: W * 1.12, height: fitH, boxShadow: "0 20px 60px rgba(0,0,0,0.6)" }}
          />
        </>
      )}
    </AbsoluteFill>
  );
  const lp = usePop(3, 14);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {shot(0, 1)}
      {moving && shot(dx * 0.25, 0.4)}
      {moving && shot(dx * 0.5, 0.25)}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)" }} />
      <div style={{ position: "absolute", left: ZONE.L, top: ZONE.TOP + 80, display: "flex", alignItems: "center", transform: `translateX(${(1 - lp) * -300}px)`, opacity: lp }}>
        <div style={{ width: 16, height: 16, borderRadius: 99, background: C.accent, marginRight: 14, boxShadow: `0 0 14px ${C.accent}` }} />
        <div style={{ ...font(900, 46), color: C.white, textShadow: "0 3px 10px rgba(0,0,0,0.6)" }}>{b.label}</div>
      </div>
    </AbsoluteFill>
  );
};

export const BrollLayer: React.FC<{ items: Broll[]; src: string }> = ({ items, src }) => (
  <>
    {items.map((b, i) => (
      <Sequence key={i} from={f(b.start)} durationInFrames={f(b.end) - f(b.start)}>
        <BrollShot b={b} src={src} />
      </Sequence>
    ))}
  </>
);

// ---------------------------------------------------------------- karaoke captions

export type CapWord = { w: string; s: number; e: number };
export type CapLine = { start: number; end: number; words: CapWord[] };

// Word-by-word captions: active word pink + slightly larger, black outline for any background.
// Centred in zone B (x 90–800, left of the button column); a long line is shrunk to fit. y = top of the line.
export const Captions: React.FC<{ lines: CapLine[]; y: number; from: number; until: number }> = ({ lines, y, from, until }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t < from || t >= until) return null;
  const line = lines.find((l) => t >= l.start - 0.05 && t < l.end + 0.15);
  if (!line) return null;
  const enter = interpolate(t, [line.start - 0.05, line.start + 0.08], [0, 1], clamp);
  const est = line.words.reduce((a, w) => a + w.w.length * 62 * 0.66 + 18, 0); // ≈ px width at size 62
  const fit = Math.min(1, (ZONE.R_B - ZONE.L) / est);
  return (
    <div style={{ position: "absolute", top: y, left: ZONE.L, width: ZONE.R_B - ZONE.L, textAlign: "center", whiteSpace: "nowrap", transform: `translateY(${(1 - enter) * 16}px) scale(${fit})`, transformOrigin: "50% 0", opacity: enter }}>
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
