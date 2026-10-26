import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { DoDont, MatCard } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 16 "Thảm rẻ vài tháng đã hỏng — mua rẻ có thật sự rẻ?"
// Louis-only visuals (cheap mats drawn as plain grey shapes — no other brand shown).
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

// ▼ EDIT ▼ camera (6 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1];
const HOOK_DROP = 1.4;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.2, 0.18],
  [8.15, 8.8, 0.1],
  [21.27, 22.0, 0.1],
  [26.51, 27.2, 0.14],
  [37.97, 38.6, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 40.6, end: 42.75, film: 0, src: PH + "tu-the/tu-the_157_tham-tap-yoga-cao-su-cao-cap-diamond.jpg", mode: "photo", label: "Thảm chất lượng tốt" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [26.51, 7, 9, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [8.15, "pop-2.mp3", 0.5],
  [10.1, "quick-swoosh.mp3", 0.5],
  [11.91, "quick-ting.mp3", 0.5],
  [18.77, "pop.mp3", 0.5],
  [21.27, "digital-counting-1.mp3", 0.5],
  [22.85, "pop-2.mp3", 0.5],
  [26.51, "punch.mp3", 0.8],
  [29.73, "correct.mp3", 0.5],
  [32.4, "quick-swoosh.mp3", 0.5],
  [37.97, "punch.mp3", 0.7],
  [40.6, "swoosh.mp3", 0.5],
  [42.8, "quick-swoosh.mp3", 0.5],
  [43.0, "quick-ting.mp3", 0.5],
  [45.43, "quick-ting.mp3", 0.5],
  [48.51, "pop.mp3", 0.5],
  [50.05, "quick-swoosh.mp3", 0.55],
  [50.3, "punch.mp3", 0.6],
  [50.55, "camera-shutter.mp3", 0.5],
  [50.9, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.9), f(2.5), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(6.2)} />
    <BigText start={0} end={f(6.2)} y={120} slam lines={[{ text: "Thảm rẻ vài tháng đã hỏng", color: C.white, size: 52 }]} />
    <BigText start={f(0.4)} end={f(6.2)} y={196} slam lines={[{ text: "mua rẻ có thật rẻ?", color: C.accent, size: 76 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(6.2)} />
    <Stamp text="Do chất liệu!" start={f(HOOK_DROP)} end={f(6.2)} x={540} y={G + 150} rot={-6} size={86} />
  </>
);

// Cost compare: cheap mat replaced again and again vs one quality Louis mat.
const Cost: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(10.1);
  const e = f(32.3);
  const cheap = (i: number, at: number) => {
    if (frame < f(at)) return null;
    const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
    return (
      <div key={i} style={{ position: "absolute", left: 40 + i * 120, top: 100, width: 90, height: 190, borderRadius: 10, background: "linear-gradient(180deg,#8E8796,#5F5866)", border: "3px solid rgba(255,255,255,0.35)", transform: `translateY(${(1 - p) * 40}px)`, opacity: Math.min(1, p * 2) }}>
        <div style={{ position: "absolute", bottom: 8, left: 0, right: 0, textAlign: "center", ...font(900, 22), color: C.white }}>{i === 0 ? "mua" : "thay"}</div>
      </div>
    );
  };
  return (
    <Panel start={s} end={e} y={G - 40} h={370}>
      <div style={{ position: "absolute", left: 30, top: 22, width: 420, textAlign: "center", ...font(900, 34), color: C.white }}>Thảm rẻ</div>
      {cheap(0, 18.77)}
      {cheap(1, 22.85)}
      {cheap(2, 23.3)}
      {frame >= f(21.27) && <div style={{ position: "absolute", left: 30, top: 300, width: 420, textAlign: "center", ...font(900, 32), color: C.gold }}>2–3 tháng/lần</div>}
      <div style={{ position: "absolute", left: 445, top: 150, width: 40, textAlign: "center", ...font(900, 34), color: C.gold }}>VS</div>
      <div style={{ position: "absolute", left: 490, top: 22, width: 400, textAlign: "center", ...font(900, 34), color: C.accent }}>Chất lượng tốt</div>
      <MatCard src="img/basic.jpg" label="1 lần, dùng bền" x={620} y={74} w={130} h={230} at={11.91} active={frame >= f(29.73)} labelSize={24} />
    </Panel>
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
      <Polaroid src="img/basic.jpg" label="Basic" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/asana25.jpg" label="Asana 25" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 38), color: C.white }}>Đầu tư</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>đúng từ đầu</div>
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
        <SeriesTag start={f(6.2)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <BottomShade start={f(6.3)} end={f(10.05)} />
        <Pill text="Phụ thuộc chất liệu thảm" start={f(8.15)} end={f(10.05)} x={W / 2} y={G + 140} size={44} />
        <Cost />
        <Stamp text="Chi phí cao hơn!" start={f(26.51)} end={f(29.6)} x={260} y={G + 160} rot={-8} size={50} />
        <BottomShade start={f(32.4)} end={f(39.1)} />
        <Kicker text="thảm không đáp ứng nhu cầu" start={f(32.5)} end={f(39.1)} y={G + 20} color={C.white} />
        <BigText start={f(37.97)} end={f(39.1)} y={G + 90} slam lines={[{ text: "Tập nản hơn", color: C.accent, size: 104 }]} />
        <DoDont title="Lời khuyên khi bắt đầu" rows={[["Chọn chất lượng đảm bảo", 43.0, true], ["Tập thoải mái hơn", 45.43, true], ["Thay thảm liên tục", 48.51, false]]} start={42.8} end={(VIDEO_FRAMES - 3) / FPS} y={G - 40} size={38} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={1.3} until={CLEAN_DURATION} />
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
