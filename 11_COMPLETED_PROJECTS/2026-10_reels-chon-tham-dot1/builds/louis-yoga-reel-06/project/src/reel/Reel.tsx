import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard, NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 06 "Dòng thảm chuyên sâu (Mastery) khác gì thảm thường?"
// Louis-only visuals: product avatars, louisyoga.vn model photos, brand film.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54;
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same studio as reels 01–05
const CAP_Y = 1190;
const G = 1330;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera (5 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26];
const HOOK_DROP = 1.5;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.3, 0.2],
  [6.49, 7.0, 0.1],
  [13.47, 14.4, 0.12],
  [30.83, 31.4, 0.08],
  [36.13, 36.9, 0.1],
  [48.75, 49.4, 0.1],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 9.4, end: 11.3, film: 0, src: PH + "tu-the/tu-the_178_tham-tap-yoga-cao-su-cao-cap-f23-1.jpg", mode: "photo", label: "Dòng Mastery" },
  { start: 11.9, end: 13.4, film: 46.2, cx: 1000, mode: "crop", label: "Chất liệu bề mặt" },
  { start: 32.2, end: 34.3, film: 0, src: PH + "tu-the/tu-the_203_tham-tap-yoga-cao-su-cao-cap-nature.jpg", mode: "photo", label: "Chất lượng vượt trội" },
  { start: 40.0, end: 42.2, film: 12.3, cx: 940, mode: "fit", label: "Tập thông thường" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.5, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [13.47, 6, 8, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.5, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [6.49, "pop-2.mp3", 0.5],
  [9.4, "swoosh.mp3", 0.5],
  [11.9, "swoosh.mp3", 0.4],
  [13.47, "punch.mp3", 0.8],
  [14.19, "pop.mp3", 0.5],
  [14.9, "quick-swoosh.mp3", 0.5],
  [18.17, "quick-ting.mp3", 0.5],
  [20.07, "quick-ting.mp3", 0.5],
  [23.95, "pop-2.mp3", 0.5],
  [26.19, "pop.mp3", 0.5],
  [29.3, "quick-swoosh.mp3", 0.5],
  [30.83, "quick-ting.mp3", 0.5],
  [32.2, "swoosh.mp3", 0.45],
  [32.91, "quick-ting.mp3", 0.5],
  [36.13, "pop-2.mp3", 0.5],
  [40.0, "swoosh.mp3", 0.45],
  [48.6, "quick-swoosh.mp3", 0.5],
  [50.25, "quick-ting.mp3", 0.5],
  [50.77, "quick-ting.mp3", 0.5],
  [51.77, "quick-ting.mp3", 0.5],
  [52.77, "correct.mp3", 0.5],
  [55.1, "quick-swoosh.mp3", 0.55],
  [55.35, "punch.mp3", 0.7],
  [55.6, "camera-shutter.mp3", 0.5],
  [55.95, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.1), f(2.7), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const MASTERY = [
  ["img/lilium.jpg", "Lilium"],
  ["img/nature.jpg", "Nature"],
  ["img/f23.jpg", "F23"],
  ["img/diamond.jpg", "Diamond"],
];

// Hook: question in two beats, then the 4 real Mastery mats drop with the heavy hit.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(4.9)} />
    <BigText start={0} end={f(4.9)} y={120} slam lines={[{ text: "Thảm chuyên sâu", color: C.white, size: 96 }]} />
    <BigText start={f(0.5)} end={f(4.9)} y={222} slam lines={[{ text: "khác gì thảm thường?", color: C.accent, size: 62 }]} />
    <Panel start={f(HOOK_DROP)} end={f(9.35)} y={G - 40} h={370}>
      <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.gold, letterSpacing: 3 }}>Dòng Mastery</div>
      {MASTERY.map(([src, label], i) => (
        <MatCard key={label} src={src} label={label} x={52 + i * 208} y={64} w={118} h={240} at={HOOK_DROP + i * 0.1} active />
      ))}
    </Panel>
  </>
);

// Material: PU sinh thái nhám lì.
const Material: React.FC = () => (
  <>
    <BottomShade start={f(13.3)} end={f(14.75)} />
    <Stamp text="PU sinh thái" start={f(13.47)} end={f(14.75)} x={540} y={G + 120} rot={-6} size={86} />
    <Pill text="Nhám lì" start={f(14.19)} end={f(14.75)} x={540} y={G + 230} bg={C.white} fg={C.ink} size={44} />
  </>
);

