import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Impact, Pill, Polaroid, Stamp, useImpact, useLife, usePop } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { CaptionsOffMg, CAP_Y, ColTitle, FrostFootage, ICY, LeftShade, MgStage, MgTitle, MgWindow, MG_TOP, SAFE_CX, SAFE_L, SAFE_R, SafePanel, Section, Snowflake } from "../kit/style2";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// 03 · Mùa đông sàn lạnh: thảm dày có cần lót thêm không? (Săn thảm 24/10, người nói: Phúc)
// Safe zone Reels/TikTok: text that must be read stays in x 108–886, y 269–1248.
// Face sits centre-right (x ≈ 420–900, y ≈ 330–620) → titles/panels live in the empty LEFT
// column x 108–~450, y 280–800; captions under the chest; nothing to read below 1248.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands (safe zone constants come from kit/style2.tsx)
const COL_Y = 380; // top of the left-column content

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3"; // anh chốt lại nhạc bản v1 (= v5)
const PH = "louis-photos/";

// ▼ EDIT ▼ camera
const SEG_ZOOM = [1.12, 1.2, 1.1, 1.22, 1.12, 1.18, 1.1, 1.2, 1.12, 1.18, 1.1, 1.2, 1.12];
const HOOK_DROP = 1.85; // right after "miền Bắc"; the riser started at 0 peaks here
const HOOK_END = 5.3;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.6, 0.12],
  [14.95, 15.6, 0.06],
  [50.8, 51.6, 0.08],
];
const FOCUS: Focus[] = [[37.18, 40.45, 640, 880, 1.24]]; // "những cái dòng thảm này" → the mat at chest

// ▼ EDIT ▼ B-roll: Louis Yoga photos only
const BROLL: Broll[] = [
  { start: 32.2, end: 34.08, film: 0, src: PH + "tu-the/tu-the_196_tham-tap-yoga-cao-su-cao-cap-lilium.jpg", mode: "photo", label: "Huấn luyện viên" },
  { start: 34.08, end: 36.3, film: 0, src: PH + "tu-the/tu-the_091_tham-tap-yoga-cao-su-asana.jpg", mode: "photo", label: "Tập chuyên sâu" },
  { start: 46.41, end: 48.19, film: 0, src: PH + "sinh-hoat/sinh-hoat_111_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Trải thẳng ra sàn" },
];

// ▼ EDIT ▼ shake/flash
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [HOOK_DROP, 10, 18, 0.6],
  [50.8, 7, 9, 0],
];

