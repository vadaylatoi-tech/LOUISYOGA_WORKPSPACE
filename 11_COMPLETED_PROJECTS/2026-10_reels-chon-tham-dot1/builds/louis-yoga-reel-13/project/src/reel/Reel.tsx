import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact, usePop } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { DoDont } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 13 "Cuộn thảm sai cách làm gãy bề mặt"
// Louis-only visuals: louisyoga.vn rolling photos + a simple roll cross-section diagram.
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
const ROLL = PH + "cuon-tham/cuon-tham_007_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg";

// ▼ EDIT ▼ camera (9 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24];
const HOOK_DROP = 1.0;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 1.8, 0.16],
  [8.07, 8.9, 0.14],
  [13.64, 14.4, 0.1],
  [23.5, 24.2, 0.1],
  [44.59, 45.3, 0.1],
  [55.24, 56.0, 0.1],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 11.2, end: 13.6, film: 0, src: ROLL, mode: "photo", label: "Cuộn thảm đúng cách" },
  { start: 40.3, end: 42.6, film: 0, src: PH + "be-mat/be-mat_077_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "Bề mặt cao su" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 8, 12, 0.4],
  [8.07, 10, 18, 0.5],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "quick-swoosh.mp3", 0.55],
  [6.15, "pop.mp3", 0.5],
  [8.07, "riser-metallic.mp3", 0.5],
  [8.07, "punch.mp3", 0.95],
  [11.2, "swoosh.mp3", 0.5],
  [13.7, "quick-swoosh.mp3", 0.5],
  [18.1, "pop-2.mp3", 0.5],
  [23.5, "correct.mp3", 0.5],
  [28.1, "quick-swoosh.mp3", 0.5],
  [30.1, "pop.mp3", 0.5],
  [34.81, "pop-2.mp3", 0.5],
  [40.3, "swoosh.mp3", 0.45],
  [44.59, "punch.mp3", 0.7],
  [48.42, "pop.mp3", 0.5],
  [49.56, "pop-2.mp3", 0.5],
  [51.75, "quick-swoosh.mp3", 0.5],
  [53.08, "quick-ting.mp3", 0.5],
  [55.24, "correct.mp3", 0.5],
  [57.3, "quick-swoosh.mp3", 0.55],
  [57.55, "punch.mp3", 0.6],
  [57.8, "camera-shutter.mp3", 0.5],
  [58.15, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.8), f(2.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Roll cross-section: a spiral of the mat; `right` = top (pink) face outside, dark base inside.
const Roll: React.FC<{ right: boolean; at: number; size?: number }> = ({ right, at, size = 220 }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [f(at), f(at) + 18], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const pts: string[] = [];
  const turns = 3.2;
  for (let k = 0; k <= 200 * draw; k++) {
    const t = (k / 200) * turns * Math.PI * 2;
    const r = 18 + (k / 200) * (size / 2 - 30);
    pts.push(`${size / 2 + r * Math.cos(t)},${size / 2 + r * Math.sin(t)}`);
  }
  const d = pts.length ? "M" + pts.join(" L") : "";
  const outer = right ? C.accent : "#9A90A6";
  const inner = right ? "#9A90A6" : C.accent;
  return (
    <svg width={size} height={size}>
      <path d={d} stroke={outer} strokeWidth={13} fill="none" strokeLinecap="round" />
      <path d={d} stroke={inner} strokeWidth={5} fill="none" strokeLinecap="round" transform={`translate(0,0)`} style={{ transform: "scale(0.955)", transformOrigin: "50% 50%" }} />
    </svg>
  );
};

const Hook: React.FC = () => {
  const p = usePop(f(HOOK_DROP), 12);
  return (
    <>
      <TopShade start={0} end={f(11.1)} />
      <BigText start={0} end={f(11.1)} y={120} slam lines={[{ text: "Cuộn thảm sai cách", color: C.white, size: 80 }]} />
      <BigText start={f(0.4)} end={f(11.1)} y={222} slam lines={[{ text: "gãy bề mặt!", color: C.accent, size: 118 }]} />
      <Panel start={f(HOOK_DROP)} end={f(11.1)} y={G - 40} h={370}>
        <div style={{ position: "absolute", left: 40, top: 40, transform: `scale(${p})` }}>
          <Roll right={false} at={HOOK_DROP} size={280} />
        </div>
        <div style={{ position: "absolute", left: 360, top: 70, ...font(900, 56), color: C.white }}>✕ Cuộn ngược</div>
        <div style={{ position: "absolute", left: 360, top: 150, ...font(800, 30), color: C.dim, letterSpacing: 1 }}>mặt chính bị cuộn vào trong</div>
      </Panel>
      <Stamp text="Dễ gãy bề mặt!" start={f(8.07)} end={f(11.1)} x={640} y={G + 240} rot={-6} size={60} />
    </>
  );
};

// Right way: top face outside, black base inside.
const RightWay: React.FC = () => (
  <Panel start={f(13.7)} end={f(28.0)} y={G - 40} h={370}>
    <div style={{ position: "absolute", left: 30, top: 40 }}>
      <Roll right at={13.7} size={280} />
    </div>
    <div style={{ position: "absolute", left: 350, top: 40, ...font(900, 50), color: C.accent }}>✓ Cuộn đúng</div>
    <Pill text="Mặt chính ra ngoài" start={f(13.7)} end={f(28.0)} x={600} y={130} size={34} />
    <Pill text="Mặt đen ở bên trong" start={f(18.1)} end={f(28.0)} x={600} y={210} bg="rgba(255,255,255,0.15)" fg={C.white} size={34} />
    <Pill text="Hạn chế gãy bề mặt" start={f(24.18)} end={f(28.0)} x={600} y={290} bg={C.gold} fg={C.ink} size={34} />
  </Panel>
);

// Don't fold the two faces together.
const NoFold: React.FC = () => {
  const frame = useCurrentFrame();
  const fold = interpolate(frame, [f(34.81), f(34.81) + 14], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <>
      <BottomShade start={f(28.1)} end={f(34.2)} />
      <Kicker text="có trong sổ hướng dẫn gửi kèm" start={f(28.2)} end={f(34.2)} y={G + 40} color={C.white} />
      <Panel start={f(34.3)} end={f(40.3)} y={G - 20} h={300}>
        <div style={{ position: "absolute", left: 80, top: 120, width: 300, height: 34, borderRadius: 8, background: C.accent }} />
        <div style={{ position: "absolute", left: 80, top: 120 - 34 - 6 * (1 - fold), width: 300, height: 34, borderRadius: 8, background: C.accent, transform: `rotate(${-150 * (1 - fold)}deg)`, transformOrigin: "100% 100%", opacity: 0.85 }} />
        <div style={{ position: "absolute", left: 430, top: 70, ...font(900, 52), color: C.white }}>✕ Gập 2 mặt</div>
        <div style={{ position: "absolute", left: 430, top: 140, ...font(900, 52), color: C.white }}>vào nhau</div>
      </Panel>
      <BottomShade start={f(42.6)} end={f(51.7)} />
      <Kicker text="cao su · bề mặt bóng" start={f(42.7)} end={f(51.7)} y={G + 10} color={C.white} />
      <Stamp text="Gập lại = dễ hỏng" start={f(44.59)} end={f(51.7)} x={540} y={G + 120} rot={-5} size={64} />
      <Pill text="Dễ dính" start={f(48.42)} end={f(51.7)} x={360} y={G + 230} size={44} />
      <Pill text="Bong bề mặt" start={f(49.56)} end={f(51.7)} x={720} y={G + 230} bg={C.gold} fg={C.ink} size={44} />
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
      <Kicker text="xem thêm mẹo dùng thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src={ROLL} label="Mặt chính ra ngoài" start={s + 8} end={DURATION + 1} x={60} y={G - 40} w={260} h={230} rot={-6} />
      <div style={{ position: "absolute", left: 660, top: G - 10, opacity: interpolate(frame, [s + 12, s + 20], [0, 1], clamp) }}>
        <Roll right at={(s + 12) / FPS} size={260} />
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
        <SeriesTag start={f(11.1)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <RightWay />
        <NoFold />
        <DoDont title="Lưu ý khi cuộn thảm" rows={[["Mặt chính ra ngoài", 53.08, true], ["Gập 2 mặt vào nhau", 55.24, false]]} start={51.75} end={(VIDEO_FRAMES - 3) / FPS} y={G - 20} size={44} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={1.0} until={CLEAN_DURATION} />
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
