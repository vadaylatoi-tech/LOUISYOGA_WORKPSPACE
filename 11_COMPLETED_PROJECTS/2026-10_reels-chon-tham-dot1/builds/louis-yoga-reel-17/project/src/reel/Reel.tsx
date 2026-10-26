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
// LOUIS YOGA REEL — STYLE 1.  Video 17 "Mới tập, sợ mình cứng không hợp yoga"
// Louis-only visuals: product avatars, louisyoga.vn photos, brand film.
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
const HOOK_DROP = 1.64;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.4, 0.16],
  [13.3, 14.1, 0.14],
  [16.02, 16.7, 0.1],
  [27.96, 28.6, 0.1],
  [44.99, 45.7, 0.1],
  [58.68, 59.4, 0.08],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 30.2, end: 32.8, film: 12.3, cx: 940, mode: "fit", label: "Mới tập yoga" },
  { start: 55.5, end: 57.8, film: 0, src: PH + "sinh-hoat/sinh-hoat_302_tui-da-nang-cao-cap-m2261.jpg", mode: "photo", label: "Mang đi tập" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 8, 12, 0.4],
  [13.3, 10, 18, 0.5],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "quick-swoosh.mp3", 0.55],
  [6.6, "pop.mp3", 0.5],
  [8.94, "pop-2.mp3", 0.5],
  [11.2, "pop.mp3", 0.5],
  [13.3, "riser-metallic.mp3", 0.5],
  [13.3, "punch.mp3", 0.95],
  [16.02, "pop-2.mp3", 0.5],
  [18.36, "quick-ting.mp3", 0.5],
  [22.4, "quick-ting.mp3", 0.5],
  [23.7, "quick-swoosh.mp3", 0.5],
  [27.96, "correct.mp3", 0.5],
  [30.2, "swoosh.mp3", 0.5],
  [34.95, "pop.mp3", 0.5],
  [38.83, "quick-ting.mp3", 0.5],
  [44.99, "punch.mp3", 0.7],
  [47.6, "quick-swoosh.mp3", 0.5],
  [50.65, "quick-ting.mp3", 0.5],
  [55.5, "swoosh.mp3", 0.45],
  [58.68, "quick-ting.mp3", 0.5],
  [59.36, "correct.mp3", 0.5],
  [61.15, "quick-swoosh.mp3", 0.55],
  [61.4, "punch.mp3", 0.6],
  [61.65, "camera-shutter.mp3", 0.5],
  [62.0, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.2), f(2.8), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(5.2)} />
    <BigText start={0} end={f(5.2)} y={120} slam lines={[{ text: "Mới tập, người cứng", color: C.white, size: 78 }]} />
    <BigText start={f(0.4)} end={f(5.2)} y={212} slam lines={[{ text: "có hợp yoga không?", color: C.accent, size: 72 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(5.2)} />
    <Pill text="Lăn tăn trước khi tập?" start={f(HOOK_DROP)} end={f(5.2)} x={W / 2} y={G + 140} bg="rgba(14,10,16,0.85)" size={46} />
  </>
);

const Worries: React.FC = () => (
  <>
    <BottomShade start={f(5.3)} end={f(12.45)} />
    <Pill text="Người cứng?" start={f(6.6)} end={f(12.45)} x={300} y={G + 60} bg="rgba(255,255,255,0.15)" size={40} />
    <Pill text="Không giãn được cơ?" start={f(8.94)} end={f(12.45)} x={680} y={G + 150} bg="rgba(255,255,255,0.15)" size={40} />
    <Pill text="Không hợp yoga?" start={f(11.2)} end={f(12.45)} x={360} y={G + 240} bg="rgba(255,255,255,0.15)" size={40} />
  </>
);

const NotYou: React.FC = () => (
  <>
    <BottomShade start={f(12.5)} end={f(23.6)} />
    <Stamp text="Không phải do bạn!" start={f(13.3)} end={f(15.9)} x={540} y={G + 140} rot={-6} size={68} />
    <Kicker text="mà còn do dụng cụ" start={f(16.02)} end={f(23.6)} y={G + 20} color={C.white} />
    <Pill text="✓ Đáp ứng nhu cầu tập" start={f(18.36)} end={f(23.6)} x={W / 2} y={G + 100} size={44} />
    <Pill text="✓ Bổ trợ tốt cho mình" start={f(22.4)} end={f(23.6)} x={W / 2} y={G + 200} bg={C.gold} fg={C.ink} size={44} />
  </>
);

const Choose: React.FC = () => (
  <Panel start={f(23.7)} end={f(30.15)} y={G - 40} h={370}>
    <div style={{ position: "absolute", top: 16, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.gold, letterSpacing: 2 }}>Dòng chất lượng tốt hơn</div>
    <MatCard src="img/basic.jpg" label="Basic" x={140} y={70} w={120} h={240} at={27.96} active />
    <MatCard src="img/asana25.jpg" label="Asana 25" x={390} y={70} w={120} h={240} at={28.1} active />
    <MatCard src="img/queen.jpg" label="Queen" x={640} y={70} w={120} h={240} at={28.24} active />
  </Panel>
);

const Mind: React.FC = () => (
  <>
    <BottomShade start={f(32.8)} end={f(47.5)} />
    <Kicker text="tâm lý: có theo được không?" start={f(32.9)} end={f(47.5)} y={G + 10} color={C.white} />
    <Pill text="Thảm tốt giúp mình yên tâm" start={f(38.83)} end={f(47.5)} x={W / 2} y={G + 90} size={42} />
    <BigText start={f(44.99)} end={f(47.5)} y={G + 170} slam lines={[{ text: "Tâm trạng tốt hơn", color: C.accent, size: 84 }]} />
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
      <Polaroid src="img/basic.jpg" label="Basic" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 38), color: C.white }}>Ai cũng</div>
        <div style={{ ...font(900, 40), color: C.accent, marginTop: 8 }}>tập được</div>
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
        <SeriesTag start={f(5.2)} end={VIDEO_FRAMES} tag="Mẹo cho người mới" brand="Louis Yoga" />
        <Worries />
        <NotYou />
        <Choose />
        <Mind />
        <CheckGrid items={[["Phù hợp", 50.65], ["Thoải mái", 58.68], ["Tâm thế tốt", 59.36]]} start={f(47.6)} end={VIDEO_FRAMES - 3} y={G} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={1.6} until={CLEAN_DURATION} />
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
