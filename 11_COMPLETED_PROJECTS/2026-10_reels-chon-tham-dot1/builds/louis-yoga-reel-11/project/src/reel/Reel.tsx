import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard, NumberRows, RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 11 "Thảm mới mở ra có mùi — có sao không?"
// Louis-only visuals: Louis mat-spray product photos, louisyoga.vn lifestyle/material photos.
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
const SPRAY = PH + "xit-ve-sinh/xit-ve-sinh_318_xit-tham-yoga-huong-chanh-sa.jpg";

// ▼ EDIT ▼ camera (13 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24, 1.12, 1.28, 1.14, 1.22];
const HOOK_DROP = 2.07;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.8, 0.18],
  [8.36, 9.2, 0.1],
  [19.4, 20.2, 0.12],
  [34.25, 35.0, 0.1],
  [46.5, 47.2, 0.1],
  [56.27, 57.0, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 10.2, end: 12.6, film: 0, src: PH + "sinh-hoat/sinh-hoat_258_tham-tap-yoga-cao-su-sunflower-2.jpg", mode: "photo", label: "Chất liệu cao su" },
  { start: 27.2, end: 29.6, film: 0, src: SPRAY, mode: "photo", label: "Xịt vệ sinh thảm" },
  { start: 31.0, end: 32.9, film: 0, src: PH + "sinh-hoat/sinh-hoat_109_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Để thoáng · bóng mát" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.39, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [19.4, 6, 8, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.39, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [6.3, "quick-swoosh.mp3", 0.5],
  [8.36, "pop-2.mp3", 0.5],
  [10.2, "swoosh.mp3", 0.5],
  [13.76, "pop.mp3", 0.5],
  [19.4, "punch.mp3", 0.75],
  [21.0, "quick-swoosh.mp3", 0.5],
  [24.86, "quick-ting.mp3", 0.5],
  [27.2, "swoosh.mp3", 0.5],
  [29.39, "quick-ting.mp3", 0.5],
  [31.0, "swoosh.mp3", 0.45],
  [33.01, "quick-ting.mp3", 0.5],
  [34.25, "pop-2.mp3", 0.5],
  [39.11, "quick-ting.mp3", 0.5],
  [42.2, "quick-swoosh.mp3", 0.5],
  [46.5, "pop-2.mp3", 0.5],
  [50.8, "quick-swoosh.mp3", 0.5],
  [52.79, "quick-ting.mp3", 0.5],
  [52.9, "correct.mp3", 0.45],
  [56.27, "punch.mp3", 0.7],
  [57.6, "quick-swoosh.mp3", 0.55],
  [57.85, "punch.mp3", 0.6],
  [58.1, "camera-shutter.mp3", 0.5],
  [58.45, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.6), f(3.2), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(6.2)} />
    <BigText start={0} end={f(6.2)} y={120} slam lines={[{ text: "Thảm mới có mùi", color: C.white, size: 96 }]} />
    <BigText start={f(0.39)} end={f(6.2)} y={232} slam lines={[{ text: "có sao không?", color: C.accent, size: 110 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(6.2)} />
    <Stamp text="Mùi đặc trưng cao su" start={f(HOOK_DROP)} end={f(6.2)} x={540} y={G + 150} rot={-6} size={62} />
  </>
);

// Material: rubber smell, same for any rubber product.
const Material: React.FC = () => (
  <>
    <Panel start={f(6.3)} end={f(10.15)} y={G - 20} h={300}>
      <MatCard src={PH + "be-mat/be-mat_076_tham-tap-yoga-cao-su-asana-25.jpg"} x={30} y={24} w={250} h={250} at={6.3} />
      <div style={{ position: "absolute", left: 320, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Mới mở thảm</div>
      <div style={{ position: "absolute", left: 320, top: 86, ...font(900, 54), color: C.white }}>Có chút mùi</div>
      <Pill text="Mùi đặc trưng chất liệu" start={f(8.36)} end={f(10.15)} x={580} y={200} size={30} />
    </Panel>
    <BottomShade start={f(12.6)} end={f(20.8)} />
    <Kicker text="mọi sản phẩm cao su" start={f(13.0)} end={f(20.8)} y={G + 20} color={C.white} />
    <Pill text="Mới mở đều có mùi" start={f(13.76)} end={f(20.8)} x={W / 2} y={G + 100} size={46} />
    <Stamp text="Không tránh được" start={f(19.4)} end={f(20.8)} x={540} y={G + 230} rot={-6} size={60} />
  </>
);

// Spray scene for sensitive noses.
const Sensitive: React.FC = () => {
  const s = f(42.2);
  const e = f(50.6);
  return (
    <Panel start={s} end={e} y={G - 20} h={300}>
      <MatCard src={SPRAY} x={30} y={24} w={250} h={250} at={42.3} active />
      <div style={{ position: "absolute", left: 320, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Nhạy cảm với mùi?</div>
      <div style={{ position: "absolute", left: 320, top: 86, ...font(900, 50), color: C.white }}>Mua thêm</div>
      <div style={{ position: "absolute", left: 320, top: 144, ...font(900, 50), color: C.accent, opacity: useCurrentFrame() >= f(46.5) ? 1 : 0 }}>xịt vệ sinh thảm</div>
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
      <Polaroid src={SPRAY} label="Xịt thảm" start={s + 8} end={DURATION + 1} x={60} y={G - 40} w={230} h={230} rot={-7} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_109_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Để thoáng" start={s + 12} end={DURATION + 1} x={760} y={G - 30} w={210} h={210} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Mở thoáng</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>mùi bay bớt</div>
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
        <SeriesTag start={f(6.2)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <Material />
        <NumberRows title="Cách khử mùi" rows={[["Để thảm thoáng", 24.86]]} start={21.0} end={27.15} y={G - 20} />
        <NumberRows title="Để thoáng đúng cách" rows={[["Nơi bóng mát", 33.01], ["Không phơi nắng", 34.25], ["Tập vài buổi", 39.11]]} start={33.0} end={42.1} y={G - 60} />
        <Sensitive />
        <RecapRows title="Thảm mới có mùi?" rows={[["Đa số", "Mở thoáng", 52.79], ["Nhạy mùi", "Xịt thảm", 52.9]]} start={50.8} end={56.1} y={G - 20} />
        <BottomShade start={f(56.1)} end={VIDEO_FRAMES - 2} />
        <Stamp text="Đặc trưng chất liệu" start={f(56.27)} end={VIDEO_FRAMES - 2} x={540} y={G + 150} rot={-6} size={64} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={2.1} until={CLEAN_DURATION} />
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