// ▼ EDIT ▼ SFX
const CUES: Cue[] = [
  // Hook (bài học Quạ HD): open on a bright, slightly harsh sound; one "tense" bright sound ≈ every 7 s.
  [0.0, "glitch.mp3", 0.5], // "rắc" on frame 0
  [0.05, "punch.mp3", 0.8],
  [0.58, "pop-2.mp3", 0.5],
  [HOOK_DROP, "riser-metallic.mp3", 0.6], // cue = PEAK time (ONSET 1.81 s) → builds from ~0 s into the drop
  [HOOK_DROP, "punch.mp3", 0.9],
  [HOOK_DROP, "glasses-cheers-2.wav", 0.7], // "keng" lands on the stamp
  [5.35, "quick-swoosh.mp3", 0.4],
  [7.05, "glitch.mp3", 0.5], // stage 1 in
  [9.91, "pop-2.mp3", 0.45],
  [13.33, "ting.wav", 0.6], // "Bị lạnh!"
  [13.45, "punch.mp3", 0.7],
  [13.83, "quick-swoosh.mp3", 0.4],
  [14.95, "digital-counting-1.mp3", 0.45],
  [15.97, "quick-ting.mp3", 0.45],
  [16.6, "quick-swoosh.mp3", 0.45],
  [17.09, "pop-2.mp3", 0.4],
  [19.83, "pop.mp3", 0.4],
  [20.87, "swoosh.mp3", 0.35],
  [22.27, "glitch.mp3", 0.4], // split: thin mat lets the cold in
  [24.61, "pop-2.mp3", 0.45],
  [25.31, "camera-shutter.mp3", 0.45],
  [26.27, "digital-counting-1.mp3", 0.45],
  [30.63, "pop-2.mp3", 0.45],
  [32.2, "swoosh.mp3", 0.5],
  [34.08, "swoosh.mp3", 0.4],
  [40.52, "quick-swoosh.mp3", 0.45],
  [40.52, "new-item.wav", 0.5], // Lilium panel sparkle
  [42.94, "quick-ting.mp3", 0.45],
  [43.64, "correct.mp3", 0.45],
  [46.41, "swoosh.mp3", 0.45],
  [49.61, "punch.mp3", 0.8],
  [49.61, "glasses-cheers-2.wav", 0.6], // answer
  [50.8, "punch.mp3", 0.9],
  [52.22, "quick-ting.mp3", 0.45],
  [53.45, "quick-swoosh.mp3", 0.5],
  [53.7, "punch.mp3", 0.7],
  [53.9, "camera-shutter.mp3", 0.45],
  [54.2, "ding.mp3", 0.35],
];
// Hook: music in at full, cut to near-silence for 0.3 s before the drop, slams back with the punch,
// then settles under the voice (mix: --music-under 11 → ~16 dB under the voice while talking).
const MUSIC_CURVE: [number[], number[]] = [
  [0, 3, f(HOOK_DROP) - 10, f(HOOK_DROP) - 7, f(HOOK_DROP), f(HOOK_END), f(HOOK_END) + 15, VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.32, 0.32, 0.03, 0.34, 0.3, 0.13, 0.13, 0.32, 0.32, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Shared style-2 blocks (LeftShade, ColTitle, SafePanel, MgStage, MgTitle, Section, …) live in kit/style2.tsx.


// Hook 0–5.3 s: question in the left column, answer stamp drops on "miền Bắc".
const Hook: React.FC = () => (
  <>
    <LeftShade start={0} end={f(HOOK_END)} />
    <ColTitle text="Mùa đông" color={C.white} size={72} start={0} end={f(HOOK_END)} y={290} />
    <ColTitle text="có cần" color={C.white} size={62} start={f(0.55)} end={f(HOOK_END)} y={376} />
    <ColTitle text="lót thảm?" color={C.accent} size={72} start={f(0.55)} end={f(HOOK_END)} y={446} />
    <Stamp text="Không cần!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={320} y={620} rot={-8} size={54} />
  </>
);

// 13.8–16.6 s: rubber 4,5 ly.
const Rubber45: React.FC = () => {
  const frame = useCurrentFrame();
  const n = interpolate(frame, [f(14.95), f(15.35)], [0, 4.5], clamp);
  const s = f(13.83);
  const e = f(16.57);
  const life = useLife(s, e);
  if (!life) return null;
  return (
    <>
      <LeftShade start={s} end={e} />
      <ColTitle text="Thảm cao su" color={C.gold} size={40} start={s} end={e} y={COL_Y} slam={false} />
      {frame >= f(14.95) && (
        <div style={{ position: "absolute", left: SAFE_L, top: COL_Y + 50, opacity: life, ...font(900, 104), color: C.accent, textShadow: "0 6px 0 rgba(0,0,0,0.55)", whiteSpace: "nowrap" }}>
          {n.toFixed(1).replace(".", ",")}
          <span style={{ ...font(900, 52), color: C.white, marginLeft: 10 }}>ly</span>
        </div>
      )}
      <Pill text="✓ Tập thoải mái" start={f(15.97)} end={e} x={280} y={COL_Y + 180} size={32} />
    </>
  );
};

// ---- Motion-graphic explainers (v3): full-frame graphic stage, content inside the safe zone,
// captions keep running on top. They replace the small left-column panels on the technical parts.


// 7–13.8 s: why you get cold — cold air outside + a mat that is not thick enough.
const MgWhyCold: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(7.05);
  const e = f(13.83);
  const SX = 168;
  const SW = 620;
  return (
    <MgStage start={s} end={e} dy={150}>
      <MgTitle start={s}>
        Vì sao <span style={{ color: C.accent }}>bị lạnh?</span>
      </MgTitle>
      <svg width={W} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {Array.from({ length: 7 }).map((_, i) => {
          const x = SAFE_L + 30 + i * 120;
          const y = 470 + ((frame - s + i * 23) % 50) * 0.9;
          return <Snowflake key={i} x={x} y={y} r={14} o={interpolate(frame, [s + 4, s + 12], [0, 0.9], clamp)} />;
        })}
      </svg>
      <Pill text="Không khí lạnh" start={s + 6} end={e} x={SAFE_CX} y={385} bg="#1E2A38" fg={ICY} size={32} />
      <Section x={SX} y={560} w={SW} matH={16} matLabel="THẢM MỎNG" through flowFrom={f(11.33)} start={f(8.97)} />
      <Pill text="Hơi lạnh xuyên qua thảm" start={f(11.33)} end={e} x={SAFE_CX} y={880} bg={C.pinkDeep} size={32} />
      <Stamp text="Bị lạnh!" start={f(13.33)} end={e} x={SAFE_CX} y={1030} rot={-7} size={60} />
    </MgStage>
  );
};

// 16.6–25.3 s: the 4,5 ly rubber mat blocks the floor cold; then thin vs thick side by side.
const MgRubberBlocks: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(16.57);
  const split = f(22.27);
  const e = f(25.28);
  const one = frame < split;
  return (
    <MgStage start={s} end={e} dy={210}>
      <MgTitle start={s}>
        Thảm cao su <span style={{ color: C.accent }}>4,5 ly</span>
      </MgTitle>
      {one ? (
        <>
          <Section x={168} y={420} w={560} matH={64} matLabel="CAO SU" through={false} flowFrom={f(19.83)} start={s + 2} dim="4,5 ly" />
          <Pill text="✓ Không lo bị lạnh" start={f(17.09)} end={split} x={SAFE_CX} y={790} size={34} />
          <Pill text="Khí lạnh bốc lên → bị chặn" start={f(20.63)} end={split} x={SAFE_CX} y={880} bg="rgba(143,211,255,0.18)" fg={ICY} size={30} />
        </>
      ) : (
        <>
          <Section x={SAFE_L} y={430} w={340} matH={14} matLabel="MỎNG" through flowFrom={split} start={split} />
          <Section x={SAFE_R - 340} y={430} w={340} matH={56} matLabel="4,5 LY" through={false} flowFrom={split} start={split + 4} />
          <Pill text="✗ Ngấm vào người" start={split + 8} end={e} x={SAFE_L + 170} y={790} bg="rgba(143,211,255,0.2)" fg={ICY} size={28} />
          <Pill text="✓ Ấm, tập thoải mái" start={split + 12} end={e} x={SAFE_R - 170} y={790} size={28} />
          <Stamp text="Không tốt!" start={f(24.61)} end={e} x={SAFE_L + 170} y={930} rot={-6} size={44} />
        </>
      )}
    </MgStage>
  );
};

