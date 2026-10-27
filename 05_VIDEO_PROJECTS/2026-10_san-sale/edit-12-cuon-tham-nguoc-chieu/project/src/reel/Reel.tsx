import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import {
  BigText,
  BottomShade,
  Impact,
  Kicker,
  Panel,
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
// LOUIS YOGA REEL — STYLE 1.  Reel "Cuộn thảm ngược chiều — vì sao thảm bị hằn và gãy"
// (series Săn sale, video 12). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same set as video 01/02 (shelf behind, foam blocks / mats on the table below).
const CAP_Y = 1030;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 12 segments (11 cuts). Mat-demo segments stay wide so the mat stays in frame.
const SEG_ZOOM = [1.24, 1.12, 1.28, 1.14, 1.1, 1.16, 1.1, 1.22, 1.12, 1.1, 1.24, 1.12];
const HOOK_DROP = 2.89;
const HOOK_END = 4.45;
const GAY = 10.7;
const DUNG = 33.87;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.7, 0.22], // hook drop "đường hằn"
  [GAY, 11.4, 0.14], // "gãy thảm luôn"
  [19.78, 20.4, 0.1], // "dính"
  [20.88, 21.6, 0.08], // "cuộn thảm đúng chiều"
  [51.33, 52.0, 0.08], // "nhìn thấy bề mặt thảm chính"
];
// Real mat in her hands: peel showing the black underside, then the rolled end (black inside).
const FOCUS: Focus[] = [
  [29.2, 31.95, 650, 820, 1.3],
  [34.45, 35.7, 626, 1300, 1.3],
];

