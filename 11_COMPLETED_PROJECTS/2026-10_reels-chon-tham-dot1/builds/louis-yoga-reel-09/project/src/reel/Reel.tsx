import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard, RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 09 "Màu thảm khác giá — có khác chất lượng?"
// Louis-only visuals: real Basic colour avatars, louisyoga.vn model photo. No marketplace logos.
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

// ▼ EDIT ▼ camera (9 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24];
const HOOK_DROP = 1.12;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 1.9, 0.18],
  [8.72, 9.6, 0.1],
  [13.32, 14.0, 0.08],
  [22.34, 23.0, 0.08],
  [34.77, 35.4, 0.08],
  [46.12, 46.7, 0.1],
  [50.03, 50.7, 0.1],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 42.9, end: 45.9, film: 0, src: PH + "tu-the/tu-the_137_tham-tap-yoga-cao-su-basic.jpg", mode: "photo", label: "Chuẩn xanh dương" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.5, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.5, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [7.7, "quick-swoosh.mp3", 0.5],
  [8.72, "digital-counting-1.mp3", 0.5],
  [13.32, "pop-2.mp3", 0.5],
  [16.12, "pop.mp3", 0.5],
  [18.99, "pop-2.mp3", 0.5],
  [20.9, "quick-swoosh.mp3", 0.5],
  [25.2, "quick-ting.mp3", 0.5],
  [26.34, "quick-ting.mp3", 0.5],
  [27.44, "quick-ting.mp3", 0.5],
  [30.09, "pop.mp3", 0.5],
  [31.53, "pop-2.mp3", 0.5],
  [32.3, "quick-swoosh.mp3", 0.5],
  [36.61, "quick-ting.mp3", 0.5],
  [37.41, "quick-ting.mp3", 0.5],
  [41.07, "pop-2.mp3", 0.5],
  [42.9, "swoosh.mp3", 0.5],
  [46.81, "quick-swoosh.mp3", 0.5],
  [50.03, "quick-ting.mp3", 0.5],
  [53.68, "correct.mp3", 0.5],
  [58.65, "pop.mp3", 0.5],
  [63.0, "quick-swoosh.mp3", 0.55],
  [63.25, "punch.mp3", 0.7],
  [63.5, "camera-shutter.mp3", 0.5],
  [63.85, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.8), f(2.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const COLORS = [
  ["img/basic_reu.jpg", "Rêu"],
  ["img/basic_den.jpg", "Đen"],
  ["img/basic_ghi.jpg", "Ghi"],
  ["img/basic_do.jpg", "Đỏ"],
  ["img/basic_coban.jpg", "Coban"],
];

// Hook: question, then 5 real colours of the same mat + stamp "chất lượng như nhau".
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(7.6)} />
    <BigText start={0} end={f(7.6)} y={120} slam lines={[{ text: "Màu khác giá", color: C.white, size: 104 }]} />
    <BigText start={f(0.5)} end={f(7.6)} y={232} slam lines={[{ text: "có khác chất lượng?", color: C.accent, size: 76 }]} />
    <Panel start={f(HOOK_DROP)} end={f(7.6)} y={G - 40} h={370}>
      {COLORS.map(([src, label], i) => (
        <MatCard key={label} src={src} label={label} x={34 + i * 170} y={30} w={130} h={270} at={HOOK_DROP + i * 0.08} labelSize={24} />
      ))}
    </Panel>
    <Stamp text="Chất lượng như nhau" start={f(HOOK_DROP + 0.4)} end={f(7.6)} x={540} y={G + 150} rot={-6} size={66} />
  </>
);

// Giá: set chung → trợ giá theo màu → chênh chút ít.
const PriceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(7.7);
  const e = f(20.8);
  return (
    <Panel start={s} end={e} y={G - 20} h={320}>
      <div style={{ position: "absolute", top: 20, left: 0, right: 0, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>Giá bán</div>
      {frame >= f(8.72) && <div style={{ position: "absolute", top: 62, left: 0, right: 0, textAlign: "center", ...font(900, 64), color: C.white }}>Chung mọi màu</div>}
      <Pill text="+ Trợ giá theo màu" start={f(13.32)} end={e} x={230} y={170} size={28} />
      <Pill text="+ Mã giảm của sàn" start={f(16.12)} end={e} x={665} y={170} bg={C.white} fg={C.ink} size={28} />
      <Pill text="→ Chênh lệch chút ít" start={f(18.99)} end={e} x={W / 2 - 50} y={240} bg={C.gold} fg={C.ink} size={34} />
    </Panel>
  );
};

// Colour groups.
const Group: React.FC<{ s: number; e: number; title: string; items: [string, string, number][]; pills: [string, number][] }> = ({ s, e, title, items, pills }) => (
  <Panel start={f(s)} end={f(e)} y={G - 40} h={370}>
    <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.accent, letterSpacing: 2 }}>{title}</div>
    {items.map(([src, label, at], i) => (
      <MatCard key={label} src={src} label={label} x={40 + i * 150} y={62} w={110} h={240} at={at} active labelSize={22} />
    ))}
    {pills.map(([t, at], i) => (
      <Pill key={t} text={t} start={f(at)} end={f(e)} x={720} y={110 + i * 90} bg={i ? C.gold : C.pinkDeep} fg={i ? C.ink : C.white} size={32} />
    ))}
  </Panel>
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
      <Polaroid src="img/basic_coban.jpg" label="Coban" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/basic_reu.jpg" label="Rêu" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 70, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 36), color: C.white }}>Mọi màu</div>
        <div style={{ ...font(900, 40), color: C.accent }}>cùng</div>
        <div style={{ ...font(900, 40), color: C.accent }}>chất lượng</div>
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
        <SeriesTag start={f(7.6)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <PriceScene />
        <Group s={20.9} e={32.2} title="Thích màu trầm · sạch" items={[["img/basic_reu.jpg", "Rêu", 25.2], ["img/basic_den.jpg", "Đen", 26.34], ["img/basic_ghi.jpg", "Ghi đậm", 27.44]]} pills={[["Dễ dùng", 30.09], ["Đỡ lộ bẩn", 31.53]]} />
        <Group s={32.3} e={42.85} title="Thích màu sáng" items={[["img/basic_do.jpg", "Đỏ", 36.61], ["img/basic_coban.jpg", "Coban", 37.41]]} pills={[["Sáng · đẹp", 41.07]]} />
        <RecapRows title="Chọn màu nào?" rows={[["Màu sáng", "Xanh coban", 50.03], ["An toàn", "Ghi · Rêu", 53.68]]} start={46.81} end={(VIDEO_FRAMES - 3) / FPS} y={G - 20} footer={["gam trầm dễ dùng hơn", 58.65]} />
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
