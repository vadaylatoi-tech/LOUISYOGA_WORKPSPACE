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
import { DoDont, MatCard, NumberRows, RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Asana hay Asana 25 — chọn mẫu nào"
// (series Săn sale, video 11). Built on the approved v4 template / video 02; only ▼ EDIT ▼ differs.
// On set: GREEN mat (multi-colour mandala, left) = Asana 25 — she touches it on "đây là Asana 25";
//         BLACK mat (gold one-colour print, right) = Asana — she touches it on "còn đây là Asana 4 ly rưỡi".
// Specs only as spoken: Asana 4,5 ly in 1 màu; Asana 25 5 ly in đa màu; both have alignment lines. No prices.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — standing set like 01/02/10 (shelf behind, two mats hanging, blocks on the table).
const CAP_Y = 1060;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";
const IMG_A25 = PH + "be-mat/be-mat_077_tham-tap-yoga-cao-su-asana-25.jpg";
const IMG_A = "brand/mat_asana_black.jpg";

// ▼ EDIT ▼ camera: 15 segments (14 cuts), alternate tight/wide.
const SEG_ZOOM = [1.22, 1.1, 1.26, 1.12, 1.28, 1.12, 1.24, 1.1, 1.26, 1.14, 1.28, 1.12, 1.24, 1.1, 1.22];
const HOOK_DROP = 1.67; // "5 LY"
const A25 = 21.55; // "nó là Asana 25"
const LEN5 = 43.29; // "lên cái dòng 5 ly"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.5, 0.22], // hook drop
  [A25, 22.2, 0.12], // "Asana 25"
  [36.05, 36.8, 0.08], // "bám tay"
  [LEN5, 43.95, 0.12], // "dòng 5 ly"
  [59.1, 59.9, 0.12], // "Asana 25 nhé"
];
// [start, end, x, y, zoom] — slide onto the real mats she touches.
const FOCUS: Focus[] = [
  [2.9, 3.68, 300, 900, 1.28], // green = Asana 25 ("in đa màu")
  [3.69, 7.45, 700, 880, 1.28], // black = Asana ("4 ly rưỡi, in 1 màu")
  [19.0, 24.45, 330, 880, 1.24], // "còn bên này, phiên bản nâng cấp … Asana 25"
  [24.5, 27.3, 380, 1000, 1.2], // she folds the green mat corner on "độ dày chuẩn 5 ly"
  [44.06, 48.4, 320, 780, 1.26], // printed mandala: "không phai, không dính quần áo"
];

// ▼ EDIT ▼ cutaways — Louis Yoga photos + brand film only, no outside clips.
const BROLL: Broll[] = [
  { start: 9.1, end: 11.0, film: 0, src: PH + "tu-the/tu-the_097_tham-tap-yoga-cao-su-asana.jpg", mode: "photo", label: "Người mới · tập ở nhà" },
  { start: 29.2, end: 31.2, film: 19.9, cx: 760, mode: "fit", label: "Bài tập nâng cao" },
  { start: 39.29, end: 41.0, film: 0, src: PH + "tu-the/tu-the_196_tham-tap-yoga-cao-su-cao-cap-lilium.jpg", mode: "photo", label: "Chó úp mặt" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [A25, 6, 8, 0],
  [LEN5, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density, one sound per beat. Times as NUMBERS (measure_sfx skips names).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [1.67, "riser-metallic.mp3", 0.45],
  [1.67, "punch.mp3", 0.95],
  [2.9, "quick-swoosh.mp3", 0.5], // compare panel: Asana 25
  [3.13, "pop-2.mp3", 0.5], // in đa màu
  [3.69, "quick-swoosh.mp3", 0.45], // Asana column
  [5.37, "pop.mp3", 0.5], // 4,5 ly
  [6.67, "pop-2.mp3", 0.5], // in 1 màu
  [9.1, "swoosh.mp3", 0.5], // photo in
  [11.05, "pop-2.mp3", 0.5], // pill: người mới
  [14.4, "quick-swoosh.mp3", 0.5], // Asana checklist
  [14.85, "quick-ting.mp3", 0.5], // ✓ bám tay
  [15.79, "quick-ting.mp3", 0.5], // ✓ thấm hút
  [17.39, "correct.mp3", 0.5], // ✓ không trơn
  [19.8, "pop.mp3", 0.5], // kicker: nâng cấp
  [21.55, "punch.mp3", 0.8], // ASANA 25 stamp
  [23.83, "pop-2.mp3", 0.5], // ra mắt cuối 2025
  [24.5, "quick-swoosh.mp3", 0.5], // panel độ dày
  [25.9, "digital-counting-1.mp3", 0.45], // 4,5 → 5
  [29.2, "swoosh.mp3", 0.5], // film in
  [31.23, "quick-swoosh.mp3", 0.5], // rows: dòng 5 ly
  [33.83, "pop-2.mp3", 0.5], // êm hơn
  [34.47, "pop.mp3", 0.5], // thấm hút
  [36.05, "pop-2.mp3", 0.5], // bám tay
  [39.29, "swoosh.mp3", 0.5], // photo in
  [40.55, "pop.mp3", 0.5], // trơn tay?
  [43.29, "punch.mp3", 0.8], // LÊN DÒNG 5 LY
  [44.06, "quick-swoosh.mp3", 0.45], // hoạ tiết in
  [46.48, "quick-ting.mp3", 0.5], // ✓ không phai
  [47.58, "quick-ting.mp3", 0.5], // ✓ không dính
  [48.43, "quick-swoosh.mp3", 0.5], // recap
  [49.94, "quick-ting.mp3", 0.53], // ✓ cơ bản
  [54.7, "quick-ting.mp3", 0.53], // ✓ êm + bám
  [62.73, "correct.mp3", 0.53], // ✓ định tuyến
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.4), f(3.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–2.9 s): "ASANA 25 / KHÁC MỖI TÊN?" slams, gets crossed out on "5 ly", stamp "DÀY 5 LY!".
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(2.9)} />
    <BigText start={0} end={f(2.9)} y={120} slam lines={[{ text: "Asana 25", color: C.white, size: 112 }]} />
    <BigText start={f(0.55)} end={f(2.9)} y={240} slam lines={[{ text: "khác mỗi tên?", color: C.accent, size: 100 }]} />
    <StrikeLine d="M130,350 L950,300" start={f(HOOK_DROP)} end={f(2.9)} length={840} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.85)} />
    <Stamp text="Dày 5 ly!" start={f(HOOK_DROP)} end={f(2.85)} x={540} y={G + 130} rot={-8} size={120} />
  </>
);

