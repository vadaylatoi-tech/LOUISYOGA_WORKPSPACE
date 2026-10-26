import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 08 "Hoạ tiết khắc laser hay in đa màu?"  (dòng 5 ly)
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

// ▼ EDIT ▼ camera (8 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16];
const HOOK_DROP = 1.22;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.0, 0.18],
  [8.47, 9.2, 0.12],
  [23.99, 24.6, 0.08],
  [40.48, 41.2, 0.1],
  [63.23, 63.9, 0.08],
  [70.83, 71.6, 0.1],
  [74.37, 75.2, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 15.3, end: 17.6, film: 0, src: PH + "be-mat/be-mat_108_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Hoạ tiết khắc laser" },
  { start: 25.5, end: 28.0, film: 0, src: PH + "tu-the/tu-the_136_tham-tap-yoga-cao-su-basic.jpg", mode: "photo", label: "Mới tập hay tập lâu" },
  { start: 34.3, end: 36.9, film: 58.2, cx: 1000, mode: "fit", label: "Đặt tay · đặt chân" },
  { start: 46.6, end: 49.2, film: 0, src: PH + "sinh-hoat/sinh-hoat_115_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Thiền định" },
  { start: 66.2, end: 68.6, film: 0, src: PH + "be-mat/be-mat_076_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "In đa màu nổi bật" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [8.47, 6, 8, 0],
  [74.37, 6, 8, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [2.74, "pop.mp3", 0.45],
  [5.11, "pop-2.mp3", 0.45],
  [8.47, "punch.mp3", 0.75],
  [9.8, "quick-swoosh.mp3", 0.5],
  [10.25, "pop-2.mp3", 0.5],
  [11.37, "pop.mp3", 0.5],
  [15.3, "swoosh.mp3", 0.5],
  [19.0, "quick-swoosh.mp3", 0.5],
  [21.15, "quick-ting.mp3", 0.5],
  [23.99, "quick-ting.mp3", 0.5],
  [25.5, "swoosh.mp3", 0.45],
  [32.05, "pop-2.mp3", 0.5],
  [34.3, "swoosh.mp3", 0.45],
  [37.4, "quick-swoosh.mp3", 0.5],
  [40.48, "pop-2.mp3", 0.5],
  [43.45, "pop.mp3", 0.5],
  [46.6, "swoosh.mp3", 0.45],
  [52.91, "quick-swoosh.mp3", 0.5],
  [57.17, "quick-ting.mp3", 0.5],
  [58.15, "quick-ting.mp3", 0.5],
  [63.23, "correct.mp3", 0.5],
  [66.2, "swoosh.mp3", 0.45],
  [70.83, "correct.mp3", 0.5],
  [74.37, "punch.mp3", 0.75],
  [78.56, "pop-2.mp3", 0.5],
  [80.95, "quick-swoosh.mp3", 0.55],
  [81.2, "punch.mp3", 0.7],
  [81.45, "camera-shutter.mp3", 0.5],
  [81.8, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(1.9), f(2.5), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const FOUR = [
  ["img/basic.jpg", "Basic", 2.74],
  ["img/basiczen.jpg", "Basic Zen", 3.57],
  ["img/asana25.jpg", "Asana 25", 5.11],
  ["img/queen.jpg", "Queen", 5.87],
] as const;

const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(9.7)} />
    <BigText start={0} end={f(9.7)} y={120} slam lines={[{ text: "Khắc laser", color: C.white, size: 104 }]} />
    <BigText start={f(0.4)} end={f(9.7)} y={232} slam lines={[{ text: "hay in đa màu?", color: C.accent, size: 96 }]} />
    <Panel start={f(HOOK_DROP)} end={f(9.7)} y={G - 40} h={370}>
      <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.gold, letterSpacing: 2 }}>Dòng 5 ly · 4 mẫu</div>
      {FOUR.map(([src, label, at], i) => (
        <MatCard key={label} src={src} label={label} x={52 + i * 208} y={64} w={118} h={240} at={Math.min(at, HOOK_DROP + i * 0.1)} active={useCurrentFrame() >= f(at)} labelSize={22} />
      ))}
    </Panel>
    <Stamp text="Chỉ khác thiết kế" start={f(8.47)} end={f(9.7)} x={540} y={G + 150} rot={-6} size={70} />
  </>
);

