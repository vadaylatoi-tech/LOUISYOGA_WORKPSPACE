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
import { DoDont } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Thảm mới dùng đã mủn — do chất lượng hay do cách dùng"
// (series Săn sale, video 07). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands. Two set-ups in the source:
//   clean 0–44.33   standing (same set as video 01/02)  → CAP_Y 1030, G 1390
//   clean 44.33–end seated, face lower                    → CAP_Y2 / G2
const CAP_Y = 1030;
const G = 1390;
const SEATED = 44.333;
const CAP_Y2 = 1190;
const G2 = 1420;
// The livestream re-framed the camera at clean 63.0 (source shrank + PiP): raw_patched crops it back,
// so add a cut there to hide the jump with a zoom change.
const REFRAME = 63.0;
const CUTS_ALL = [...CUTS, REFRAME];

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 11 segments (10 cuts incl. REFRAME), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.26, 1.12, 1.28, 1.12, 1.22, 1.1, 1.24, 1.12, 1.1];
const HOOK_DROP = 2.53;
const WRONG = 33.52;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.3, 0.22], // hook drop "kém thế"
  [5.27, 6.0, 0.12], // "mủn"
  [11.49, 12.4, 0.08], // "vệ sinh và bảo quản"
  [14.27, 15.0, 0.1], // "độ bền"
  [29.88, 30.6, 0.1], // "nhanh hỏng"
  [WRONG, 34.1, 0.14], // "chưa đúng"
  [45.55, 46.3, 0.08], // "không phải"
  [64.04, 64.8, 0.08], // "độ bền"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga only. 52.8–56.5 also hides the source PiP sliding across the table/body.
const BROLL: Broll[] = [
  { start: 19.2, end: 21.05, film: 50.6, cx: 620, mode: "crop", label: "Thời tiết, độ ẩm" },
  { start: 52.8, end: 54.75, film: 0, src: PH + "cuon-tham/cuon-tham_268_tham-tap-yoga-cao-su-xo-dua-aura.jpg", mode: "photo", label: "Lau cồn → kém bền" },
  { start: 54.75, end: 56.5, film: 0, src: PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg", mode: "photo", label: "Vệ sinh đúng cách" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [WRONG, 7, 9, 0],
  [57.76, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.55/s), one sound per beat. Times as NUMBERS (measure_sfx/build_stems).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [2.53, "riser-metallic.mp3", 0.45],
  [2.53, "punch.mp3", 0.95],
  [3.65, "quick-swoosh.mp3", 0.5], // panel: mới dùng
  [5.27, "pop-2.mp3", 0.5], // ✕ xuống cấp
  [7.05, "quick-swoosh.mp3", 0.47], // panel: ngoài chất lượng
  [11.49, "pop.mp3", 0.5], // cách vệ sinh
  [12.03, "pop-2.mp3", 0.5], // bảo quản
  [13.6, "quick-swoosh.mp3", 0.5], // panel: độ bền phụ thuộc
  [15.75, "pop-2.mp3", 0.5], // ① chất lượng
  [19.2, "swoosh.mp3", 0.5], // b-roll in
  [20.57, "pop.mp3", 0.47], // ② thời tiết
  [21.99, "pop-2.mp3", 0.5], // ③ vệ sinh + bảo quản
  [24.35, "quick-swoosh.mp3", 0.5], // panel: khách hỏi
  [26.1, "quick-ting.mp3", 0.5], // ✓ rất kỹ
  [29.88, "pop.mp3", 0.5], // vẫn nhanh hỏng?
  [31.92, "pop-2.mp3", 0.5], // title line 1
  [WRONG, "punch.mp3", 0.8], // CHƯA ĐÚNG!
  [34.65, "quick-swoosh.mp3", 0.45], // kicker: tùy loại thảm
  [38.05, "pop-2.mp3", 0.5], // TPE
  [38.95, "pop.mp3", 0.5], // cao su
  [40.89, "pop-2.mp3", 0.5], // vải
  [41.71, "quick-ting.mp3", 0.45], // mỗi loại một cách
  [44.45, "quick-swoosh.mp3", 0.5], // panel: độ bền ≠ thời gian
  [45.55, "pop.mp3", 0.47], // ✕ không cố định
  [47.47, "pop-2.mp3", 0.5], // tùy cách vệ sinh
  [52.8, "swoosh.mp3", 0.5], // photo in
  [54.75, "quick-ting.mp3", 0.5], // ✓ vệ sinh đúng cách
  [57.76, "punch.mp3", 0.75], // slam: thảm bền lâu
  [58.5, "pop-2.mp3", 0.5], // line 2
  [60.84, "quick-swoosh.mp3", 0.5], // checklist
  [61.44, "quick-ting.mp3", 0.53],
  [61.92, "quick-ting.mp3", 0.53],
  [64.04, "correct.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(3.2), f(3.8), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

const Center: React.FC<{ y: number; size: number; color: string; children: React.ReactNode; spacing?: number; weight?: number }> = ({ y, size, color, children, spacing = 0, weight = 900 }) => (
  <div style={{ position: "absolute", left: 0, width: 900, top: y, textAlign: "center", ...font(weight, size), color, letterSpacing: spacing }}>{children}</div>
);

// Hook (0–3.6 s): "THẢM MỚI DÙNG / ĐÃ MỦN = KÉM?" slams, "= kém?" gets crossed out, "CHƯA CHẮC!" stamp drops.
const HOOK_END = 3.6;
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Thảm mới dùng", color: C.white, size: 100 }]} />
    <BigText start={f(0.55)} end={f(HOOK_END)} y={232} slam lines={[{ text: "đã mủn = kém?", color: C.accent, size: 96 }]} />
    <StrikeLine d="M110,345 L970,295" start={f(HOOK_DROP)} end={f(HOOK_END)} length={870} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Chưa chắc!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 130} rot={-8} size={112} />
  </>
);

// "mình mới dùng mà nó đã bị mủn rồi"
const NewMatScene: React.FC = () => {
  const s = f(3.65);
  const e = f(6.95);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "cuon-tham/cuon-tham_261_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Thảm mới" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Mới dùng</Label>
      <Label x={370} y={82} size={66} color={C.white}>đã mủn</Label>
      <Label x={370} y={150} size={66} color={C.accent}>rồi?</Label>
      <Pill text="✕ Xuống cấp" start={f(5.27)} end={e} x={730} y={175} bg={C.gold} fg={C.ink} size={38} />
    </Panel>
  );
};

