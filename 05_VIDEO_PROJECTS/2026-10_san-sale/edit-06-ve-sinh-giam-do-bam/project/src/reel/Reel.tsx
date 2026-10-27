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
import { DoDont, NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Vệ sinh thảm thường xuyên có làm giảm độ bám?"
// (series Săn sale, video 06). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same set as video 01/02 (shelf behind, foam blocks / mats on the table below).
// The source PiP (clean 25.9–40.4 s) was patched out of raw_patched.mp4 before cutting.
const CAP_Y = 1070;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 10 segments (9 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.12, 1.26, 1.1, 1.22, 1.14, 1.28, 1.12];
const HOOK_DROP = 2.38; // "không?"
const OK_GRIP = 12.31; // "không ảnh hưởng"
const SHADE = 25.06; // "bóng mát"
const FAST_DRY = 45.87; // "nhanh khô hơn"
const END_SLAM = 50.21; // "làm giảm độ bám" (không)
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.0, 0.22], // hook drop
  [OK_GRIP, 13.2, 0.12], // "không ảnh hưởng"
  [SHADE, 25.8, 0.1], // "bóng mát"
  [37.55, 38.1, 0.08], // "100ml"
  [FAST_DRY, 46.6, 0.1], // "nhanh khô"
  [END_SLAM, 51.0, 0.12], // "không làm giảm độ bám"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 17.89, end: 20.3, film: 0, src: PH + "sinh-hoat/sinh-hoat_115_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Để thoáng cho bay hơi nước" },
  { start: 36.63, end: 38.4, film: 0, src: PH + "xit-ve-sinh/xit-ve-sinh_319_xit-tham-yoga-huong-chanh-sa.jpg", mode: "photo", label: "Xịt thảm Louis Yoga · 100 ml" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.94, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [OK_GRIP, 6, 8, 0],
  [END_SLAM, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.5/s), one sound per beat. Times written as numbers (measure_sfx.py).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.94, "pop-2.mp3", 0.59],
  [2.38, "riser-metallic.mp3", 0.45],
  [2.38, "punch.mp3", 0.95],
  [3.03, "quick-swoosh.mp3", 0.5], // panel: làm sạch bề mặt
  [6.43, "pop-2.mp3", 0.5], // bụi bẩn
  [8.83, "pop.mp3", 0.47], // khi tập
  [9.4, "quick-swoosh.mp3", 0.47], // panel: đúng cách
  [12.31, "punch.mp3", 0.8], // stamp: không ảnh hưởng
  [14.43, "quick-swoosh.mp3", 0.5], // steps panel
  [15.71, "pop-2.mp3", 0.5], // ① vệ sinh xong
  [16.75, "pop.mp3", 0.5], // ② để thoáng
  [17.89, "swoosh.mp3", 0.5], // photo in
  [21.99, "quick-ting.mp3", 0.53], // ③ khô rồi mới cuộn
  [22.85, "quick-swoosh.mp3", 0.47], // DoDont phơi
  [23.4, "pop.mp3", 0.47], // ✕ nắng
  [24.32, "quick-ting.mp3", 0.53], // ✓ bóng mát
  [26.4, "quick-swoosh.mp3", 0.5], // panel: muốn sạch hơn
  [28.8, "pop-2.mp3", 0.5], // khử mùi
  [31.29, "pop.mp3", 0.47], // sạch hơn
  [32.59, "pop-2.mp3", 0.5], // an tâm
  [34.27, "quick-swoosh.mp3", 0.5], // xịt chuyên dụng card
  [36.63, "swoosh.mp3", 0.5], // photo in
  [37.55, "digital-counting-1.mp3", 0.45], // 100 ml
  [38.45, "quick-swoosh.mp3", 0.5], // panel: khăn mềm
  [39.23, "pop-2.mp3", 0.5], // ① xịt ra khăn
  [43.79, "pop.mp3", 0.5], // ② lau bề mặt
  [45.87, "punch.mp3", 0.75], // NHANH KHÔ HƠN
  [46.79, "pop-2.mp3", 0.47], // ✕ xịt trực tiếp
  [50.21, "punch.mp3", 0.8], // KHÔNG GIẢM ĐỘ BÁM
  [51.4, "quick-swoosh.mp3", 0.5], // checklist
  [51.9, "quick-ting.mp3", 0.53],
  [53.23, "quick-ting.mp3", 0.53],
  [54.17, "pop.mp3", 0.5], // ✕ sai cách
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.9), f(3.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

const Label: React.FC<{ x: number; y: number; size: number; color: string; children: React.ReactNode; spacing?: number; weight?: number }> = ({
  x,
  y,
  size,
  color,
  children,
  spacing = 0,
  weight = 900,
}) => <div style={{ position: "absolute", left: x, top: y, ...font(weight, size), color, letterSpacing: spacing }}>{children}</div>;

// Hook (0–3.0 s): "VỆ SINH THƯỜNG XUYÊN / GIẢM ĐỘ BÁM?" slams, the question is crossed out, stamp answers.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(3.0)} />
    <BigText start={0} end={f(3.0)} y={120} slam lines={[{ text: "Vệ sinh thường xuyên", color: C.white, size: 66 }]} />
    <BigText start={f(0.94)} end={f(3.0)} y={226} slam lines={[{ text: "giảm độ bám?", color: C.accent, size: 110 }]} />
    <StrikeLine d="M150,350 L930,300" start={f(HOOK_DROP)} end={f(3.0)} length={800} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(3.0)} />
    <Stamp text="Đúng cách: Không!" start={f(HOOK_DROP)} end={f(3.0)} x={540} y={G + 130} rot={-8} size={96} />
  </>
);