// Two groups: khắc laser (Basic, Basic Zen) vs in đa màu (Asana 25, Queen).
const Groups: React.FC<{ s: number; e: number; laserAt: number; printAt: number; hiLaser?: number; hiPrint?: number; title?: string; laserLabel?: string; printLabel?: string }> = ({
  s,
  e,
  laserAt,
  printAt,
  hiLaser = 999,
  hiPrint = 999,
  title,
  laserLabel = "Khắc laser",
  printLabel = "In đa màu",
}) => {
  const frame = useCurrentFrame();
  const box = (x: number, label: string, at: number, hi: number, items: readonly (readonly [string, string])[], color: string) =>
    frame >= f(at) && (
      <div style={{ position: "absolute", left: x, top: 0, width: 440, height: 370 }}>
        <div style={{ position: "absolute", top: title ? 52 : 18, left: 0, right: 0, textAlign: "center", ...font(900, 34), color: frame >= f(hi) ? color : C.white }}>{label}</div>
        {items.map(([src, l], i) => (
          <MatCard key={l} src={src} label={l} x={70 + i * 170} y={title ? 100 : 70} w={110} h={title ? 200 : 230} at={at + i * 0.1} active={frame >= f(hi)} labelSize={22} />
        ))}
      </div>
    );
  return (
    <Panel start={f(s)} end={f(e)} y={G - 40} h={370}>
      {title && <div style={{ position: "absolute", top: 12, left: 0, right: 0, textAlign: "center", ...font(900, 30), color: C.dim, letterSpacing: 2 }}>{title}</div>}
      {box(10, laserLabel, laserAt, hiLaser, [["img/basic.jpg", "Basic"], ["img/basiczen.jpg", "Basic Zen"]], C.accent)}
      <div style={{ position: "absolute", left: 425, top: 160, width: 50, textAlign: "center", ...font(900, 36), color: C.gold }}>VS</div>
      {box(450, printLabel, printAt, hiPrint, [["img/asana25.jpg", "Asana 25"], ["img/queen.jpg", "Queen"]], C.gold)}
    </Panel>
  );
};

// Basic: đơn giản, đủ định tuyến.
const BasicScene: React.FC = () => (
  <>
    <Panel start={f(19.0)} end={f(25.4)} y={G - 40} h={370}>
      <MatCard src="img/basic.jpg" label="Basic" x={50} y={22} w={130} h={270} at={19.0} active />
      <div style={{ position: "absolute", left: 230, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Khắc laser</div>
      <div style={{ position: "absolute", left: 230, top: 84, ...font(900, 64), color: C.white }}>Basic</div>
      <Pill text="✓ Đơn giản, dễ dùng" start={f(21.15)} end={f(25.4)} x={500} y={190} size={32} />
      <Pill text="✓ Đủ đường định tuyến" start={f(23.99)} end={f(25.4)} x={500} y={262} bg={C.gold} fg={C.ink} size={32} />
    </Panel>
    <BottomShade start={f(28.0)} end={f(34.3)} />
    <Pill text="Dễ tập bài mới" start={f(32.05)} end={f(34.3)} x={W / 2} y={G + 160} size={46} />
  </>
);

// Basic Zen: độc đáo, quay video / chụp ảnh, thiền định.
const ZenScene: React.FC = () => (
  <Panel start={f(37.4)} end={f(46.6)} y={G - 40} h={370}>
    <MatCard src="img/basiczen.jpg" label="Basic Zen" x={50} y={22} w={130} h={270} at={37.4} active />
    <div style={{ position: "absolute", left: 230, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Khắc laser</div>
    <div style={{ position: "absolute", left: 230, top: 84, ...font(900, 64), color: C.white }}>Basic Zen</div>
    <Pill text="✓ Độc đáo hơn" start={f(40.48)} end={f(46.6)} x={480} y={190} size={32} />
    <Pill text="✓ Quay video · chụp ảnh" start={f(43.45)} end={f(46.6)} x={520} y={262} bg={C.gold} fg={C.ink} size={30} />
  </Panel>
);

const NeedScene: React.FC = () => (
  <>
    <BottomShade start={f(52.9)} end={f(61.4)} />
    <Kicker text="chỉ cần thảm đảm bảo" start={f(53.4)} end={f(61.4)} y={G + 20} color={C.white} />
    <Pill text="✓ Thấm hút" start={f(57.17)} end={f(61.4)} x={340} y={G + 110} size={46} />
    <Pill text="✓ Bám tay · bám sàn" start={f(58.15)} end={f(61.4)} x={W / 2} y={G + 210} bg={C.gold} fg={C.ink} size={44} />
  </>
);

const Closing: React.FC = () => (
  <>
    <Stamp text="Cùng kích thước · chất liệu" start={f(74.37)} end={f(78.4)} x={540} y={G + 150} rot={-5} size={52} />
    <BottomShade start={f(78.4)} end={VIDEO_FRAMES - 2} />
    <BigText start={f(78.56)} end={VIDEO_FRAMES - 2} y={G + 90} slam lines={[{ text: "Tuỳ nhu cầu", color: C.accent, size: 92 }, { text: "& sở thích", color: C.white, size: 72 }]} />
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
      <Polaroid src="img/basic.jpg" label="Khắc laser" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/asana25.jpg" label="In đa màu" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Dòng 5 ly</div>
        <div style={{ ...font(900, 44), color: C.accent, marginTop: 8 }}>4 mẫu</div>
        <div style={{ ...font(900, 30), color: C.gold, marginTop: 8 }}>cùng chất lượng</div>
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
        <SeriesTag start={f(9.7)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <Groups s={9.8} e={15.3} laserAt={10.25} printAt={11.37} hiLaser={14.47} />
        <BasicScene />
        <ZenScene />
        <NeedScene />
        <Groups s={61.5} e={74.2} laserAt={61.6} printAt={61.7} hiLaser={63.23} hiPrint={70.83} title="Chọn theo nhu cầu" laserLabel="Đơn giản" printLabel="Nổi bật" />
        <Closing />
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
