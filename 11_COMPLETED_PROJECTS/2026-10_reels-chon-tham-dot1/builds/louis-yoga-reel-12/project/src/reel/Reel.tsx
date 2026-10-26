import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { DoDont, NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 12 "Có nên giặt thảm cao su?"
// Louis-only visuals: Louis towel / mat spray / rolling photos (louisyoga.vn).
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

// ▼ EDIT ▼ camera (13 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24, 1.12, 1.28, 1.14, 1.22];
const HOOK_DROP = 1.4;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.2, 0.18],
  [7.84, 8.5, 0.1],
  [26.29, 27.0, 0.1],
  [45.23, 45.9, 0.08],
  [60.42, 61.2, 0.14],
  [72.27, 72.9, 0.08],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 34.45, end: 36.7, film: 0, src: PH + "khan/khan_059_khan-lau-mo-hoi-tap-yoga.jpg", mode: "photo", label: "Lau bằng khăn ẩm" },
  { start: 38.9, end: 40.65, film: 0, src: PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg", mode: "photo", label: "Nước vệ sinh thảm" },
  { start: 43.3, end: 45.2, film: 0, src: PH + "sinh-hoat/sinh-hoat_109_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Để thảm thoáng, khô" },
  { start: 52.5, end: 55.0, film: 0, src: PH + "cuon-tham/cuon-tham_007_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg", mode: "photo", label: "Cuộn mang về nhà" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [60.42, 6, 8, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [9.0, "quick-swoosh.mp3", 0.5],
  [11.8, "quick-ting.mp3", 0.5],
  [16.84, "quick-ting.mp3", 0.5],
  [26.29, "quick-ting.mp3", 0.5],
  [29.4, "quick-swoosh.mp3", 0.5],
  [32.69, "pop-2.mp3", 0.5],
  [34.45, "swoosh.mp3", 0.5],
  [38.9, "swoosh.mp3", 0.45],
  [43.3, "swoosh.mp3", 0.45],
  [45.23, "pop.mp3", 0.5],
  [46.3, "quick-swoosh.mp3", 0.5],
  [52.5, "swoosh.mp3", 0.45],
  [58.52, "pop-2.mp3", 0.5],
  [60.42, "punch.mp3", 0.75],
  [66.9, "quick-swoosh.mp3", 0.5],
  [72.27, "pop.mp3", 0.5],
  [74.57, "quick-ting.mp3", 0.5],
  [77.37, "pop.mp3", 0.5],
  [78.57, "pop-2.mp3", 0.5],
  [81.0, "correct.mp3", 0.45],
  [82.05, "quick-swoosh.mp3", 0.55],
  [82.3, "punch.mp3", 0.6],
  [82.55, "camera-shutter.mp3", 0.5],
  [82.9, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.9), f(2.5), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(8.9)} />
    <BigText start={0} end={f(8.9)} y={120} slam lines={[{ text: "Thảm cao su", color: C.white, size: 110 }]} />
    <BigText start={f(0.4)} end={f(8.9)} y={240} slam lines={[{ text: "có nên giặt?", color: C.accent, size: 116 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(8.9)} />
    <Stamp text="Không nên giặt!" start={f(HOOK_DROP)} end={f(8.9)} x={540} y={G + 150} rot={-6} size={86} />
  </>
);

const Clean: React.FC = () => (
  <>
    <BottomShade start={f(29.4)} end={f(34.45)} />
    <Kicker text="vệ sinh đúng cách" start={f(29.5)} end={f(34.45)} y={G + 30} color={C.white} />
    <Pill text="✓ Chỉ lau qua bề mặt" start={f(32.69)} end={f(34.45)} x={W / 2} y={G + 120} size={48} />
    <BottomShade start={f(36.7)} end={f(38.9)} />
    <Pill text="✓ Kết hợp xịt vệ sinh" start={f(36.75)} end={f(38.9)} x={W / 2} y={G + 140} bg={C.gold} fg={C.ink} size={46} />
    <BottomShade start={f(45.2)} end={f(46.25)} />
    <Pill text="✓ Để khô thoáng" start={f(45.23)} end={f(46.25)} x={W / 2} y={G + 140} size={48} />
  </>
);

const ClassCase: React.FC = () => (
  <>
    <BottomShade start={f(46.3)} end={f(52.5)} />
    <Kicker text="tập ở lớp, không kịp chờ khô?" start={f(46.4)} end={f(52.5)} y={G + 40} color={C.white} />
    <BottomShade start={f(55.0)} end={f(64.5)} />
    <Pill text="Mở thoáng khi về nhà" start={f(55.0)} end={f(64.5)} x={W / 2} y={G + 60} size={42} />
    <Pill text="Ở lớp: cuộn lỏng tay" start={f(58.52)} end={f(64.5)} x={W / 2} y={G + 150} bg={C.gold} fg={C.ink} size={42} />
    <Stamp text="Đừng cuộn chặt!" start={f(60.42)} end={f(64.5)} x={540} y={G + 270} rot={-6} size={64} />
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
      <Polaroid src={PH + "khan/khan_059_khan-lau-mo-hoi-tap-yoga.jpg"} label="Lau khăn ẩm" start={s + 8} end={DURATION + 1} x={60} y={G - 40} w={230} h={230} rot={-7} />
      <Polaroid src={PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg"} label="Xịt thảm" start={s + 12} end={DURATION + 1} x={760} y={G - 30} w={210} h={210} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Không giặt</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>lau là đủ</div>
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
        <SeriesTag start={f(8.9)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <NumberRows title="Vì sao không nên giặt?" rows={[["Thấm nước nhiều", 11.8], ["Hơi ẩm đọng lại", 16.84], ["Hại bề mặt thảm", 26.29]]} start={9.0} end={29.3} y={G - 60} />
        <Clean />
        <ClassCase />
        <DoDont title="Lưu ý khi vệ sinh" rows={[["Chất tẩy rửa mạnh", 72.27, false], ["Nước vệ sinh chuyên dụng", 74.57, true], ["Phơi nắng trực tiếp", 77.37, false], ["Cuộn khi thảm ướt", 78.57, false]]} start={66.9} end={(VIDEO_FRAMES - 3) / FPS} y={G - 70} size={38} />
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
