import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard, RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 07 "Asana, Moon, Sunflower khác nhau chỗ nào?"
// Louis-only visuals: product avatars, louisyoga.vn photos (bags, Sunflower rolls), brand film.
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

// ▼ EDIT ▼ camera (10 segments)
const SEG_ZOOM = [1.22, 1.12, 1.28, 1.14, 1.26, 1.1, 1.3, 1.16, 1.24, 1.12];
const HOOK_DROP = 2.22;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.0, 0.18],
  [7.59, 8.3, 0.12],
  [14.65, 15.4, 0.1],
  [33.49, 34.3, 0.1],
  [39.99, 40.6, 0.08],
  [51.54, 52.2, 0.1],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll — Louis Yoga only
const BROLL: Broll[] = [
  { start: 23.3, end: 25.6, film: 0, src: PH + "sinh-hoat/sinh-hoat_258_tham-tap-yoga-cao-su-sunflower-2.jpg", mode: "photo", label: "Thảm Sunflower" },
  { start: 29.1, end: 30.95, film: 42.3, cx: 1150, mode: "crop", label: "Bám tay · thấm hút" },
  { start: 44.5, end: 46.6, film: 0, src: PH + "sinh-hoat/sinh-hoat_302_tui-da-nang-cao-cap-m2261.jpg", mode: "photo", label: "Mang thảm đi tập" },
];

const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.4, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [7.59, 6, 8, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.4, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [3.57, "pop.mp3", 0.5],
  [4.31, "pop-2.mp3", 0.5],
  [7.59, "punch.mp3", 0.75],
  [9.87, "quick-swoosh.mp3", 0.5],
  [11.27, "pop-2.mp3", 0.5],
  [14.65, "punch.mp3", 0.7],
  [17.67, "pop.mp3", 0.5],
  [19.8, "quick-swoosh.mp3", 0.5],
  [23.3, "swoosh.mp3", 0.5],
  [27.53, "quick-ting.mp3", 0.5],
  [29.1, "swoosh.mp3", 0.4],
  [28.43, "quick-ting.mp3", 0.5],
  [31.5, "quick-swoosh.mp3", 0.5],
  [33.49, "pop-2.mp3", 0.5],
  [36.19, "pop.mp3", 0.5],
  [38.6, "quick-swoosh.mp3", 0.5],
  [39.99, "quick-ting.mp3", 0.5],
  [44.5, "swoosh.mp3", 0.5],
  [46.8, "quick-swoosh.mp3", 0.5],
  [48.76, "pop-2.mp3", 0.5],
  [51.54, "quick-ting.mp3", 0.5],
  [53.9, "correct.mp3", 0.5],
  [56.95, "quick-swoosh.mp3", 0.55],
  [57.2, "punch.mp3", 0.7],
  [57.45, "camera-shutter.mp3", 0.5],
  [57.8, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.8), f(3.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Hook: names + question, then the three real mats pop in as they are named; stamp on "tương đương".
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(5.4)} />
    <BigText start={0} end={f(5.4)} y={120} slam lines={[{ text: "Asana · Moon · Sunflower", color: C.white, size: 56 }]} />
    <BigText start={f(0.4)} end={f(5.4)} y={200} slam lines={[{ text: "khác nhau chỗ nào?", color: C.accent, size: 74 }]} />
    <Panel start={f(HOOK_DROP)} end={f(9.8)} y={G - 40} h={370}>
      <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(800, 28), color: C.dim, letterSpacing: 3 }}>Cùng kích thước · chất liệu</div>
      <MatCard src="img/sunflower.jpg" label="Sunflower" x={110} y={64} w={120} h={240} at={HOOK_DROP} active />
      <MatCard src="img/asana.jpg" label="Asana" x={390} y={64} w={120} h={240} at={3.57} active />
      <MatCard src="img/moon.jpg" label="Moon" x={670} y={64} w={120} h={240} at={4.31} active />
    </Panel>
    <Stamp text="Chất lượng như nhau" start={f(7.59)} end={f(9.8)} x={540} y={G + 150} rot={-6} size={64} />
  </>
);

