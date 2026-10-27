import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
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
  TopShade,
  useImpact,
} from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { DoDont, MatCard } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Ưu tiên độ êm hay độ bám - chọn thảm nào"
// (series Săn sale, video 09). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// Product comparison: TPE 9 ly / cao su 5 ly / Lilium 6,5 ly — only the numbers the speaker says.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — she sits low (chin ≈ 1020 unzoomed), foam blocks + rolled mats on the table below.
const CAP_Y = 1200;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 11 segments (10 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.2, 1.12, 1.28, 1.12, 1.26, 1.1, 1.22, 1.12, 1.26];
const HOOK_DROP = 2.9; // "(cả độ) bám (nữa)"
const HOOK_END = 3.43;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.43, 0.22],
  [8.36, 9.0, 0.1], // "9 ly"
  [33.01, 33.6, 0.08], // "cao hơn"
  [39.55, 40.3, 0.12], // "6 ly rưỡi"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — louisyoga.vn photos only, no outside clips.
const BROLL: Broll[] = [
  { start: 27.95, end: 29.65, film: 0, src: PH + "do-day/do-day_074_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "Chuẩn 5 ly" },
  { start: 37.66, end: 39.12, film: 0, src: PH + "tu-the/tu-the_195_tham-tap-yoga-cao-su-cao-cap-lilium.jpg", mode: "photo", label: "Thảm Lilium" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [1.8, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [8.36, 6, 8, 0],
  [39.55, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.6/s), one sound per beat. Times written as numbers (measure_sfx.py).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [1.8, "pop-2.mp3", 0.59], // "hay độ bám?"
  [2.9, "riser-metallic.mp3", 0.45],
  [2.9, "punch.mp3", 0.95], // stamp CHỌN THẢM NÀO?
  [3.5, "quick-swoosh.mp3", 0.47], // kicker: nếu ưu tiên độ êm
  [5.66, "quick-swoosh.mp3", 0.47], // panel: thảm TPE
  [6.16, "pop-2.mp3", 0.5], // "TPE"
  [8.36, "punch.mp3", 0.8], // DÀY 9 LY
  [9.6, "quick-swoosh.mp3", 0.47], // checklist TPE
  [9.97, "quick-ting.mp3", 0.53], // ✓ êm, nhẹ
  [13.7, "quick-ting.mp3", 0.53], // ✓ giá thành thấp hơn
  [17.2, "pop.mp3", 0.5], // ✕ độ bám hạn chế hơn
  [20.92, "quick-swoosh.mp3", 0.5], // slam: vừa êm
  [23.02, "pop-2.mp3", 0.5], // vừa bám tốt
  [24.75, "quick-swoosh.mp3", 0.47], // panel: thảm cao su
  [27.95, "swoosh.mp3", 0.5], // photo in: thước kẹp 5 mm
  [29.05, "punch.mp3", 0.75], // CHUẨN 5 LY
  [32.21, "quick-swoosh.mp3", 0.47], // slam: mức đầu tư
  [33.01, "pop-2.mp3", 0.53], // cao hơn
  [35.0, "pop-2.mp3", 0.5], // độ êm
  [36.14, "pop.mp3", 0.47], // độ bám
  [36.72, "quick-ting.mp3", 0.5], // chất lượng
  [37.66, "swoosh.mp3", 0.5], // photo in: Lilium
  [39.55, "punch.mp3", 0.8], // 6,5 LY
  [41.6, "quick-ting.mp3", 0.53], // recap rows
  [42.4, "quick-ting.mp3", 0.53],
  [43.2, "correct.mp3", 0.45],
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

// Hook (0–3.43 s): "ƯU TIÊN ĐỘ ÊM / HAY ĐỘ BÁM?" slams twice → stamp "CHỌN THẢM NÀO?" + riser/punch/shake.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Ưu tiên độ êm", color: C.white, size: 98 }]} />
    <BigText start={f(1.8)} end={f(HOOK_END)} y={238} slam lines={[{ text: "hay độ bám?", color: C.accent, size: 112 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Chọn thảm nào?" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 130} rot={-7} size={84} />
  </>
);

// "Mình đang ưu tiên hơn về độ êm thì bên em sẽ có cái thảm TPE xốp. Cái dạng thảm đấy thì nó sẽ dày 9 ly."
const TpeScene: React.FC = () => {
  const s = f(5.66);
  const e = f(9.55);
  return (
    <>
      <Kicker text="Nếu ưu tiên độ êm" start={f(3.5)} end={f(5.6)} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "tu-the/tu-the_291_tham-tap-yoga-tpe-dinh-tuyen-tpe9.jpg"} label="Thảm TPE" x={30} y={25} w={300} h={220} start={s} end={e} />
        <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Bên em có · dạng xốp</Label>
        <Label x={370} y={78} size={68} color={C.white}>Thảm TPE</Label>
        <Stamp text="Dày 9 ly" start={f(8.36)} end={e} x={560} y={198} rot={-5} size={58} />
      </Panel>
    </>
  );
};

// "Thì nó sẽ rất là êm. Ưu điểm … êm, nhẹ và giá thành thấp hơn. Tuy nhiên độ bám tay … hạn chế hơn so với cao su."
const TpeProsCons: React.FC = () => (
  <>
    <DoDont
      title="THẢM TPE 9 LY"
      rows={[
        ["Êm, nhẹ", 9.97, true],
        ["Giá thành thấp hơn", 13.7, true],
        ["Độ bám hạn chế hơn", 17.2, false],
      ]}
      start={9.6}
      end={19.0}
      y={1316}
    />
    <Kicker text="So với thảm cao su" start={f(18.04)} end={f(19.0)} y={300} color={C.gold} />
  </>
);

// "Còn nếu mà mình đang muốn nó êm và nó có cái độ bám tốt…"
const BothScene: React.FC = () => (
  <>
    <TopShade start={f(20.92)} end={f(24.6)} />
    <BigText start={f(20.92)} end={f(24.6)} y={170} slam lines={[{ text: "Vừa êm", color: C.white, size: 100 }]} />
    <BigText start={f(23.02)} end={f(24.6)} y={290} slam lines={[{ text: "vừa bám tốt", color: C.accent, size: 104 }]} />
  </>
);

// "…thì chị có thể tham khảo các cái mẫu dòng cao su, thì nó sẽ là độ dày…" → real product avatars.
const RubberScene: React.FC = () => {
  const s = f(24.7);
  const e = f(27.9);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <MatCard src="img/basic.jpg" x={40} y={18} w={110} h={232} at={24.83} />
      <MatCard src="img/queen.jpg" x={168} y={18} w={110} h={232} at={25.03} />
      <Label x={320} y={36} size={30} color={C.dim} spacing={3} weight={800}>Các mẫu dòng</Label>
      <Label x={320} y={78} size={62} color={C.white}>Thảm cao su</Label>
      <Label x={322} y={162} size={40} color={C.accent}>Êm + bám tốt</Label>
    </Panel>
  );
};

// "…độ dày nó là 5 ly, chuẩn 5 ly thì nó sẽ êm hơn" — caliper photo, then stamp.
const FiveScene: React.FC = () => (
  <>
    <BottomShade start={f(29.05) - 2} end={f(30.6)} />
    <Stamp text="Chuẩn 5 ly" start={f(29.05)} end={f(30.6)} x={540} y={G + 130} rot={-6} size={100} />
  </>
);

// "Ngoài ra nếu mà mình có cái mức đầu tư nó cao hơn, tức là chị ưu tiên hơn hẳn về độ êm, độ bám, chất lượng vượt trội…"
const InvestScene: React.FC = () => {
  const s = f(34.11);
  const e = f(37.6);
  return (
    <>
      <TopShade start={f(32.21)} end={f(34.6)} />
      <BigText start={f(32.21)} end={f(34.6)} y={170} slam lines={[{ text: "Mức đầu tư", color: C.white, size: 98 }]} />
      <BigText start={f(33.01)} end={f(34.6)} y={290} slam lines={[{ text: "cao hơn", color: C.accent, size: 112 }]} />
      <Panel start={s} end={e} y={G} h={270}>
        <Label x={0} y={30} size={32} color={C.dim} spacing={4} weight={800}>
          <div style={{ width: 900, textAlign: "center" }}>Ưu tiên hơn hẳn</div>
        </Label>
        <Pill text="Độ êm" start={f(35.0)} end={e} x={140} y={150} bg={C.white} fg={C.ink} size={42} />
        <Pill text="Độ bám" start={f(36.14)} end={e} x={400} y={150} bg={C.pinkDeep} size={42} />
        <Pill text="Chất lượng" start={f(36.72)} end={e} x={705} y={150} bg={C.gold} fg={C.ink} size={42} />
      </Panel>
    </>
  );
};

// "…tham khảo cái mẫu thảm Lilium 6 ly rưỡi của cái dòng thảm cao su".
const LiliumScene: React.FC = () => {
  const s = f(39.15);
  const e = f(41.4);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <MatCard src="img/lilium.jpg" x={40} y={18} w={110} h={232} at={39.17} active />
      <Label x={190} y={36} size={30} color={C.dim} spacing={3} weight={800}>Mẫu thảm</Label>
      <Label x={190} y={76} size={78} color={C.white}>Lilium</Label>
      <Label x={192} y={170} size={36} color={C.accent}>dòng cao su</Label>
      <Stamp text="6,5 ly" start={f(39.55)} end={e} x={720} y={140} rot={-6} size={84} />
    </Panel>
  );
};

// Closing recap answers the hook (compact rows so the panel stays above the post description).
const RecapRow: React.FC<{ need: string; pick: string; at: number; i: number }> = ({ need, pick, at, i }) => {
  const frame = useCurrentFrame();
  if (frame < f(at)) return null;
  const p = spring({ frame: frame - f(at), fps: FPS, config: { damping: 12, stiffness: 180 } });
  return (
    <div style={{ position: "absolute", left: 36, top: 74 + i * 78, display: "flex", alignItems: "center", transform: `scale(${0.7 + 0.3 * p})`, transformOrigin: "left center", opacity: Math.min(1, p * 2) }}>
      <div style={{ width: 58, height: 58, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 32), boxShadow: "0 0 18px rgba(255,90,174,0.5)" }}>✓</div>
      <div style={{ marginLeft: 16, width: 330, ...font(900, 38), color: C.white }}>{need}</div>
      <div style={{ ...font(900, 38), color: C.dim }}>→</div>
      <div style={{ marginLeft: 14, ...font(900, 40), color: C.gold }}>{pick}</div>
    </div>
  );
};

const Closing: React.FC = () => (
  <Panel start={f(41.45)} end={f(CLEAN_DURATION - 0.05)} y={1320} h={322}>
    <div style={{ position: "absolute", top: 16, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.accent, letterSpacing: 2 }}>CHỌN THẢM THEO NHU CẦU</div>
    <RecapRow need="Êm, giá thấp" pick="TPE 9 ly" at={41.6} i={0} />
    <RecapRow need="Êm + bám tốt" pick="Cao su 5 ly" at={42.4} i={1} />
    <RecapRow need="Đầu tư cao" pick="Lilium 6,5 ly" at={43.2} i={2} />
  </Panel>
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
      <Kicker text="xem thêm mẹo chọn thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src={PH + "tu-the/tu-the_293_tham-tap-yoga-tpe-dinh-tuyen-tpe9.jpg"} label="Thảm TPE" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "tu-the/tu-the_137_tham-tap-yoga-cao-su-basic.jpg"} label="Thảm cao su" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(HOOK_END)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <TpeScene />
        <TpeProsCons />
        <BothScene />
        <RubberScene />
        <FiveScene />
        <InvestScene />
        <LiliumScene />
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