// "Nó sẽ làm sạch cái bề mặt thảm này, hay là các cái bụi bẩn ... trong quá trình tập luyện".
const CleanScene: React.FC = () => {
  const s = f(3.03);
  const e = f(9.3);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "be-mat/be-mat_108_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Bề mặt thảm" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Vệ sinh là</Label>
      <Label x={370} y={80} size={50} color={C.white}>làm sạch</Label>
      <Label x={370} y={140} size={50} color={C.accent}>bề mặt</Label>
      <Pill text="Bụi bẩn" start={f(6.43)} end={e} x={790} y={60} bg={C.white} fg={C.ink} size={32} />
      <Pill text="Khi tập" start={f(8.83)} end={e} x={790} y={150} bg={C.pinkDeep} size={32} />
    </Panel>
  );
};

// "Nếu vệ sinh thảm đúng cách thì nó sẽ không ảnh hưởng đến cái độ bám của thảm".
const GripScene: React.FC = () => {
  const s = f(9.4);
  const e = f(14.35);
  return (
    <>
      <Kicker text="Vệ sinh đúng cách" start={f(10.75)} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "tu-the/tu-the_211_tham-tap-yoga-cao-su-moon.jpg"} label="Vẫn bám chắc" x={30} y={25} w={300} h={220} start={s} end={e} />
        <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Độ bám</Label>
        <Label x={370} y={78} size={60} color={C.white}>của thảm</Label>
        <Stamp text="Không ảnh hưởng" start={f(OK_GRIP)} end={e} x={605} y={196} rot={-5} size={44} />
      </Panel>
    </>
  );
};

