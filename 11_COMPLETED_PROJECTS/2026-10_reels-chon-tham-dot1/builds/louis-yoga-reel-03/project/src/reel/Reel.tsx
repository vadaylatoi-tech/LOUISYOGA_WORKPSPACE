import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, CheckGrid, Impact, Kicker, Panel, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { MatCard, RecapRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Video 03 "Người mới nên chọn thảm TPE hay cao su?"
// TPE facts from louisyoga.vn (Thảm TPE Định Tuyến – TPE9: 9 mm, 1,4 kg). data.ts by gen_data.py.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same studio as reels 01–02 (face centre y≈900, towels from y≈1340)
const CAP_Y = 1190;
const G = 1330;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";

// ▼ EDIT ▼ camera (11 segments)
const SEG_ZOOM = [1.22, 1.1, 1.28, 1.14, 1.26, 1.12, 1.3, 1.16, 1.24, 1.12, 1.28];
const HOOK_DROP = 1.94;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.8, 0.2],
  [5.91, 6.5, 0.1],
  [25.09, 25.9, 0.08],
  [38.44, 39.0, 0.1],
  [42.84, 43.5, 0.08],
  [56.23, 56.9, 0.1],
  [62.09, 63.0, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ B-roll: Louis Yoga only — model photos from louisyoga.vn (photo) + brand film (fit)
const BROLL: Broll[] = [
  { start: 11.2, end: 13.8, film: 0, src: "louis-photos/tu-the/tu-the_158_tham-tap-yoga-cao-su-cao-cap-diamond.jpg", mode: "photo", label: "Mới làm quen yoga" },
  { start: 15.0, end: 18.4, film: 0, src: "louis-photos/sinh-hoat/sinh-hoat_112_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Tập thể dục tại nhà" },
  { start: 31.3, end: 34.6, film: 63.3, cx: 900, mode: "fit", label: "Tập lâu dài" },
  { start: 44.2, end: 46.9, film: 0, src: "louis-photos/tu-the/tu-the_211_tham-tap-yoga-cao-su-moon.jpg", mode: "photo", label: "Giữ tư thế lâu" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.86, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [38.44, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density and families (references/02-sfx-va-am-thanh.md)
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.82],
  [0.86, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.53],
  [HOOK_DROP, "punch.mp3", 0.96],
  [3.66, "quick-swoosh.mp3", 0.53],
  [5.91, "digital-counting-1.mp3", 0.53],
  [8.91, "pop-2.mp3", 0.53],
  [9.25, "pop.mp3", 0.47],
  [10.35, "pop-2.mp3", 0.53],
  [11.2, "swoosh.mp3", 0.59],
  [15.0, "swoosh.mp3", 0.47],
  [20.4, "quick-swoosh.mp3", 0.53],
  [21.61, "pop.mp3", 0.53],
  [25.09, "quick-ting.mp3", 0.53],
  [27.0, "quick-swoosh.mp3", 0.47],
  [31.3, "swoosh.mp3", 0.53],
  [35.1, "quick-swoosh.mp3", 0.53],
  [38.44, "punch.mp3", 0.78],
  [41.22, "quick-ting.mp3", 0.53],
  [42.84, "quick-ting.mp3", 0.53],
  [44.2, "swoosh.mp3", 0.47],
  [46.74, "quick-ting.mp3", 0.53],
  [48.64, "correct.mp3", 0.53],
  [50.9, "quick-swoosh.mp3", 0.53],
  [52.95, "quick-ting.mp3", 0.53],
  [56.23, "pop-2.mp3", 0.53],
  [58.55, "quick-ting.mp3", 0.53],
  [62.09, "correct.mp3", 0.53],
  [63.5, "quick-swoosh.mp3", 0.59],
  [63.7, "punch.mp3", 0.72],
  [63.95, "camera-shutter.mp3", 0.53],
  [64.3, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.6), f(3.2), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Hook: question slams in two beats, then the real TPE vs rubber photos drop with the heavy hit.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(3.6)} />
    <BigText start={0} end={f(3.6)} y={120} slam lines={[{ text: "Mới tập yoga", color: C.white, size: 96 }]} />
    <BigText start={f(0.86)} end={f(3.6)} y={222} slam lines={[{ text: "TPE hay cao su?", color: C.accent, size: 104 }]} />
    <Panel start={f(HOOK_DROP)} end={f(3.6)} y={G - 40} h={370}>
      <MatCard src="img/tpe_pink.jpg" label="TPE" x={70} y={20} w={290} h={290} at={HOOK_DROP} />
      <MatCard src="img/asana.jpg" label="Cao su" x={680} y={20} w={140} h={290} at={HOOK_DROP} />
    </Panel>
    <Stamp text="VS" start={f(HOOK_DROP)} end={f(3.6)} x={540} y={G + 140} rot={-6} size={110} />
  </>
);

// "Thảm TPE này — dày 9 ly — êm, nhẹ, độ bền cao".
const TpeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(3.66);
  const e = f(10.85);
  const n = Math.min(9, Math.max(1, Math.round(interpolate(frame, [f(5.91), f(6.35)], [1, 9], clamp))));
  return (
    <Panel start={s} end={e} y={G - 40} h={370}>
      <MatCard src="img/tpe_pink.jpg" x={30} y={30} w={300} h={300} at={3.66} />
      <div style={{ position: "absolute", left: 370, top: 26 }}>
        <div style={{ ...font(800, 28), color: C.dim, letterSpacing: 3 }}>Thảm TPE · Louis Yoga</div>
        {frame >= f(5.91) && (
          <div style={{ marginTop: 6 }}>
            <span style={{ ...font(900, 96), color: C.accent }}>{n}</span>
            <span style={{ ...font(900, 46), color: C.white, marginLeft: 10 }}>ly</span>
          </div>
        )}
      </div>
      <Pill text="Êm" start={f(8.91)} end={e} x={440} y={238} size={34} />
      <Pill text="Nhẹ 1,4 kg" start={f(9.25)} end={e} x={630} y={238} bg={C.white} fg={C.ink} size={34} />
      <Pill text="Độ bền cao" start={f(10.35)} end={e} x={560} y={300 - 4} bg={C.gold} fg={C.ink} size={30} />
    </Panel>
  );
};