// "ngoài chất lượng … quan tâm cách vệ sinh và bảo quản thảm"
const BeyondScene: React.FC = () => {
  const s = f(7.05);
  const e = f(12.95);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Center y={28} size={30} color={C.dim} spacing={4} weight={800}>Ngoài chất lượng</Center>
      <Center y={72} size={52} color={C.white}>còn phải để ý</Center>
      <Pill text="Cách vệ sinh" start={f(11.49)} end={e} x={250} y={190} bg={C.pinkDeep} size={42} />
      <Pill text="Bảo quản" start={f(12.03)} end={e} x={670} y={190} bg={C.gold} fg={C.ink} size={42} />
    </Panel>
  );
};

// "độ bền của thảm: ngoài chất lượng … thời tiết … cách vệ sinh và bảo quản hằng ngày"
const DurabilityScene: React.FC = () => {
  const s = f(13.6);
  const e = f(24.2);
  return (
    <>
      <Kicker text="Độ bền thảm" start={s} end={f(19.15)} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <Center y={24} size={30} color={C.dim} spacing={4} weight={800}>Phụ thuộc vào</Center>
        <Pill text="① Chất lượng" start={f(15.75)} end={e} x={240} y={105} bg={C.white} fg={C.ink} size={40} />
        <Pill text="② Thời tiết" start={f(20.57)} end={e} x={665} y={105} bg={C.gold} fg={C.ink} size={40} />
        <Pill text="③ Vệ sinh + bảo quản" start={f(21.99)} end={e} x={450} y={200} bg={C.pinkDeep} size={40} />
      </Panel>
    </>
  );
};

// "có những chị bảo vệ sinh rất kỹ … mà vẫn nhanh hỏng"
const AskScene: React.FC = () => {
  const s = f(24.35);
  const e = f(30.7);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "xit-ve-sinh/xit-ve-sinh_026_combo-tham-yoga-basic-khan-da-nang-va-xi.jpg"} label="Vệ sinh" x={30} y={25} w={260} h={220} start={s} end={e} />
      <Label x={330} y={36} size={30} color={C.dim} spacing={3} weight={800}>Khách hỏi</Label>
      <Label x={330} y={78} size={46} color={C.white}>Đã vệ sinh</Label>
      <Pill text="✓ Rất kỹ" start={f(26.1)} end={e} x={765} y={104} bg={C.gold} fg={C.ink} size={34} />
      <Pill text="Vẫn nhanh hỏng?" start={f(29.88)} end={e} x={600} y={198} bg={C.pinkDeep} size={42} />
    </Panel>
  );
};

// "cách vệ sinh thảm của mình nó cũng chưa đúng"
const WrongScene: React.FC = () => (
  <>
    <TopShade start={f(31.92)} end={f(34.55)} />
    <BigText start={f(31.92)} end={f(34.55)} y={200} slam lines={[{ text: "Cách vệ sinh", color: C.white, size: 96 }]} />
    <BigText start={f(WRONG)} end={f(34.55)} y={312} slam lines={[{ text: "chưa đúng!", color: C.accent, size: 112 }]} />
  </>
);