// ▼ EDIT ▼ cutaways — Louis Yoga only (photos from louisyoga.vn + brand film), no outside clips.
// 42.77–46.67: the speaker turns away to put the mat back -> covered by two rolling photos.
const BROLL: Broll[] = [
  { start: 13.3, end: 15.35, film: 60.0, cx: 960, mode: "crop", label: "Dòng cao su bóng" },
  { start: 36.0, end: 38.1, film: 0, src: PH + "cuon-tham/cuon-tham_006_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg", mode: "photo", label: "Lúc nhận thảm cuộn thế nào" },
  { start: 42.77, end: 44.72, film: 0, src: PH + "cuon-tham/cuon-tham_007_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg", mode: "photo", label: "Mặt chính ra ngoài" },
  { start: 44.72, end: 46.67, film: 0, src: PH + "cuon-tham/cuon-tham_010_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg", mode: "photo", label: "Mặt đen cuộn vào trong" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [GAY, 7, 9, 0],
  [DUNG, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — one sound per beat (~0.6/s). Times as NUMBERS (measure_sfx skips named constants).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [2.89, "riser-metallic.mp3", 0.45],
  [2.89, "punch.mp3", 0.95], // gạch chữ + HẰN & GÃY THẢM!
  [4.6, "quick-swoosh.mp3", 0.5], // panel: cuộn ngược +
  [5.3, "pop-2.mp3", 0.5], // dẫm lên
  [7.04, "pop.mp3", 0.5], // vật nặng
  [7.7, "quick-swoosh.mp3", 0.47], // panel: ép 2 mặt
  [8.5, "pop-2.mp3", 0.45], // ép
  [10.7, "punch.mp3", 0.85], // GÃY THẢM!
  [13.3, "swoosh.mp3", 0.5], // film in
  [15.5, "quick-swoosh.mp3", 0.47], // panel: cao su bóng
  [16.8, "pop-2.mp3", 0.5], // đè lâu
  [19.78, "pop.mp3", 0.5], // dính bề mặt
  [20.88, "punch.mp3", 0.75], // slam: cuộn đúng chiều
  [21.2, "pop.mp3", 0.45], // ✕ ngược chiều
  [22.84, "quick-ting.mp3", 0.53], // ✓ đúng chiều
  [26.36, "pop-2.mp3", 0.5], // mặt chính ra ngoài
  [30.92, "pop-2.mp3", 0.5], // mặt đen vào trong
  [33.87, "punch.mp3", 0.7], // CUỘN ĐÚNG!
  [36.0, "swoosh.mp3", 0.5], // photo in
  [38.85, "quick-swoosh.mp3", 0.47], // panel: tập xong
  [40.19, "pop-2.mp3", 0.5],
  [41.97, "pop.mp3", 0.47],
  [42.77, "swoosh.mp3", 0.5], // photo in
  [44.78, "pop-2.mp3", 0.5], // ✕ mủn
  [46.88, "pop.mp3", 0.5], // ✕ gãy
  [51.33, "quick-ting.mp3", 0.5], // luôn thấy mặt chính
  [53.45, "quick-ting.mp3", 0.53],
  [54.05, "pop.mp3", 0.45],
  [54.6, "correct.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(3.8), f(4.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–4.45 s): "CUỘN THẢM / NGƯỢC CHIỀU?" slams, gets crossed out, "HẰN & GÃY THẢM!" stamp drops on "đường hằn".
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Cuộn thảm", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(HOOK_END)} y={232} slam lines={[{ text: "ngược chiều?", color: C.accent, size: 104 }]} />
    <StrikeLine d="M150,345 L930,290" start={f(HOOK_DROP)} end={f(HOOK_END)} length={800} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Hằn & gãy thảm!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 130} rot={-8} size={100} />
  </>
);

// "nhất là khi mình vô tình dẫm lên hay là để các cái vật nặng lên"
const PressScene: React.FC = () => {
  const s = f(4.6);
  const e = f(7.6);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={0} y={26} size={30} color={C.dim} spacing={4} weight={800}>
        <div style={{ width: 900, textAlign: "center" }}>Cuộn ngược + thêm</div>
      </Label>
      <Pill text="Vô tình dẫm lên" start={f(5.3)} end={e} x={450} y={100} bg={C.white} fg={C.ink} size={44} />
      <Pill text="Vật nặng đè lên" start={f(7.04)} end={e} x={450} y={186} bg={C.pinkDeep} size={44} />
    </Panel>
  );
};

// "Nó sẽ ép hai cái bề mặt lại với nhau luôn, nó sẽ gãy thảm luôn" — two mat layers squeeze together, then crack.
const SqueezeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(7.7);
  const e = f(11.3);
  const k = interpolate(frame, [f(8.5), f(9.3)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const crack = interpolate(frame, [f(GAY), f(GAY) + 6], [0, 1], clamp);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={40} y={30} size={30} color={C.dim} spacing={3} weight={800}>Ép 2 mặt</Label>
      <Label x={40} y={72} size={58} color={C.white}>dính</Label>
      <Label x={40} y={136} size={58} color={C.accent}>vào nhau</Label>
      <div style={{ position: "absolute", left: 480, top: 0, width: 400, height: 270 }}>
        {/* arrows pressing down/up */}
        <div style={{ position: "absolute", left: 180, top: 18 + 30 * k, ...font(900, 40), color: C.gold }}>▼</div>
        <div style={{ position: "absolute", left: 180, top: 208 - 30 * k, ...font(900, 40), color: C.gold }}>▲</div>
        <div style={{ position: "absolute", left: 0, top: 80 + 28 * k, width: 400, height: 36, borderRadius: 10, background: "#2E8FB5" }} />
        <div style={{ position: "absolute", left: 0, top: 156 - 12 * k, width: 400, height: 36, borderRadius: 10, background: "#26222B", border: "2px solid rgba(255,255,255,0.35)" }} />
        {crack > 0 && (
          <svg width={400} height={270} style={{ position: "absolute", left: 0, top: 0 }}>
            <path d="M200,95 L182,120 L212,140 L188,165 L205,190" stroke={C.accent} strokeWidth={9} fill="none" strokeLinecap="round" strokeDasharray={160} strokeDashoffset={160 * (1 - crack)} />
          </svg>
        )}
      </div>
      <Stamp text="Gãy thảm!" start={f(GAY)} end={e} x={640} y={196} rot={-8} size={84} />
    </Panel>
  );
};

// "đối với dòng cao su bóng, đè xuống lâu ... bị dính bề mặt thảm"
const StickScene: React.FC = () => {
  const s = f(15.45);
  const e = f(20.85);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={0} y={26} size={30} color={C.dim} spacing={4} weight={800}>
        <div style={{ width: 900, textAlign: "center" }}>Thảm cao su bóng</div>
      </Label>
      <Pill text="Đè xuống lâu" start={f(16.8)} end={e} x={450} y={100} bg={C.white} fg={C.ink} size={44} />
      <Pill text="✕ Dính bề mặt thảm" start={f(19.78)} end={e} x={450} y={186} bg={C.pinkDeep} size={44} />
    </Panel>
  );
};

