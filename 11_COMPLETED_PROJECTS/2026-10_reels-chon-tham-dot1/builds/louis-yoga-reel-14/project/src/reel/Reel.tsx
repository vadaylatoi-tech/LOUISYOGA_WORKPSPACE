import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 14 "Thảm yoga dùng được bao lâu?"
// Louis-only visuals: product avatar wear map, louisyoga.vn model photo, brand film.
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

// ▼ EDIT ▼ camera (11 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24, 1.12, 1.28];
const HOOK_DROP = 1.86;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.6, 0.18],
  [9.67, 10.3, 0.08],
  [26.68, 27.3, 0.1],
  [33.64, 34.4, 0.12],
  [49.17, 49.9, 0.1],
  [65.91, 66.6, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 23.3, end: 25.6, film: 0, src: PH + "tu-the/tu-the_287_tham-tap-yoga-du-lich.jpg", mode: "photo", label: "Cường độ cao" },
  { start: 27.0, end: 30.0, film: 12.3, cx: 940, mode: "fit", label: "Tập nhẹ nhàng" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [65.91, 7, 9, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [9.67, "pop-2.mp3", 0.5],
  [10.3, "quick-swoosh.mp3", 0.5],
  [12.19, "quick-ting.mp3", 0.5],
  [15.29, "quick-ting.mp3", 0.5],
  [17.63, "quick-ting.mp3", 0.5],
  [19.99, "pop.mp3", 0.5],
  [22.21, "pop-2.mp3", 0.5],
  [23.3, "swoosh.mp3", 0.5],
  [27.0, "swoosh.mp3", 0.4],
  [33.64, "punch.mp3", 0.7],
  [39.24, "pop.mp3", 0.5],
  [40.7, "quick-swoosh.mp3", 0.5],
  [46.51, "pop-2.mp3", 0.5],
  [47.41, "pop.mp3", 0.5],
  [49.17, "quick-ting.mp3", 0.5],
  [54.0, "pop-2.mp3", 0.5],
  [55.57, "pop.mp3", 0.5],
  [58.97, "pop-2.mp3", 0.5],
  [65.91, "punch.mp3", 0.75],
  [68.6, "quick-swoosh.mp3", 0.5],
  [70.25, "quick-ting.mp3", 0.5],
  [74.23, "correct.mp3", 0.5],
  [76.2, "quick-swoosh.mp3", 0.55],
  [76.45, "punch.mp3", 0.6],
  [76.7, "camera-shutter.mp3", 0.5],
  [77.05, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.4), f(3.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(4.8)} />
    <BigText start={0} end={f(4.8)} y={120} slam lines={[{ text: "Thảm yoga", color: C.white, size: 112 }]} />
    <BigText start={f(0.4)} end={f(4.8)} y={240} slam lines={[{ text: "dùng được bao lâu?", color: C.accent, size: 70 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(4.8)} />
    <Stamp text="Tuỳ cách dùng!" start={f(HOOK_DROP)} end={f(4.8)} x={540} y={G + 150} rot={-6} size={86} />
  </>
);

const Intro: React.FC = () => (
  <>
    <BottomShade start={f(4.9)} end={f(10.2)} />
    <Kicker text="mỗi mẫu thảm" start={f(5.0)} end={f(10.2)} y={G + 40} color={C.white} />
    <Pill text="Độ bền không giống nhau" start={f(9.67)} end={f(10.2)} x={W / 2} y={G + 130} size={46} />
  </>
);

const Compare: React.FC = () => (
  <>
    <BottomShade start={f(19.3)} end={f(23.3)} />
    <Pill text="Tập nhiều" start={f(19.99)} end={f(23.3)} x={300} y={G + 80} size={44} />
    <Pill text="Ra nhiều mồ hôi" start={f(22.21)} end={f(23.3)} x={720} y={G + 80} bg={C.gold} fg={C.ink} size={44} />
    <BottomShade start={f(25.6)} end={f(27.0)} />
    <Stamp text="Độ bền khác" start={f(26.68)} end={f(27.0)} x={540} y={G + 150} rot={-6} size={80} />
  </>
);

const NoFixed: React.FC = () => (
  <>
    <BottomShade start={f(30.1)} end={f(40.6)} />
    <Kicker text="thông thường" start={f(30.2)} end={f(40.6)} y={G + 10} color={C.white} />
    <BigText start={f(33.64)} end={f(40.6)} y={G + 64} slam lines={[{ text: "Không có thời hạn", color: C.accent, size: 84 }, { text: "cố định", color: C.white, size: 70 }]} />
    <Pill text="Tuỳ mỗi người" start={f(39.24)} end={f(40.6)} x={W / 2} y={G + 270} bg={C.gold} fg={C.ink} size={40} />
  </>
);

// Wear map: real Louis mat with glowing hand/foot spots.
const WearMap: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(40.7);
  const e = f(65.8);
  const glow = (at: number) => spring({ frame: frame - f(at), fps: FPS, config: { damping: 10, stiffness: 160 } });
  const g = frame >= f(49.17) ? glow(49.17) : 0;
  const spot = (x: number, y: number) => (
    <div style={{ position: "absolute", left: x - 22, top: y - 22, width: 44, height: 44, borderRadius: 99, background: "rgba(255,90,174,0.55)", border: `3px solid ${C.accent}`, boxShadow: `0 0 ${18 * g}px ${C.accent}`, transform: `scale(${g})` }} />
  );
  return (
    <Panel start={s} end={e} y={G - 40} h={370}>
      <div style={{ position: "absolute", left: 60, top: 26, width: 150, height: 314, borderRadius: 14, overflow: "hidden", border: "3px solid rgba(255,255,255,0.85)" }}>
        <Img src={staticFile("img/asana.jpg")} style={{ width: 150, height: 314, objectFit: "cover" }} />
        {spot(40, 60)}
        {spot(110, 60)}
        {spot(48, 262)}
        {spot(102, 262)}
      </div>
      <div style={{ position: "absolute", left: 250, top: 26, ...font(800, 28), color: C.dim, letterSpacing: 3 }}>Sau thời gian dùng</div>
      <Pill text="Mủn" start={f(46.51)} end={e} x={310} y={80} size={30} />
      <Pill text="Bong tróc" start={f(47.41)} end={e} x={530} y={80} bg={C.gold} fg={C.ink} size={30} />
      {frame >= f(49.17) && <div style={{ position: "absolute", left: 250, top: 140, ...font(900, 40), color: C.accent }}>chỗ đặt tay · đặt chân</div>}
      <Pill text="Dùng thường xuyên" start={f(54.0)} end={e} x={420} y={210} bg="rgba(255,255,255,0.15)" size={30} />
      <Pill text="Mồ hôi" start={f(55.57)} end={e} x={700} y={210} bg="rgba(255,255,255,0.15)" size={30} />
      <Pill text="Ma sát tay chân" start={f(58.97)} end={e} x={500} y={285} bg="rgba(255,255,255,0.15)" size={30} />
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
      <Kicker text="xem thêm mẹo dùng thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/basic.jpg" label="Basic" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 36), color: C.white }}>Bảo quản tốt</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>thảm bền lâu</div>
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
        <SeriesTag start={f(4.8)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <Intro />
        <NumberRows title="Độ bền phụ thuộc" rows={[["Tần suất dùng", 12.19], ["Vệ sinh · bảo quản", 15.29], ["Cường độ tập", 17.63]]} start={10.3} end={19.2} y={G - 60} />
        <Compare />
        <NoFixed />
        <WearMap />
        <BottomShade start={f(65.8)} end={f(68.5)} />
        <Stamp text="Không tránh khỏi" start={f(65.91)} end={f(68.5)} x={540} y={G + 150} rot={-6} size={74} />
        <CheckGrid items={[["Tần suất", 70.25], ["Cường độ", 70.9], ["Bảo quản", 71.6], ["Cách dùng", 74.23]]} start={f(68.6)} end={VIDEO_FRAMES - 3} y={G} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={1.9} until={CLEAN_DURATION} />
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
