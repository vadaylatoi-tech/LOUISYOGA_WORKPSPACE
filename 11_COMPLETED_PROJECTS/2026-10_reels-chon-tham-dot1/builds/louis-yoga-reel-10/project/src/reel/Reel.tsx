import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 10 "Thảm TPE — nên chọn loại 1 lớp, hợp với ai?"
// TPE facts from louisyoga.vn (TPE9: đúc liền 1 lớp, 9 mm). Louis-only visuals.
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
const HOOK_DROP = 1.89;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.6, 0.16],
  [5.79, 6.5, 0.14],
  [13.59, 14.3, 0.1],
  [24.83, 25.6, 0.14],
  [43.14, 43.8, 0.08],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 26.5, end: 28.9, film: 0, src: PH + "tu-the/tu-the_291_tham-tap-yoga-tpe-dinh-tuyen-tpe9.jpg", mode: "photo", label: "Bắt đầu làm quen yoga" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 8, 12, 0.4],
  [5.79, 10, 18, 0.5],
  [24.83, 7, 9, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "quick-swoosh.mp3", 0.55],
  [5.79, "riser-metallic.mp3", 0.5],
  [5.79, "punch.mp3", 0.95],
  [7.07, "pop-2.mp3", 0.5],
  [9.3, "quick-swoosh.mp3", 0.5],
  [13.59, "quick-ting.mp3", 0.5],
  [14.91, "pop.mp3", 0.5],
  [17.6, "quick-swoosh.mp3", 0.5],
  [19.53, "pop-2.mp3", 0.5],
  [21.63, "pop.mp3", 0.5],
  [24.83, "punch.mp3", 0.8],
  [26.5, "swoosh.mp3", 0.5],
  [29.43, "pop-2.mp3", 0.5],
  [31.3, "quick-swoosh.mp3", 0.5],
  [36.93, "pop.mp3", 0.5],
  [43.14, "quick-ting.mp3", 0.5],
  [44.2, "quick-ting.mp3", 0.5],
  [45.2, "quick-ting.mp3", 0.5],
  [49.1, "correct.mp3", 0.5],
  [55.35, "quick-swoosh.mp3", 0.55],
  [55.6, "punch.mp3", 0.7],
  [55.85, "camera-shutter.mp3", 0.5],
  [56.2, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.4), f(3.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <TopShade start={0} end={f(9.2)} />
      <BigText start={0} end={f(9.2)} y={120} slam lines={[{ text: "Thảm TPE", color: C.white, size: 112 }]} />
      <BigText start={f(0.4)} end={f(9.2)} y={240} slam lines={[{ text: "nên chọn loại nào?", color: C.accent, size: 80 }]} />
      <Panel start={f(HOOK_DROP)} end={f(9.2)} y={G - 40} h={370}>
        <MatCard src="img/tpe_pink.jpg" x={30} y={30} w={300} h={300} at={HOOK_DROP} />
        <div style={{ position: "absolute", left: 370, top: 30, ...font(800, 28), color: C.dim, letterSpacing: 3 }}>Thảm TPE · Louis Yoga</div>
        {frame >= f(5.79) && <div style={{ position: "absolute", left: 370, top: 76, ...font(900, 92), color: C.accent }}>1 lớp</div>}
        <Pill text="✓ Độ bền cao hơn" start={f(7.07)} end={f(9.2)} x={600} y={250} bg={C.gold} fg={C.ink} size={34} />
      </Panel>
    </>
  );
};

// Louis TPE = đúc liền 1 lớp.
const LouisTpe: React.FC = () => {
  const s = f(9.3);
  const e = f(17.5);
  const mats = ["tpe_green", "tpe_blue", "tpe_purple", "tpe_pink"];
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <div style={{ position: "absolute", top: 16, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.gold, letterSpacing: 2 }}>TPE Louis Yoga · đúc liền 1 lớp</div>
        {mats.map((m, i) => (
          <MatCard key={m} src={`img/${m}.jpg`} x={40 + i * 210} y={76} w={190} h={190} at={9.4 + i * 0.12} active={i === 3} />
        ))}
      </Panel>
      <Pill text="✓ Bền hơn · tập thoải mái" start={f(14.91)} end={e} x={W / 2} y={G + 255} size={38} />
    </>
  );
};

