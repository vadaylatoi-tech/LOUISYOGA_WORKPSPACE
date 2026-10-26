import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 04 "Thảm 4,5 ly hay 5 ly?"  (data.ts by gen_data.py)
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same studio as reels 01–03
const CAP_Y = 1190;
const G = 1330;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";

// ▼ EDIT ▼ camera (6 segments)
const SEG_ZOOM = [1.24, 1.12, 1.3, 1.14, 1.26, 1.1];
const HOOK_DROP = 2.26;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.0, 0.2],
  [9.03, 9.6, 0.08],
  [23.35, 24.1, 0.14],
  [36.81, 37.4, 0.12],
  [45.25, 46.0, 0.1],
  [57.05, 57.9, 0.1],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll: Louis Yoga only — model photos from louisyoga.vn (photo) + brand film (fit)
const BROLL: Broll[] = [
  { start: 15.8, end: 17.85, film: 0, src: "louis-photos/tu-the/tu-the_138_tham-tap-yoga-cao-su-basic.jpg", mode: "photo", label: "Ra nhiều mồ hôi" },
  { start: 19.4, end: 22.2, film: 17.2, cx: 820, mode: "fit", label: "Bài tập nâng cao" },
  { start: 48.3, end: 50.9, film: 0, src: "louis-photos/tu-the/tu-the_160_tham-tap-yoga-cao-su-cao-cap-diamond.jpg", mode: "photo", label: "Ổn định · bám chắc" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.96, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [23.35, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density and families (references/02-sfx-va-am-thanh.md)
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.6],
  [0.05, "punch.mp3", 0.8],
  [0.96, "pop-2.mp3", 0.55],
  [HOOK_DROP, "riser-metallic.mp3", 0.5],
  [HOOK_DROP, "punch.mp3", 0.95],
  [5.63, "pop-2.mp3", 0.5],
  [9.03, "pop.mp3", 0.5],
  [10.67, "quick-ting.mp3", 0.5],
  [11.47, "quick-ting.mp3", 0.5],
  [15.8, "swoosh.mp3", 0.55],
  [19.4, "swoosh.mp3", 0.45],
  [23.35, "punch.mp3", 0.8],
  [24.3, "quick-swoosh.mp3", 0.5],
  [25.55, "quick-ting.mp3", 0.5],
  [27.11, "quick-ting.mp3", 0.5],
  [31.73, "correct.mp3", 0.5],
  [32.5, "quick-swoosh.mp3", 0.5],
  [33.57, "pop-2.mp3", 0.5],
  [36.81, "punch.mp3", 0.8],
  [39.69, "pop.mp3", 0.5],
  [41.5, "quick-swoosh.mp3", 0.5],
  [45.25, "digital-counting-1.mp3", 0.5],
  [48.3, "swoosh.mp3", 0.45],
  [49.11, "pop-2.mp3", 0.5],
  [50.09, "pop.mp3", 0.5],
  [53.9, "quick-swoosh.mp3", 0.5],
  [55.17, "quick-ting.mp3", 0.5],
  [57.05, "quick-ting.mp3", 0.5],
  [57.97, "correct.mp3", 0.5],
  [58.6, "quick-swoosh.mp3", 0.55],
  [58.8, "punch.mp3", 0.7],
  [59.05, "camera-shutter.mp3", 0.5],
  [59.4, "ding.mp3", 0.4],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.8), f(3.4), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Hook: question slams in two beats; "4,5 ly" panel drops with the heavy hit.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(3.3)} />
    <BigText start={0} end={f(3.3)} y={120} slam lines={[{ text: "Thảm 4,5 ly", color: C.white, size: 110 }]} />
    <BigText start={f(0.96)} end={f(3.3)} y={240} slam lines={[{ text: "hay 5 ly?", color: C.accent, size: 124 }]} />
  </>
);

// Thickness bar (grows downward under the number, never over it).
const Bar: React.FC<{ h: number; color: string; w?: number }> = ({ h, color, w = 300 }) => (
  <div style={{ width: w, height: h, borderRadius: 8, background: color, marginTop: 14 }} />
);

// 4,5 ly = Asana · Moon → bài nhẹ nhàng, ít mồ hôi.
const ThinScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(HOOK_DROP);
  const e = f(13.9);
  const p = spring({ frame: frame - s, fps: FPS, config: { damping: 10, stiffness: 180 } });
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <MatCard src="img/asana.jpg" label="Asana" x={36} y={26} w={120} h={250} at={HOOK_DROP} active={frame >= f(10.67) && frame < f(11.47)} />
        <MatCard src="img/moon.jpg" label="Moon" x={186} y={26} w={120} h={250} at={HOOK_DROP + 0.1} active={frame >= f(11.47)} />
        <div style={{ position: "absolute", left: 360, top: 22, transform: `scale(${interpolate(p, [0, 1], [1.8, 1])})`, transformOrigin: "left top", opacity: Math.min(1, p * 2) }}>
          <span style={{ ...font(900, 104), color: C.accent }}>4,5</span>
          <span style={{ ...font(900, 50), color: C.white, marginLeft: 10 }}>ly</span>
          <Bar h={18} color={`linear-gradient(180deg, ${C.accent}, ${C.pinkDeep})`} />
        </div>
      </Panel>
      <Pill text="✓ Bài nhẹ nhàng" start={f(5.63)} end={e} x={640} y={G + 140} size={36} />
      <Pill text="✓ Ít mồ hôi" start={f(9.03)} end={e} x={640} y={G + 225} bg={C.white} fg={C.ink} size={36} />
    </>
  );
};