// "Setup phòng tập — mức đầu tư khá phù hợp": several real TPE colours.
const StudioScene: React.FC = () => {
  const s = f(20.4);
  const e = f(26.5);
  const mats = ["tpe_green", "tpe_orange", "tpe_blue", "tpe_navy"];
  return (
    <>
      <Panel start={s} end={e} y={G - 40} h={370}>
        <div style={{ position: "absolute", top: 18, left: 0, right: 0, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>Setup phòng tập</div>
        {mats.map((m, i) => (
          <MatCard key={m} src={`img/${m}.jpg`} x={40 + i * 210} y={76} w={190} h={190} at={21.61 + i * 0.12} />
        ))}
      </Panel>
      <Pill text="✓ Mức đầu tư hợp lý" start={f(25.09)} end={e} x={W / 2} y={G + 252} bg={C.gold} fg={C.ink} size={40} />
    </>
  );
};

// "Tập lâu dài / cải thiện sức khoẻ → dòng cao su".
const LongTerm: React.FC = () => (
  <>
    <BottomShade start={f(26.6)} end={f(31.3)} />
    <Kicker text="xác định tập lâu dài?" start={f(27.0)} end={f(31.3)} y={G + 40} color={C.white} />
    <BottomShade start={f(35.1)} end={f(38.8)} />
    <Kicker text="cải thiện sức khoẻ thì chọn" start={f(35.1)} end={f(38.8)} y={G + 10} color={C.white} />
  </>
);

// Rubber line: Asana + Moon slam in on "cao su".
const RubberScene: React.FC = () => (
  <>
    <BigText start={f(38.44)} end={f(40.85)} y={G + 70} slam lines={[{ text: "Thảm cao su", color: C.accent, size: 104 }]} />
  </>
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
      <Polaroid src="img/tpe_pink.jpg" label="TPE 9 ly" start={s + 8} end={DURATION + 1} x={60} y={G - 40} w={240} h={240} rot={-7} />
      <Polaroid src="img/asana.jpg" label="Asana" start={s + 12} end={DURATION + 1} x={750} y={G - 60} w={190} h={290} rot={6} />
      <div style={{ position: "absolute", left: 330, right: 330, top: G + 80, textAlign: "center", opacity: interpolate(frame, [s + 14, s + 22], [0, 1], clamp) }}>
        <div style={{ ...font(900, 40), color: C.white }}>Chọn theo</div>
        <div style={{ ...font(900, 46), color: C.accent, marginTop: 8 }}>mục tiêu</div>
        <div style={{ ...font(900, 46), color: C.accent }}>tập</div>
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
        <SeriesTag start={f(3.6)} end={VIDEO_FRAMES} tag="Mẹo chọn thảm" brand="Louis Yoga" />
        <TpeScene />
        <StudioScene />
        <LongTerm />
        <RubberScene />
        <CheckGrid items={[["Thấm hút", 41.22], ["Bám tay", 42.84], ["Giữ lâu", 46.74], ["Đổ mồ hôi", 48.64]]} start={f(40.9)} end={f(50.85)} y={G} />
        <RecapRows title="Mới tập chọn thảm nào?" rows={[["Giá tốt · êm", "TPE 9 ly", 52.95], ["Bám tay chắc", "Asana · Moon", 58.55]]} start={50.9} end={(VIDEO_FRAMES - 3) / FPS} y={G - 20} />
        <Captions lines={CAPTIONS} y={CAP_Y} from={3.6} until={CLEAN_DURATION} />
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