// Hạn chế xước / bám bẩn.
const Protect: React.FC = () => (
  <>
    <BottomShade start={f(20.9)} end={f(29.2)} />
    <Kicker text="so với thảm thông thường" start={f(21.0)} end={f(29.2)} y={G + 20} color={C.white} />
    <Pill text="✓ Hạn chế trầy xước" start={f(23.95)} end={f(29.2)} x={W / 2} y={G + 100} size={46} />
    <Pill text="✓ Hạn chế bám bẩn" start={f(26.19)} end={f(29.2)} x={W / 2} y={G + 200} bg={C.gold} fg={C.ink} size={46} />
  </>
);

const PriceNote: React.FC = () => (
  <Pill text="Giá thành nhỉnh hơn" start={f(36.13)} end={f(39.3)} x={W / 2} y={G + 245} bg={C.white} fg={C.ink} size={38} />
);

// Conclusion: normal training → Balance line (5 ly).
const Balance: React.FC = () => {
  const s = f(48.6);
  const e = VIDEO_FRAMES - 3;
  const mats = [
    ["img/basic.jpg", "Basic", 50.25],
    ["img/basiczen.jpg", "Basic Zen", 50.77],
    ["img/asana25.jpg", "Asana 25", 51.77],
    ["img/queen.jpg", "Queen", 52.77],
  ] as const;
  return (
    <>
      <Kicker text="tập cường độ vừa phải?" start={f(42.4)} end={f(48.6)} y={G + 40} color={C.white} />
      <Panel start={s} end={e} y={G - 40} h={370}>
        <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.accent, letterSpacing: 2 }}>Dòng Balance · 5 ly là đủ</div>
        {mats.map(([src, label, at], i) => (
          <MatCard key={label} src={src} label={label} x={52 + i * 208} y={64} w={118} h={240} at={at} active labelSize={22} />
        ))}
      </Panel>
    </>
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
        <Img src={staticFile("brand/lotus.png")} style={{ width: 140, height: 140 }} />
      </div>
      <BigText start={s + 6} end={DURATION + 1} y={260} slam lines={[{ text: "Follow Louis Yoga", color: C.white, size: 84 }]} />
      <Kicker text="xem thêm mẹo chọn thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src="img/lilium.jpg" label="Mastery" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/basic.jpg" label="Balance" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 60, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 34), color: C.white }}>Chuyên sâu</div>
        <div style={{ ...font(900, 44), color: C.gold }}>Mastery</div>
        <div style={{ ...font(900, 34), color: C.white, marginTop: 12 }}>Thông thường</div>
        <div style={{ ...font(900, 44), color: C.accent }}>Balance</div>
      </div>
    </>
  );
};

// ▲ EDIT ▲ ------------------------------------------------------------------------------

export const LouisYogaReel: React.FC = () => {
  useMontserrat();
  const { dx, dy, flash } = useImpact(IMPACTS);
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, fontFamily: MONTSERRAT }}>
      <AbsoluteFill style={{ transform: `translate(${dx}px, ${dy}px) scale(${dx || dy ? 1.03 : 1})` }}>
        <TalkingHead src={FOOTAGE} videoFrames={VIDEO_FRAMES} duration={DURATION} cuts={CUTS} face={FACE} segZoom={SEG_ZOOM} punches={PUNCHES} focus={FOCUS} muted={STEM !== "all"} />
        <BrollLayer items={BROLL} src={FILM} />
        <Hook />
        <SeriesTag start={f(4.9)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <Material />
        <CheckGrid items={[["Thấm hút", 18.17], ["Bám tay", 20.07]]} start={f(14.9)} end={f(20.85)} y={G} />
        <Protect />
        <NumberRows title="Mastery vượt trội" rows={[["Đáp ứng cao hơn", 30.83], ["Bền · chất lượng", 32.91]]} start={29.3} end={39.3} y={G - 20} />
        <PriceNote />
        <Balance />
        <Captions lines={CAPTIONS} y={CAP_Y} from={4.9} until={CLEAN_DURATION} />
        <EndCTA />
      </AbsoluteFill>
      {flash > 0 && <AbsoluteFill style={{ background: "#fff", opacity: flash }} />}
      <SoundLayer cues={CUES} music={MUSIC} curve={MUSIC_CURVE} />
    </AbsoluteFill>
  );
};

export const LouisYogaReelComposition: React.FC = () => (
  <Composition id="LouisYogaReel" component={LouisYogaReel} durationInFrames={DURATION} fps={FPS} width={W} height={1920} />
);