// Side-by-side with REAL product images while the camera slides over the real mats (2.9–7.45).
const CompareScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(2.9);
  const e = f(7.45);
  const right = f(3.69);
  const vs = interpolate(frame, [right, right + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  return (
    <Panel start={s} end={e} y={G - 40} h={300}>
      <MatCard src={IMG_A25} x={24} y={22} w={150} h={256} at={2.9} active={frame < right} />
      <Label x={190} y={30} size={44} color={C.gold}>ASANA 25</Label>
      <Pill text="5 ly" start={s} end={e} x={290} y={110} bg={C.white} fg={C.ink} size={34} />
      <Pill text="In đa màu" start={f(3.13)} end={e} x={300} y={192} bg={C.pinkDeep} size={34} />
      <div style={{ position: "absolute", left: 449, top: 30, width: 2, height: 240, background: "rgba(255,255,255,0.25)" }} />
      {frame >= right && (
        <>
          <div style={{ position: "absolute", left: 412, top: 112, width: 76, height: 76, borderRadius: 99, background: C.gold, color: C.ink, display: "flex", alignItems: "center", justifyContent: "center", ...font(900, 32), transform: `scale(${vs})` }}>VS</div>
          <MatCard src={IMG_A} x={726} y={22} w={150} h={256} at={3.69} active />
          <Label x={480} y={30} size={44} color={C.white}>ASANA</Label>
          <Pill text="4,5 ly" start={f(5.37)} end={e} x={590} y={110} bg={C.white} fg={C.ink} size={34} />
          <Pill text="In 1 màu" start={f(6.67)} end={e} x={590} y={192} bg="#3A3340" size={34} />
        </>
      )}
    </Panel>
  );
};

// "Asana thường … người mới tập / cơ bản ở nhà … bám tay, thấm hút mồ hôi, không trơn, không xê dịch".
const AsanaScene: React.FC = () => (
  <>
    <Kicker text="ASANA THƯỜNG · 4,5 LY" start={f(7.55)} end={f(9.05)} y={300} color={C.gold} />
    <Pill text="Người mới · tập cơ bản" start={f(11.05)} end={f(14.3)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={44} />
    <DoDont
      title="ASANA 4,5 LY"
      rows={[
        ["Bám tay tốt", 14.85, true],
        ["Thấm hút mồ hôi", 15.79, true],
        ["Không trơn, không xê dịch", 17.39, true],
      ]}
      start={14.4}
      end={18.95}
      y={G - 70}
      size={40}
    />
  </>
);

// "Còn bên này, phiên bản nâng cấp hơn của Asana, nó là Asana 25 … ra mắt cuối năm 2025".
const UpgradeScene: React.FC = () => (
  <>
    <Kicker text="PHIÊN BẢN NÂNG CẤP" start={f(19.8)} end={f(24.45)} y={300} color={C.gold} />
    <BottomShade start={f(A25) - 2} end={f(23.8)} />
    <Stamp text="Asana 25" start={f(A25)} end={f(23.8)} x={540} y={G + 110} rot={-6} size={110} />
    <Pill text="Ra mắt cuối 2025" start={f(23.83)} end={f(24.45)} x={W / 2} y={G + 110} bg={C.white} fg={C.ink} size={44} />
  </>
);

// "Thì cái dòng này nó sẽ là độ dày chuẩn 5 ly" — caliper photo + counter 4,5 → 5 LY.
const ThickScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(24.5);
  const e = f(27.3);
  const v = interpolate(frame, [f(25.9), f(26.9)], [4.5, 5], { ...clamp, easing: Easing.out(Easing.cubic) });
  const done = frame >= f(26.9);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "do-day/do-day_074_tham-tap-yoga-cao-su-asana-25.jpg"} label="Asana 25" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Độ dày chuẩn</Label>
      <Label x={370} y={80} size={120} color={done ? C.accent : C.white}>
        {v.toFixed(1).replace(".", ",").replace(",0", "")}
        <span style={{ fontSize: 64, marginLeft: 16 }}>LY</span>
      </Label>
    </Panel>
  );
};