// "Mọi người cuộn thảm đúng chiều giúp em nhé" — turn: ✕ ngược / ✓ đúng.
const TurnScene: React.FC = () => (
  <>
    <TopShade start={f(20.88)} end={f(23.9)} />
    <BigText
      start={f(20.88)}
      end={f(23.9)}
      y={170}
      slam
      lines={[
        { text: "Cuộn thảm", color: C.white, size: 96 },
        { text: "đúng chiều", color: C.accent, size: 112 },
      ]}
    />
    <DoDont
      title="CUỘN THẢM"
      rows={[
        ["Ngược chiều", 21.2, false],
        ["Đúng chiều nhận về", 22.84, true],
      ]}
      start={21.0}
      end={23.9}
      y={G - 10}
      size={46}
    />
  </>
);

// Real-mat demo: surface out, black side in, then "cuộn đúng" stamp on the rolled end.
const DemoScene: React.FC = () => (
  <>
    <Pill text="Mặt chính → ra ngoài" start={f(26.36)} end={f(28.35)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={48} />
    <Kicker text="Mặt đen bên dưới" start={f(28.45)} end={f(32.3)} y={300} color={C.gold} />
    <Pill text="Mặt đen → úp vào trong" start={f(30.92)} end={f(32.3)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={48} />
    <BottomShade start={f(DUNG) - 2} end={f(35.7)} />
    <Stamp text="Cuộn đúng!" start={f(DUNG)} end={f(35.7)} x={540} y={G + 130} rot={-7} size={96} />
  </>
);

// "Thì khi mà mình tập xong mình nhớ là cuộn theo đúng cái chiều thảm mà mình nhận về"
const RememberScene: React.FC = () => {
  const s = f(38.2);
  const e = f(42.7);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={0} y={26} size={30} color={C.dim} spacing={4} weight={800}>
        <div style={{ width: 900, textAlign: "center" }}>Tập xong, nhớ</div>
      </Label>
      <Pill text="Cuộn theo đúng chiều" start={f(40.19)} end={e} x={450} y={100} bg={C.white} fg={C.ink} size={44} />
      <Pill text="như lúc nhận thảm" start={f(41.97)} end={e} x={450} y={186} bg={C.pinkDeep} size={44} />
    </Panel>
  );
};

// Closing checklist answers the hook.
const Closing: React.FC = () => (
  <DoDont
    title="CUỘN THẢM ĐÚNG CÁCH"
    rows={[
      ["Mặt chính quay ra ngoài", 53.45, true],
      ["Cuộn ngược chiều", 54.05, false],
      ["Mặt đen úp vào trong", 54.6, true],
    ]}
    start={53.35}
    end={CLEAN_DURATION - 0.05}
    y={G - 70}
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
      <Polaroid src={PH + "tu-the/tu-the_160_tham-tap-yoga-cao-su-cao-cap-diamond.jpg"} label="Thảm cao su" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_111_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(HOOK_END)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <PressScene />
        <SqueezeScene />
        <StickScene />
        <TurnScene />
        <DemoScene />
        <RememberScene />
        <Pill text="✕ Mủn thảm" start={f(44.78)} end={f(46.6)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={48} />
        <Pill text="✕ Gãy bề mặt" start={f(46.88)} end={f(47.85)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={48} />
        <Pill text="✓ Luôn thấy mặt chính" start={f(51.33)} end={f(53.25)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={48} />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={HOOK_END} until={CLEAN_DURATION} />
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
