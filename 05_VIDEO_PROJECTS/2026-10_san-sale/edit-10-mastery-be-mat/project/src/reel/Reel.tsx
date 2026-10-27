import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import {
  BigText,
  BottomShade,
  Impact,
  Kicker,
  Panel,
  PhotoCard,
  Pill,
  Polaroid,
  SeriesTag,
  Stamp,
  StrikeLine,
  TopShade,
  useImpact,
} from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Thảm tập thường xuyên và Mastery khác nhau ở bề mặt"
// (series Săn sale, video 10). Built on the approved v4 template / video 02; only ▼ EDIT ▼ differs.
// NOTE: the speaker touches both standing mats (blue + purple) without clearly naming which is which,
// so no graphic labels a physical mat as "Mastery" — camera focus only shows "2 bề mặt".
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same standing set as video 01/02 (shelf behind, two mats + foam blocks on the table).
const CAP_Y = 1060;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 10 segments (9 cuts), alternate tight/wide.
const SEG_ZOOM = [1.22, 1.1, 1.26, 1.12, 1.28, 1.12, 1.24, 1.1, 1.26, 1.14];
const HOOK_DROP = 1.48; // "bề MẶT"
const NHAM = 25.05; // "nhám lì" (2nd time, Mastery)
const PICK = 41.71; // "dòng Mastery nhé"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.4, 0.22], // hook drop
  [3.3, 3.9, 0.08], // "nhám lì"
  [5.3, 6.2, 0.08], // "độ bám cao hơn"
  [NHAM, 25.8, 0.14], // "nhám lì"
  [29.03, 29.7, 0.1], // "vượt trội"
  [PICK, 42.4, 0.12], // "Mastery nhé"
];
// [start, end, x, y, zoom] — slide onto the two standing mats / the hand on the surface.
const FOCUS: Focus[] = [
  [10.75, 15.05, 730, 820, 1.26], // "để cho mọi người thấy 2 dòng khác nhau thế nào"
  [26.25, 28.3, 735, 640, 1.3], // "độ bám tay này"
];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 28.35, end: 29.83, film: 0, src: PH + "tu-the/tu-the_091_tham-tap-yoga-cao-su-asana.jpg", mode: "photo", label: "Bám tay, chống trượt" },
  { start: 36.9, end: 38.4, film: 0, src: PH + "tu-the/tu-the_219_tham-tap-yoga-cao-su-moon.jpg", mode: "photo", label: "Tập chuyên sâu" },
  // closing line over the speaker walking off — held under the CTA so it never whips out
  { start: 42.43, end: DURATION / FPS + 0.5, film: 0, src: PH + "be-mat/be-mat_077_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "Thoải mái hơn" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [NHAM, 7, 9, 0],
  [PICK, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density, one sound per beat. Times as NUMBERS (measure_sfx skips names).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [1.48, "riser-metallic.mp3", 0.45],
  [1.48, "punch.mp3", 0.95],
  [2.66, "quick-swoosh.mp3", 0.5], // panel: Mastery column
  [3.3, "pop-2.mp3", 0.5], // nhám lì
  [5.3, "pop.mp3", 0.5], // bám cao hơn
  [6.37, "quick-swoosh.mp3", 0.47], // thường xuyên column
  [9.03, "pop-2.mp3", 0.5], // hơi bóng
  [10.75, "quick-swoosh.mp3", 0.45], // focus: 2 mats
  [12.67, "pop.mp3", 0.5], // 2 dòng
  [15.17, "quick-swoosh.mp3", 0.5], // panel: thường xuyên = cao su
  [17.9, "quick-ting.mp3", 0.5], // nhẵn hơn
  [19.45, "quick-swoosh.mp3", 0.47], // Mastery
  [21.41, "pop-2.mp3", 0.5], // cao su tự nhiên
  [22.23, "pop.mp3", 0.5], // mật độ cao hơn
  [23.71, "pop-2.mp3", 0.5], // PU sinh thái
  [25.05, "punch.mp3", 0.85], // NHÁM LÌ!
  [27.63, "quick-ting.mp3", 0.5], // bám tay
  [28.35, "swoosh.mp3", 0.5], // photo in
  [30.6, "pop-2.mp3", 0.5], // mức đầu tư
  [32.42, "quick-swoosh.mp3", 0.5], // recap
  [34.08, "quick-ting.mp3", 0.53], // ✓ cơ bản
  [36.9, "swoosh.mp3", 0.5], // photo in
  [37.51, "quick-ting.mp3", 0.53], // ✓ chuyên sâu
  [39.53, "correct.mp3", 0.53], // ✓ mồ hôi
  [41.71, "punch.mp3", 0.8], // CHỌN MASTERY
  [42.43, "swoosh.mp3", 0.5], // photo in
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.2), f(2.8), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Label: React.FC<{ x: number; y: number; size: number; color: string; children: React.ReactNode; spacing?: number; weight?: number; w?: number; align?: "left" | "center" }> = ({
  x,
  y,
  size,
  color,
  children,
  spacing = 0,
  weight = 900,
  w,
  align = "left",
}) => <div style={{ position: "absolute", left: x, top: y, width: w, textAlign: align, ...font(weight, size), color, letterSpacing: spacing }}>{children}</div>;

// Hook (0–2.6 s): "THẢM NÀO / CŨNG NHƯ NHAU?" slams, gets crossed out, "KHÁC Ở BỀ MẶT!" stamp drops.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(2.62)} />
    <BigText start={0} end={f(2.62)} y={120} slam lines={[{ text: "Thảm nào", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(2.62)} y={232} slam lines={[{ text: "cũng như nhau?", color: C.accent, size: 94 }]} />
    <StrikeLine d="M110,345 L970,290" start={f(HOOK_DROP)} end={f(2.62)} length={870} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.6)} />
    <Stamp text="Khác ở bề mặt!" start={f(HOOK_DROP)} end={f(2.6)} x={540} y={G + 130} rot={-8} size={96} />
  </>
);