// 1 lớp vs 2 lớp: the cheap 2-layer mat peels apart on "bong tách".
const Layers: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(17.6);
  const e = f(25.7);
  const split = interpolate(frame, [f(24.83), f(24.83) + 12], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  const show2 = frame >= f(19.53);
  const slab = (x: number, y: number, w: number, h: number, bg: string, rot = 0) => (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 10, background: bg, transform: `rotate(${rot}deg)`, transformOrigin: "left center", boxShadow: "0 6px 14px rgba(0,0,0,0.4)" }} />
  );
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <div style={{ position: "absolute", left: 40, top: 26, width: 380, textAlign: "center", ...font(900, 34), color: C.accent }}>TPE 1 lớp</div>
        {slab(70, 140, 320, 70, `linear-gradient(180deg, ${C.accent}, ${C.pinkDeep})`)}
        <div style={{ position: "absolute", left: 40, top: 240, width: 380, textAlign: "center", ...font(800, 26), color: C.white }}>đúc liền · bền</div>
        <div style={{ position: "absolute", left: 425, top: 150, width: 50, textAlign: "center", ...font(900, 36), color: C.gold }}>VS</div>
        {show2 && (
          <>
            <div style={{ position: "absolute", left: 480, top: 26, width: 380, textAlign: "center", ...font(900, 34), color: C.white }}>Giá rẻ · {frame >= f(21.63) ? "2 lớp" : "?"}</div>
            {slab(510, 130 - 26 * split, 320, 36, "#B7A9C9", -9 * split)}
            {slab(510, 172 + 10 * split, 320, 36, "#8E80A3")}
          </>
        )}
      </Panel>
      <Stamp text="Dễ bong tách!" start={f(24.83)} end={e} x={680} y={G + 230} rot={-7} size={58} />
    </>
  );
};

const Beginner: React.FC = () => (
  <>
    <BottomShade start={f(28.9)} end={f(31.2)} />
    <Pill text="✓ Tập thể dục nhẹ nhàng" start={f(29.43)} end={f(31.2)} x={W / 2} y={G + 160} size={44} />
  </>
);

const Kids: React.FC = () => (
  <>
    <BottomShade start={f(31.3)} end={f(42.3)} />
    <Kicker text="TPE · các mẹ mua cho con" start={f(31.4)} end={f(42.3)} y={G + 30} color={C.white} />
    <Pill text="Yoga trong trường học" start={f(36.93)} end={f(42.3)} x={W / 2} y={G + 130} bg={C.gold} fg={C.ink} size={44} />
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
      <Kicker text="xem thêm mẹo chọn thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src="img/tpe_pink.jpg" label="TPE 1 lớp" start={s + 8} end={DURATION + 1} x={60} y={G - 40} w={230} h={230} rot={-7} />
      <Polaroid src="img/tpe_blue.jpg" label="TPE 9 ly" start={s + 12} end={DURATION + 1} x={760} y={G - 30} w={210} h={210} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Bền · êm</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>người mới</div>
        <div style={{ ...font(900, 40), color: C.accent }}>& trẻ em</div>
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
        <SeriesTag start={f(9.2)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <LouisTpe />
        <Layers />
        <Beginner />
        <Kids />
        <CheckGrid items={[["Êm ái", 43.14], ["Bền 1 lớp", 44.2], ["Hợp trẻ em", 45.2], ["Người mới", 49.1]]} start={f(42.4)} end={VIDEO_FRAMES - 3} y={G} />
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