// "Sau mỗi buổi tập vệ sinh xong, là mình để thoáng ra cho nó khô" → steps; photo; "sau đó mới cuộn cất".
const AfterScene: React.FC = () => (
  <>
    <NumberRows
      title="SAU MỖI BUỔI TẬP"
      rows={[
        ["Vệ sinh xong", 15.71],
        ["Để thoáng cho khô", 16.75],
      ]}
      start={14.43}
      end={17.85}
      y={G - 40}
    />
    <Pill text="Rồi mới cuộn thảm cất đi" start={f(21.99)} end={f(22.8)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />
  </>
);

// "Không phơi trực tiếp dưới ánh nắng mặt trời. Phơi trong bóng mát".
const DryScene: React.FC = () => (
  <DoDont
    title="PHƠI THẢM SAU KHI LAU"
    rows={[
      ["Phơi nắng trực tiếp", 23.4, false],
      ["Phơi trong bóng mát", 24.32, true],
    ]}
    start={22.85}
    end={25.85}
    y={G - 10}
    size={50}
  />
);

// "Muốn xử lý mùi tốt hơn, sạch hơn, tập an tâm hơn → dùng thêm chai nước vệ sinh thảm chuyên dụng".
const SprayScene: React.FC = () => {
  const s = f(26.4);
  const e = f(34.2);
  const s2 = f(34.27);
  const e2 = f(36.6);
  return (
    <>
      <Kicker text="Muốn sạch hơn nữa?" start={s} end={e2} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <Label x={0} y={22} size={30} color={C.dim} spacing={4} weight={800}>
          <div style={{ width: 900, textAlign: "center" }}>Vệ sinh thảm để</div>
        </Label>
        <Pill text="Khử mùi tốt hơn" start={f(28.8)} end={e} x={250} y={84} bg={C.white} fg={C.ink} size={38} />
        <Pill text="Sạch hơn" start={f(31.29)} end={e} x={680} y={84} bg={C.pinkDeep} size={38} />
        <Pill text="Tập an tâm hơn" start={f(32.59)} end={e} x={450} y={170} bg={C.gold} fg={C.ink} size={40} />
      </Panel>
      <Panel start={s2} end={e2} y={G} h={270}>
        <PhotoCard src={PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg"} label="Louis Yoga" x={30} y={25} w={300} h={220} start={s2} end={e2} />
        <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Dùng thêm</Label>
        <Label x={370} y={78} size={60} color={C.white}>xịt thảm</Label>
        <Label x={370} y={146} size={60} color={C.accent}>chuyên dụng</Label>
      </Panel>
    </>
  );
};

// "Xịt ra cái khăn mềm ... lau lên bề mặt thảm" → 2 steps with the towel photo.
const TowelScene: React.FC = () => {
  const s = f(38.45);
  const e = f(45.7);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "khan/khan_065_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn mềm" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={30} size={30} color={C.dim} spacing={3} weight={800}>Cách dùng</Label>
      <Pill text="① Xịt ra khăn" start={f(39.23)} end={e} x={600} y={80} bg={C.pinkDeep} size={40} />
      <Pill text="② Lau bề mặt thảm" start={f(43.79)} end={e} x={620} y={168} bg={C.white} fg={C.ink} size={40} />
    </Panel>
  );
};

// "Thì nó sẽ nhanh khô hơn so với việc xịt trực tiếp".
const FastDryScene: React.FC = () => (
  <>
    <TopShade start={f(FAST_DRY)} end={f(48.05)} />
    <BigText
      start={f(FAST_DRY)}
      end={f(48.05)}
      y={200}
      slam
      lines={[
        { text: "Nhanh khô", color: C.white, size: 104 },
        { text: "hơn hẳn", color: C.accent, size: 110 },
      ]}
    />
    <Pill text="✕ Xịt thẳng lên thảm" start={f(46.79)} end={f(48.05)} x={W / 2} y={G + 110} bg="#3A3340" size={44} />
  </>
);

// "Nếu vệ sinh đúng cách thì nó sẽ không làm giảm độ bám của thảm đâu".
const EndSlam: React.FC = () => (
  <>
    <TopShade start={f(48.15)} end={f(51.3)} />
    <BigText start={f(48.15)} end={f(51.3)} y={140} slam lines={[{ text: "Đúng cách", color: C.white, size: 100 }]} />
    <BigText start={f(END_SLAM)} end={f(51.3)} y={260} slam lines={[{ text: "Không giảm bám", color: C.accent, size: 88 }]} />
  </>
);

// Closing checklist answers the hook.
const Closing: React.FC = () => (
  <DoDont
    title="VỆ SINH THẢM ĐÚNG CÁCH"
    rows={[
      ["Xịt ra khăn mềm, lau đều", 51.9, true],
      ["Để khô trong bóng mát", 53.23, true],
      ["Sai cách → hại thảm", 54.17, false],
    ]}
    start={51.4}
    end={CLEAN_DURATION - 0.05}
    y={G - 40}
  />
);

// CTA tail: freeze + dim, logo, follow line, product polaroids.
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
      <Polaroid src={PH + "xit-ve-sinh/xit-ve-sinh_318_xit-tham-yoga-huong-chanh-sa.jpg"} label="Xịt thảm" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "khan/khan_059_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn Louis" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(3.0)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <CleanScene />
        <GripScene />
        <AfterScene />
        <DryScene />
        <SprayScene />
        <TowelScene />
        <FastDryScene />
        <EndSlam />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={3.0} until={CLEAN_DURATION} />
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