// 25.3–32.2 s: Lilium — real photo in a card (nothing printed over the photo), then thickness
// compared to the 4,5 ly mat, then the weight.
const MgLilium: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(25.31);
  const e = f(32.2);
  const cardP = usePop(s, 12);
  const th = f(26.07);
  const g = (at: number) => interpolate(frame, [at, at + 14], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const n = interpolate(frame, [th + 6, th + 22], [0, 6.5], clamp);
  const slab = (label: string, mm: number, x: number, color: string, at: number, big: boolean) => {
    const h = mm * 20 * g(at);
    return (
      <div style={{ position: "absolute", left: x, top: 760, width: 330, height: 200 }}>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 64, height: h, borderRadius: 10, background: color, boxShadow: big ? "0 0 30px rgba(255,90,174,0.55)" : "none" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 56, height: 4, background: "rgba(255,255,255,0.3)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, textAlign: "center", ...font(900, 30), color: big ? C.accent : C.white, opacity: g(at) }}>
          {label}
        </div>
      </div>
    );
  };
  const wP = usePop(f(30.63), 11);
  return (
    <MgStage start={s} end={e} dy={150}>
      <div
        style={{
          position: "absolute",
          left: SAFE_CX - 290,
          top: MG_TOP,
          width: 580,
          background: "#FAFAF7",
          borderRadius: 18,
          padding: 14,
          boxShadow: "0 24px 50px rgba(0,0,0,0.55)",
          transform: `translateY(${(1 - cardP) * -160}px) scale(${0.9 + 0.1 * cardP})`,
          opacity: Math.min(1, cardP * 2),
        }}
      >
        <Img src={staticFile(PH + "tu-the/tu-the_195_tham-tap-yoga-cao-su-cao-cap-lilium.jpg")} style={{ width: 552, height: 320, objectFit: "cover", borderRadius: 10, display: "block" }} />
        <div style={{ ...font(900, 34), color: C.ink, textAlign: "center", paddingTop: 12 }}>Thảm Lilium</div>
      </div>
      {frame >= th && (
        <>
          <div style={{ position: "absolute", left: SAFE_L, width: SAFE_R - SAFE_L, top: 724, textAlign: "center", ...font(800, 28), color: C.dim, letterSpacing: 3, opacity: g(th) }}>
            Độ dày
          </div>
          {slab("Cao su 4,5 ly", 4.5, SAFE_L + 20, "#7A6A80", th, false)}
          {slab(`Lilium ${n.toFixed(1).replace(".", ",")} ly`, 6.5, SAFE_R - 350, C.accent, th + 6, true)}
        </>
      )}
      {frame >= f(30.63) && (
        <div
          style={{
            position: "absolute",
            left: SAFE_CX - 250,
            top: 985,
            width: 500,
            height: 96,
            borderRadius: 999,
            background: C.gold,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 16,
            transform: `scale(${wP})`,
            boxShadow: "0 10px 24px rgba(0,0,0,0.45)",
          }}
        >
          <svg width={52} height={52} viewBox="0 0 52 52">
            <path d="M16 18 a10 10 0 0 1 20 0" stroke={C.ink} strokeWidth={5} fill="none" />
            <path d="M8 20 h36 l-4 26 h-28 z" fill={C.ink} />
          </svg>
          <span style={{ ...font(900, 40), color: C.ink, whiteSpace: "nowrap" }}>Nặng hơn 4 kg</span>
        </div>
      )}
    </MgStage>
  );
};