// 5 ly: thấm hút, bám chắc, thoải mái.
const ThickTitle: React.FC = () => (
  <>
    <BottomShade start={f(23.0)} end={f(24.3)} />
    <BigText start={f(23.35)} end={f(24.3)} y={G + 70} slam lines={[{ text: "Dòng 5 ly", color: C.accent, size: 120 }]} />
  </>
);

// Basic = chuẩn 5 ly, cơ bản → nâng cao.
const BasicScene: React.FC = () => {
  const s = f(32.5);
  const e = f(41.4);
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <MatCard src="louis-photos/do-day/do-day_074_tham-tap-yoga-cao-su-asana-25.jpg" label="Đo thực tế" x={30} y={22} w={270} h={270} at={33.57} active />
        <div style={{ position: "absolute", left: 340, top: 30 }}>
          <div style={{ ...font(800, 28), color: C.dim, letterSpacing: 3 }}>Độ dày</div>
          <span style={{ ...font(900, 104), color: C.white }}>5</span>
          <span style={{ ...font(900, 50), color: C.white, marginLeft: 10 }}>ly</span>
          <Bar h={30} color="linear-gradient(180deg, #F4C25B, #D9A33A)" w={360} />
        </div>
        <Pill text="Cơ bản → nâng cao" start={f(39.69)} end={e} x={620} y={262} bg={C.white} fg={C.ink} size={34} />
      </Panel>
      <Stamp text="Chuẩn 5 ly" start={f(36.81)} end={f(39.6)} x={650} y={G + 170} rot={-7} size={74} />
    </>
  );
};

// 5–6 buổi / tuần: week dots fill up.
const WeekScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(41.5);
  const e = f(48.3);
  const filled = Math.round(interpolate(frame, [f(45.25), f(45.25) + 14], [0, 6], clamp));
  const days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
  return (
    <Panel start={s} end={e} y={G - 20} h={300}>
      <div style={{ position: "absolute", top: 20, left: 0, right: 0, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>Tập thường xuyên</div>
      <div style={{ position: "absolute", top: 70, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 18 }}>
        {days.map((d, i) => (
          <div key={d} style={{ width: 96, height: 96, borderRadius: 18, display: "flex", alignItems: "center", justifyContent: "center", ...font(900, 30),
            background: i < filled ? (i < 5 ? C.pinkDeep : "rgba(226,49,139,0.55)") : "rgba(255,255,255,0.1)", color: C.white }}>{d}</div>
        ))}
      </div>
      {frame >= f(45.25) && (
        <div style={{ position: "absolute", top: 196, left: 0, right: 0, textAlign: "center" }}>
          <span style={{ ...font(900, 64), color: C.gold }}>5–6 buổi</span>
          <span style={{ ...font(900, 40), color: C.white, marginLeft: 12 }}>/ tuần</span>
        </div>
      )}
    </Panel>
  );
};

// Stability pills after the B-roll.
const StablePills: React.FC = () => (
  <>
    <Pill text="Ổn định" start={f(49.11)} end={f(53.85)} x={360} y={G + 150} size={46} />
    <Pill text="Bám chắc" start={f(50.09)} end={f(53.85)} x={720} y={G + 150} bg={C.gold} fg={C.ink} size={46} />
  </>
);

// Conclusion: the 5 ly line — Basic, Asana 25, Queen.
const Pick5 = () => {
  const s = f(53.9);
  const e = VIDEO_FRAMES - 3;
  return (
    <Panel start={s} end={e} y={G - 40} h={370}>
      <div style={{ position: "absolute", top: 14, left: 0, right: 0, textAlign: "center", ...font(900, 32), color: C.accent, letterSpacing: 2 }}>Tập thường xuyên · 5 ly</div>
      <MatCard src="img/basic.jpg" label="Basic" x={110} y={64} w={120} h={250} at={55.17} active />
      <MatCard src="img/asana25.jpg" label="Asana 25" x={390} y={64} w={120} h={250} at={57.05} active />
      <MatCard src="img/queen.jpg" label="Queen" x={670} y={64} w={120} h={250} at={57.97} active />
    </Panel>
  );
};

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
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 8} end={DURATION + 1} x={70} y={G - 60} w={200} h={300} rot={-7} />
      <Polaroid src="img/basic.jpg" label="Basic" start={s + 12} end={DURATION + 1} x={740} y={G - 50} w={200} h={300} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 60, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 34), color: C.white }}>Nhẹ nhàng</div>
        <div style={{ ...font(900, 44), color: C.accent }}>4,5 ly</div>
        <div style={{ ...font(900, 34), color: C.white, marginTop: 12 }}>Thường xuyên</div>
        <div style={{ ...font(900, 44), color: C.gold }}>5 ly</div>
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
        <SeriesTag start={f(3.3)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <ThinScene />
        <ThickTitle />
        <CheckGrid items={[["Thấm hút", 25.55], ["Bám chắc", 27.11], ["Thoải mái", 31.73]]} start={f(24.3)} end={f(32.4)} y={G} />
        <BasicScene />
        <WeekScene />
        <StablePills />
        <Pick5 />
        <Captions lines={CAPTIONS} y={CAP_Y} from={3.3} until={CLEAN_DURATION} />
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