// Two-column comparison that builds while she speaks: Mastery (2.66–6.3) then Thường xuyên (6.37–10.6).
const CompareScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(2.66);
  const e = f(10.6);
  const right = f(6.37);
  const vs = interpolate(frame, [right, right + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  return (
    <Panel start={s} end={e} y={G} h={300}>
      <Label x={20} y={20} w={410} align="center" size={42} color={C.gold}>MASTERY</Label>
      <Pill text="PU sinh thái" start={s} end={e} x={225} y={98} bg={C.white} fg={C.ink} size={32} />
      <Pill text="Nhám lì" start={f(3.3)} end={e} x={225} y={164} bg={C.pinkDeep} size={32} />
      <Pill text="Bám cao hơn" start={f(5.3)} end={e} x={225} y={230} bg={C.gold} fg={C.ink} size={32} />
      <div style={{ position: "absolute", left: 449, top: 30, width: 2, height: 240, background: "rgba(255,255,255,0.25)" }} />
      {frame >= right && (
        <div style={{ position: "absolute", left: 412, top: 126, width: 76, height: 76, borderRadius: 99, background: C.gold, color: C.ink, display: "flex", alignItems: "center", justifyContent: "center", ...font(900, 32), transform: `scale(${vs})` }}>VS</div>
      )}
      {frame >= right && (
        <>
          <Label x={470} y={20} w={410} align="center" size={42} color={C.white}>THƯỜNG XUYÊN</Label>
          <Pill text="Hơi bóng hơn" start={f(9.03)} end={e} x={675} y={98} bg={C.white} fg={C.ink} size={32} />
          <Pill text="Nhẵn hơn" start={f(10.07)} end={e} x={675} y={164} bg="#3A3340" size={32} />
        </>
      )}
    </Panel>
  );
};

// "đây em để đây để cho mọi người thấy 2 dòng chất liệu này khác nhau như thế nào" — camera slides onto the mats.
const ShowScene: React.FC = () => (
  <>
    <Kicker text="So sánh trực tiếp" start={f(10.75)} end={f(15.05)} y={300} color={C.gold} />
    <Pill text="2 dòng · 2 bề mặt" start={f(12.67)} end={f(15.05)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
  </>
);

// "Dòng thường xuyên: chất liệu cũng là cao su tự nhiên, nhưng bề mặt nhẵn hơn".
const RegularScene: React.FC = () => {
  const s = f(15.17);
  const e = f(19.4);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src="brand/rubber_rolls.jpg" label="Cao su tự nhiên" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Dòng thường xuyên</Label>
      <Label x={370} y={80} size={58} color={C.white}>Cao su</Label>
      <Label x={370} y={140} size={58} color={C.accent}>tự nhiên</Label>
      <Pill text="Bề mặt nhẵn hơn" start={f(17.9)} end={e} x={720} y={214} bg={C.gold} fg={C.ink} size={34} />
    </Panel>
  );
};

// "Còn dòng Mastery: cao su tự nhiên, mật độ cao su cao hơn, bề mặt PU sinh thái nhám lì".
const MasteryScene: React.FC = () => {
  const s = f(19.45);
  const e = f(25.83);
  return (
    <>
      <Kicker text="Còn dòng Mastery" start={s} end={e} y={300} color={C.gold} />
      <Panel start={f(21.3)} end={e} y={G} h={270}>
        <Pill text="Cao su tự nhiên" start={f(21.41)} end={e} x={250} y={50} bg={C.white} fg={C.ink} size={36} />
        <Pill text="Mật độ cao su ↑" start={f(22.23)} end={e} x={665} y={50} bg={C.pinkDeep} size={36} />
        <Pill text="Bề mặt PU sinh thái" start={f(23.71)} end={e} x={250} y={160} bg={C.gold} fg={C.ink} size={34} />
        <Stamp text="Nhám lì!" start={f(NHAM)} end={e} x={665} y={172} rot={-7} size={64} />
      </Panel>
    </>
  );
};

// "nên là nó sẽ có cái độ bám tay này, độ chống chân trượt vượt trội hơn hẳn" + "tùy mức đầu tư / nhu cầu".
const GripScene: React.FC = () => (
  <>
    <Pill text="✓ Bám tay" start={f(27.63)} end={f(28.33)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
    <Kicker text="Chọn tuỳ theo" start={f(29.86)} end={f(32.4)} y={300} color={C.gold} />
    <Pill text="Mức đầu tư" start={f(30.6)} end={f(32.4)} x={300} y={G + 110} bg={C.white} fg={C.ink} size={44} />
    <Pill text="Nhu cầu tập" start={f(31.54)} end={f(32.4)} x={760} y={G + 110} bg={C.pinkDeep} size={44} />
  </>
);

// Closing recap answers the hook: which line for which need.
const Closing: React.FC = () => (
  <>
    <RecapRows
      title="CHỌN DÒNG NÀO?"
      rows={[
        ["Tập cơ bản", "Thường xuyên", 34.08],
        ["Chuyên sâu", "Mastery", 37.51],
        ["Nhiều mồ hôi", "Mastery", 39.53],
      ]}
      start={32.42}
      end={42.4}
      y={G - 120}
    />
    <TopShade start={f(PICK)} end={f(42.4)} />
    <Stamp text="Chọn Mastery!" start={f(PICK)} end={f(42.4)} x={540} y={330} rot={-6} size={92} />
  </>
);

// CTA tail: dim, logo, follow line, product polaroids.
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
      <Polaroid src={PH + "cuon-tham/cuon-tham_009_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg"} label="Thảm cao su" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "tu-the/tu-the_097_tham-tap-yoga-cao-su-asana.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(2.62)} end={VIDEO_FRAMES} tag="Chọn thảm" brand="Louis Yoga" />
        <CompareScene />
        <ShowScene />
        <RegularScene />
        <MasteryScene />
        <GripScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={2.6} until={CLEAN_DURATION} />
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