// 40.5–45 s: what the Lilium line brings.
const LiliumCheck: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(40.52);
  const e = f(45.2);
  const row = (text: string, at: number, i: number) => {
    if (frame < f(at)) return null;
    const p = interpolate(frame, [f(at), f(at) + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
    return (
      <div key={i} style={{ position: "absolute", left: 22, top: 92 + i * 70, display: "flex", alignItems: "center", transform: `scale(${0.6 + 0.4 * p})`, transformOrigin: "0% 50%", opacity: Math.min(1, p * 2) }}>
        <div style={{ width: 50, height: 50, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 28) }}>✓</div>
        <div style={{ marginLeft: 14, ...font(900, 28), color: C.white, whiteSpace: "nowrap" }}>{text}</div>
      </div>
    );
  };
  return (
    <SafePanel start={s} end={e} x={SAFE_L} y={COL_Y} w={372} h={250}>
      <div style={{ position: "absolute", left: 22, top: 22, ...font(900, 44), color: C.accent }}>Lilium</div>
      {row("Dày 6,5 ly", 42.94, 0)}
      {row("Cao su tự nhiên", 43.64, 1)}
    </SafePanel>
  );
};

// 49.6–53.4 s: answer to the hook.
const Answer: React.FC = () => (
  <>
    <LeftShade start={f(49.61)} end={VIDEO_FRAMES} />
    <ColTitle text="Không cần" color={C.white} size={80} start={f(49.61)} end={VIDEO_FRAMES} y={300} />
    <ColTitle text="lót thảm!" color={C.accent} size={80} start={f(50.8)} end={VIDEO_FRAMES} y={392} />
    <Pill text="✓ Trải là tập" start={f(52.22)} end={VIDEO_FRAMES} x={262} y={510} size={32} />
  </>
);