// "tùy tính chất từng loại thảm: TPE, cao su, thảm vải … cách vệ sinh khác nhau"
const TypesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(37.93);
  const e = f(44.3);
  const vai = f(40.89);
  const pv = interpolate(frame, [vai, vai + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  return (
    <>
      <TopShade start={f(34.65)} end={e} />
      <Kicker text="Tùy từng loại thảm" start={f(34.65)} end={f(41.6)} y={300} color={C.gold} />
      <Kicker text="Mỗi loại — một cách vệ sinh" start={f(41.71)} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        {frame >= f(38.05) && <PhotoCard src={PH + "tu-the/tu-the_293_tham-tap-yoga-tpe-dinh-tuyen-tpe9.jpg"} label="TPE" x={25} y={25} w={270} h={220} start={f(38.05)} end={e} />}
        {frame >= f(38.95) && <PhotoCard src="brand/rubber_rolls.jpg" label="Cao su" x={315} y={25} w={270} h={220} start={f(38.95)} end={e} highlight />}
        {frame >= vai && (
          <div
            style={{
              position: "absolute",
              left: 605,
              top: 25,
              width: 270,
              height: 220,
              borderRadius: 18,
              border: "3px solid rgba(255,255,255,0.85)",
              background: "linear-gradient(135deg, rgba(255,90,174,0.25), rgba(244,194,91,0.18))",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              transform: `scale(${0.6 + 0.4 * pv})`,
              opacity: pv,
            }}
          >
            <div style={{ ...font(800, 28), color: C.dim, letterSpacing: 3 }}>THẢM</div>
            <div style={{ ...font(900, 64), color: C.white }}>Vải</div>
          </div>
        )}
      </Panel>
    </>
  );
};

// Seated: "độ bền không phải một thời gian cụ thể — tùy cách vệ sinh và bảo quản"
const NoFixedScene: React.FC = () => {
  const s = f(44.45);
  const e = f(50.2);
  return (
    <Panel start={s} end={e} y={G2} h={270}>
      <Center y={24} size={30} color={C.dim} spacing={4} weight={800}>Độ bền thảm</Center>
      <Pill text="✕ Không cố định" start={f(45.55)} end={e} x={450} y={105} bg={C.white} fg={C.ink} size={42} />
      <Pill text="Tùy cách vệ sinh + bảo quản" start={f(47.47)} end={e} x={450} y={200} bg={C.pinkDeep} size={38} />
    </Panel>
  );
};

// "nên là mọi người lưu ý thêm …" — conclusion slams, then the checklist answers the hook.
const AdviceScene: React.FC = () => (
  <>
    <TopShade start={f(57.76)} end={f(60.8)} />
    <BigText start={f(57.76)} end={f(60.8)} y={200} slam lines={[{ text: "Thảm bền lâu", color: C.white, size: 100 }]} />
    <BigText start={f(58.5)} end={f(60.8)} y={312} slam lines={[{ text: "nhờ dùng đúng!", color: C.accent, size: 100 }]} />
  </>
);

const Closing: React.FC = () => (
  <DoDont
    title="ĐỂ THẢM BỀN LÂU"
    rows={[
      ["Vệ sinh đúng loại thảm", 61.44, true],
      ["Bảo quản cẩn thận", 61.92, true],
      ["Bền hơn, tập thoải mái", 64.04, true],
    ]}
    start={60.84}
    end={CLEAN_DURATION - 0.05}
    y={1320}
  />
);

// CTA tail: freeze + dim, logo, follow line, Louis photos.
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
      <Polaroid src={PH + "xit-ve-sinh/xit-ve-sinh_323_xit-tham-yoga-huong-chanh-sa.jpg"} label="Xịt thảm" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "tu-the/tu-the_243_tham-tap-yoga-cao-su-queen.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <TalkingHead src={FOOTAGE} videoFrames={VIDEO_FRAMES} duration={DURATION} cuts={CUTS_ALL} face={FACE} segZoom={SEG_ZOOM} punches={PUNCHES} focus={FOCUS} muted={STEM !== "all"} />
        <BrollLayer items={BROLL} src={FILM} />
        <Hook />
        <SeriesTag start={f(HOOK_END)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <NewMatScene />
        <BeyondScene />
        <DurabilityScene />
        <AskScene />
        <WrongScene />
        <TypesScene />
        <NoFixedScene />
        <AdviceScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={HOOK_END} until={SEATED} />
        <Captions lines={CAPTIONS} y={CAP_Y2} from={SEATED} until={CLEAN_DURATION} />
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
