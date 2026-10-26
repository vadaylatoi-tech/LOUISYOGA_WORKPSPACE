import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 15 "Dấu hiệu nên thay thảm mới"
// Louis-only visuals: louisyoga.vn model photos, product avatars.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54;
const DURATION = VIDEO_FRAMES + TAIL;

const CAP_Y = 1190;
const G = 1330;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera (7 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3];
const HOOK_DROP = 1.18;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.0, 0.18],
  [8.68, 9.4, 0.12],
  [21.86, 22.5, 0.1],
  [49.05, 49.8, 0.08],
  [58.75, 59.5, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 7.6, end: 10.0, film: 0, src: PH + "tu-the/tu-the_211_tham-tap-yoga-cao-su-moon.jpg", mode: "photo", label: "Phải gồng sức nhiều hơn" },
  { start: 32.5, end: 34.9, film: 0, src: PH + "tu-the/tu-the_160_tham-tap-yoga-cao-su-cao-cap-diamond.jpg", mode: "photo", label: "Tập thoải mái hơn" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.69],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.63],
  [HOOK_DROP, "riser-metallic.mp3", 0.57],
  [HOOK_DROP, "punch.mp3", 0.95],
  [7.6, "swoosh.mp3", 0.57],
  [10.1, "pop-2.mp3", 0.57],
  [15.0, "quick-swoosh.mp3", 0.57],
  [18.68, "quick-ting.mp3", 0.57],
  [19.9, "quick-ting.mp3", 0.57],
  [21.86, "pop.mp3", 0.57],
  [22.9, "quick-swoosh.mp3", 0.57],
  [24.82, "quick-ting.mp3", 0.57],
  [28.79, "quick-ting.mp3", 0.57],
  [31.83, "correct.mp3", 0.57],
  [32.5, "swoosh.mp3", 0.52],
  [37.9, "pop.mp3", 0.57],
  [39.6, "quick-swoosh.mp3", 0.57],
  [49.05, "pop-2.mp3", 0.57],
  [54.1, "quick-swoosh.mp3", 0.57],
  [55.69, "quick-ting.mp3", 0.57],
  [56.49, "quick-ting.mp3", 0.57],
  [57.71, "quick-ting.mp3", 0.57],
  [58.75, "pop-2.mp3", 0.57],
  [61.27, "correct.mp3", 0.52],
  [62.15, "quick-swoosh.mp3", 0.63],
  [62.4, "punch.mp3", 0.6],
  [62.65, "camera-shutter.mp3", 0.57],
  [63.0, "ding.mp3", 0.46],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.7), f(2.3), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(7.5)} />
    <BigText start={0} end={f(7.5)} y={120} slam lines={[{ text: "Khi nào nên", color: C.white, size: 104 }]} />
    <BigText start={f(0.4)} end={f(7.5)} y={232} slam lines={[{ text: "thay thảm mới?", color: C.accent, size: 104 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(7.5)} />
    <Stamp text="Mất độ bám → thay!" start={f(HOOK_DROP)} end={f(7.5)} x={540} y={G + 150} rot={-6} size={70} />
  </>
);

const Effort: React.FC = () => (
  <>
    <BottomShade start={f(10.0)} end={f(12.2)} />
    <Pill text="Phải gồng giữ người trên thảm" start={f(10.1)} end={f(12.2)} x={W / 2} y={G + 140} size={40} />
  </>
);

const Global: React.FC = () => (
  <>
    <BottomShade start={f(39.6)} end={f(54.0)} />
    <Kicker text="dùng lâu, chất liệu nào cũng vậy" start={f(39.7)} end={f(54.0)} y={G + 40} color={C.white} />
    <Pill text="Kể cả thương hiệu quốc tế" start={f(49.05)} end={f(54.0)} x={W / 2} y={G + 140} bg={C.gold} fg={C.ink} size={42} />
  </>
);

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
      <Kicker text="xem thêm mẹo dùng thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/basic.jpg" label="Basic" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 38), color: C.white }}>Thảm mới</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>tập an tâm</div>
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
        <SeriesTag start={f(7.5)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <Effort />
        <NumberRows title="Dấu hiệu nên thay" rows={[["Bong tróc", 18.68], ["Mất độ bám", 19.9]]} start={15.0} end={22.8} y={G - 20} />
        <CheckGrid items={[["Sức khoẻ", 24.82], ["Hiệu quả", 28.79], ["Thoải mái", 31.83]]} start={f(22.9)} end={f(32.45)} y={G} />
        <BottomShade start={f(34.9)} end={f(39.5)} />
        <Pill text="Thảm mủn · bong tróc" start={f(37.9)} end={f(39.5)} x={W / 2} y={G + 140} bg="rgba(14,10,16,0.85)" size={44} />
        <Global />
        <NumberRows title="Thay thảm mới khi" rows={[["Bị mủn", 55.69], ["Mất độ bám", 56.49], ["Bong tróc", 57.71]]} start={54.1} end={(VIDEO_FRAMES - 3) / FPS} y={G - 60} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={1.2} until={CLEAN_DURATION} />
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