// CTA tail: freeze + dim, logo, follow, the two mats mentioned — all inside the safe zone.
const EndCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const s = VIDEO_FRAMES - 4;
  if (frame < s) return null;
  const dim = interpolate(frame, [s, s + 10], [0, 0.5], clamp);
  const fade = (d: number) => interpolate(frame, [s + d, s + d + 8], [0, 1], clamp);
  return (
    <>
      <AbsoluteFill style={{ background: `rgba(14,10,16,${dim})` }} />
      <div style={{ position: "absolute", left: SAFE_CX - 65, top: 290, transform: `scale(${interpolate(frame, [s, s + 10], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) })})` }}>
        <Img src={staticFile("brand/lotus.png")} style={{ width: 130, height: 130 }} />
      </div>
      <div style={{ position: "absolute", left: SAFE_L, width: SAFE_R - SAFE_L, top: 440, textAlign: "center", opacity: fade(6) }}>
        <div style={{ ...font(900, 80), color: C.white, textShadow: "0 6px 0 rgba(0,0,0,0.55)" }}>Follow</div>
        <div style={{ ...font(900, 80), color: C.accent, textShadow: "0 6px 0 rgba(0,0,0,0.55)" }}>Louis Yoga</div>
        <div style={{ ...font(800, 34), color: C.gold, letterSpacing: 3, marginTop: 14 }}>xem thêm mẹo chọn thảm</div>
      </div>
      <Polaroid src={PH + "tu-the/tu-the_195_tham-tap-yoga-cao-su-cao-cap-lilium.jpg"} label="Lilium · 6,5 ly" start={s + 8} end={DURATION + 1} x={130} y={760} w={290} h={250} rot={-6} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_115_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Cao su · 4,5 ly" start={s + 12} end={DURATION + 1} x={540} y={770} w={290} h={250} rot={5} />
    </>
  );
};

const MG_WINDOWS: MgWindow[] = [[7.05, 13.83], [16.57, 25.28], [25.31, 32.2]];


// ▲ EDIT ▲ ------------------------------------------------------------------------------

export const LouisYogaReel: React.FC = () => {
  useMontserrat();
  const { dx, dy, flash } = useImpact(IMPACTS);
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink, fontFamily: MONTSERRAT }}>
      <AbsoluteFill style={{ transform: `translate(${dx}px, ${dy}px) scale(${dx || dy ? 1.03 : 1})` }}>
        <FrostFootage windows={MG_WINDOWS}>
          <TalkingHead src={FOOTAGE} videoFrames={VIDEO_FRAMES} duration={DURATION} cuts={CUTS} face={FACE} segZoom={SEG_ZOOM} punches={PUNCHES} focus={FOCUS} muted={STEM !== "all"} />
        </FrostFootage>
        <BrollLayer items={BROLL} src={FILM} />
        <Hook />
        <Rubber45 />
        <MgWhyCold />
        <MgRubberBlocks />
        <MgLilium />
        <LiliumCheck />
        <Answer />
        {/* captions centred on the safe zone (x 108–886), scaled a touch so 20-char lines fit on one line */}
        <CaptionsOffMg windows={MG_WINDOWS}>
          <Captions lines={CAPTIONS} y={CAP_Y} from={1.7} until={CLEAN_DURATION} />
        </CaptionsOffMg>
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