// Moon vs Asana: chỉ khác hoạ tiết.
const Pattern: React.FC = () => {
  const s = f(9.87);
  const e = f(19.7);
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <MatCard src="img/moon.jpg" label="Moon" x={120} y={22} w={130} h={270} at={9.87} active />
        <MatCard src="img/asana.jpg" label="Asana" x={650} y={22} w={130} h={270} at={10.0} />
        <div style={{ position: "absolute", left: 300, width: 300, top: 120, textAlign: "center", ...font(900, 44), color: C.gold }}>VS</div>
        <Pill text="Hoạ tiết nhỏ gọn" start={f(11.27)} end={e} x={250} y={60} size={26} />
      </Panel>
      <Stamp text="Chỉ khác hoạ tiết" start={f(14.65)} end={f(17.5)} x={540} y={G + 150} rot={-6} size={66} />
      <Pill text="Chọn mẫu đang ưu đãi" start={f(17.67)} end={e} x={W / 2} y={G + 200} bg={C.gold} fg={C.ink} size={40} />
    </>
  );
};

// Sunflower: dòng cơ bản, bám + thấm hút, tặng dây đeo, trợ giá.
const Sunflower: React.FC = () => {
  const s = f(19.8);
  const e = f(38.5);
  return (
    <>
      <Panel start={s} end={f(23.3)} y={G - 40} h={370}>
        <MatCard src="img/sunflower.jpg" label="Sunflower" x={60} y={22} w={130} h={270} at={19.8} active />
        <div style={{ position: "absolute", left: 250, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Dòng thảm cơ bản</div>
        <div style={{ position: "absolute", left: 250, top: 90, ...font(900, 64), color: C.white }}>Sunflower</div>
      </Panel>
      <BottomShade start={f(25.6)} end={f(29.1)} />
      <Pill text="✓ Độ bám" start={f(27.53)} end={f(29.1)} x={360} y={G + 140} size={46} />
      <Pill text="✓ Thấm hút" start={f(28.43)} end={f(29.1)} x={720} y={G + 140} bg={C.gold} fg={C.ink} size={46} />
      <Panel start={f(31.5)} end={e} y={G - 20} h={300}>
        <MatCard src="img/sunflower.jpg" x={50} y={22} w={120} h={250} at={31.5} active />
        <div style={{ position: "absolute", left: 220, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Đang tặng kèm</div>
        <div style={{ position: "absolute", left: 220, top: 84, ...font(900, 60), color: C.gold, opacity: useCurrentFrame() >= f(33.49) ? 1 : 0 }}>Dây đeo thảm</div>
        <Pill text="Trợ giá sâu hơn" start={f(36.19)} end={e} x={470} y={190} size={38} />
      </Panel>
    </>
  );
};

// Asana · Moon tặng túi đựng.
const BagScene: React.FC = () => {
  const s = f(46.8);
  const e = f(53.85);
  return (
    <Panel start={s} end={e} y={G - 40} h={370}>
      <MatCard src="img/asana.jpg" label="Asana" x={40} y={22} w={110} h={250} at={48.76} active />
      <MatCard src="img/moon.jpg" label="Moon" x={175} y={22} w={110} h={250} at={49.76} active />
      <div style={{ position: "absolute", left: 300, top: 120, ...font(900, 50), color: C.gold }}>+</div>
      <MatCard src={PH + "tui-dung-tham/tui-dung-tham_304_tui-da-nang-cao-cap-m2261.jpg"} label="Tặng túi đựng" x={360} y={22} w={480} h={250} at={51.54} active />
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
      <Kicker text="xem thêm mẹo chọn thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src="img/sunflower.jpg" label="Sunflower" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Cùng</div>
        <div style={{ ...font(900, 44), color: C.accent }}>chất lượng</div>
        <div style={{ ...font(900, 32), color: C.gold, marginTop: 8 }}>khác quà tặng</div>
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
        <SeriesTag start={f(5.4)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <Pattern />
        <Sunflower />
        <RecapRows title="Chọn mẫu nào?" rows={[["Ưu tiên giá", "Sunflower", 39.99]]} start={38.6} end={43.8} y={G - 20} />
        <BagScene />
        <RecapRows title="Chọn mẫu nào?" rows={[["Ưu tiên giá", "Sunflower", 53.9], ["Mang đi tập", "Asana · Moon", 53.95]]} start={53.9} end={(VIDEO_FRAMES - 3) / FPS} y={G - 20} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={5.4} until={CLEAN_DURATION} />
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