// "Asana 25 đáp ứng tốt cả bài tập nâng cao … bởi vì dòng 5 ly: êm hơn, thấm hút tốt hơn, bám tay chắc hơn".
const AdvancedScene: React.FC = () => (
  <>
    <Kicker text="ASANA 25 · 5 LY" start={f(27.33)} end={f(29.15)} y={300} color={C.gold} />
    <Pill text="✓ Cả bài nâng cao" start={f(27.97)} end={f(29.15)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
    <NumberRows
      title="DÒNG 5 LY"
      rows={[
        ["Êm hơn", 33.83],
        ["Thấm hút tốt hơn", 34.47],
        ["Bám tay chắc hơn", 36.05],
      ]}
      start={31.23}
      end={37.25}
      y={G - 120}
    />
  </>
);

// "Đặc biệt khi tập chó úp mặt mà hay bị trơn tay → tham khảo đầu tư lên dòng 5 ly".
const SlipScene: React.FC = () => (
  <>
    <Kicker text="ĐẶC BIỆT KHI TẬP" start={f(37.33)} end={f(39.25)} y={300} color={C.gold} />
    <Pill text="Hay bị trơn tay?" start={f(40.55)} end={f(43.25)} x={W / 2} y={G + 110} bg={C.white} fg={C.ink} size={46} />
    <TopShade start={f(LEN5)} end={f(44.0)} />
    <BigText
      start={f(LEN5)}
      end={f(44.0)}
      y={235}
      slam
      lines={[
        { text: "Lên dòng", color: C.white, size: 96 },
        { text: "5 ly", color: C.accent, size: 128 },
      ]}
    />
  </>
);

// "Hoạ tiết in như thế này không bị phai, không dính ra quần áo".
const PrintScene: React.FC = () => (
  <>
    <Kicker text="HOẠ TIẾT IN" start={f(44.06)} end={f(48.4)} y={300} color={C.gold} />
    <Pill text="✓ Không phai" start={f(46.48)} end={f(48.4)} x={300} y={G + 110} bg={C.pinkDeep} size={42} />
    <Pill text="✓ Không dính quần áo" start={f(47.58)} end={f(48.4)} x={620} y={G + 200} bg={C.gold} fg={C.ink} size={42} />
  </>
);

// Closing recap answers the hook: which model for which need.
const Closing: React.FC = () => (
  <RecapRows
    title="CHỌN MẪU NÀO?"
    rows={[
      ["Tập cơ bản", "Asana 4,5 ly", 49.94],
      ["Êm, bám hơn", "Asana 25", 54.7],
      ["Cả 2 mẫu", "Có định tuyến", 62.73],
    ]}
    start={48.43}
    end={CLEAN_DURATION - 0.05}
    y={G - 120}
  />
);

// CTA tail: dim, logo, follow line, product polaroids (Asana 25 + Asana).
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
      <Polaroid src={PH + "be-mat/be-mat_075_tham-tap-yoga-cao-su-asana-25.jpg"} label="Asana 25" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "tu-the/tu-the_091_tham-tap-yoga-cao-su-asana.jpg"} label="Asana" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(2.9)} end={VIDEO_FRAMES} tag="Chọn thảm" brand="Louis Yoga" />
        <CompareScene />
        <AsanaScene />
        <UpgradeScene />
        <ThickScene />
        <AdvancedScene />
        <SlipScene />
        <PrintScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={2.85} until={CLEAN_DURATION} />
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
