import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BigText, BottomShade, Impact, Kicker, Panel, PhotoCard, Pill, Polaroid, SeriesTag, Stamp, TopShade, useImpact } from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { DoDont } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Tập xong có cần lau thảm mỗi ngày"
// (series Săn sale, video 05). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// Source: speaker has her back to the camera for the hook question (clean 0–3.6 s) and bends away
// to put the mat down at clean 30.97–34.97 s → both covered by Louis Yoga B-roll.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — seated at the table, face lower than in 01/02 (face centre y≈910).
const CAP_Y = 1100;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 11 segments (10 cuts), alternate tight/wide.
const SEG_ZOOM = [1.2, 1.12, 1.26, 1.1, 1.28, 1.14, 1.24, 1.1, 1.26, 1.12, 1.24];
const HOOK_END = 3.6;
const HOOK_DROP = 1.95; // "...có phải vệ sinh không?"
const MUI = 19.59; // "để lại mùi"
const GIAM = 45.43; // "giảm đi luôn"
const THOANG = 46.96; // "để thảm cho nó thoáng ra"
const PUNCHES: Punch[] = [
  [7.66, 8.3, 0.1], // "rất là tốt"
  [13.99, 14.38, 0.08], // "rất là nhiều"
  [MUI, 20.14, 0.14], // "mùi"
  [24.06, 24.77, 0.1], // "khăn mềm ẩm"
  [GIAM, 46.17, 0.14], // "giảm"
  [47.96, 48.47, 0.08], // "thoáng"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga only: brand film (hand wiping the mat surface) + louisyoga.vn photos.
const BROLL: Broll[] = [
  { start: 0, end: HOOK_END, film: 43.4, cx: 1150, mode: "crop", label: "Sau mỗi buổi tập" },
  { start: 30.94, end: 32.57, film: 0, src: PH + "sinh-hoat/sinh-hoat_114_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Để thảm khô" },
  { start: 32.57, end: 34.97, film: 0, src: PH + "cuon-tham/cuon-tham_008_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg", mode: "photo", label: "Khô rồi mới cuộn, cất" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [MUI, 7, 9, 0],
  [GIAM, 7, 9, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density, one sound per beat.
const CUES: Cue[] = [
  [0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [4.74, "quick-ting.mp3", 0.5], // ✓ lau thảm
  [7.92, "quick-swoosh.mp3", 0.5], // panel: mỗi buổi tập
  [10.1, "pop-2.mp3", 0.5], // ① mồ hôi
  [11.1, "pop.mp3", 0.47], // ② tay chân
  [13.99, "pop-2.mp3", 0.53], // RẤT NHIỀU
  [14.34, "quick-swoosh.mp3", 0.47], // panel: để lâu
  [17.53, "pop-2.mp3", 0.5], // ✕ không vệ sinh
  [MUI, "punch.mp3", 0.82], // ĐỂ LẠI MÙI!
  [20.19, "pop-2.mp3", 0.5], // tập hằng ngày
  [21.97, "quick-swoosh.mp3", 0.5], // panel: khăn
  [24.06, "quick-ting.mp3", 0.5], // khăn mềm ẩm
  [25.22, "pop-2.mp3", 0.5], // lau bề mặt
  [26.57, "quick-swoosh.mp3", 0.47], // panel: lau đi
  [29.4, "pop.mp3", 0.47], // bụi bẩn
  [30.94, "swoosh.mp3", 0.55], // photo in
  [33.54, "quick-ting.mp3", 0.5], // ✓ sạch hơn
  [34.97, "quick-swoosh.mp3", 0.5], // panel: nóng ẩm
  [36.97, "pop-2.mp3", 0.5],
  [41.17, "pop.mp3", 0.47],
  [42.57, "quick-swoosh.mp3", 0.47], // battery
  [43.61, "digital-counting-1.mp3", 0.45], // drains
  [GIAM, "punch.mp3", 0.85], // GIẢM ĐỘ BỀN!
  [THOANG, "punch.mp3", 0.75], // slam: để thảm thoáng ra
  [49.36, "pop-2.mp3", 0.5], // bay hơi
  [52.17, "quick-swoosh.mp3", 0.5], // checklist
  [53.02, "quick-ting.mp3", 0.53],
  [53.73, "correct.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(HOOK_END - 0.4), f(HOOK_END + 0.2), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–3.6 s, over brand film of a hand wiping the mat): "TẬP XONG MỖI NGÀY / CÓ CẦN / LAU THẢM?" → stamp "NÊN LAU!".
const Hook: React.FC = () => (
  <>
    {useCurrentFrame() < f(HOOK_END) && <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 22%, rgba(0,0,0,0.5) 29%, rgba(0,0,0,0.5) 47%, rgba(0,0,0,0) 54%)" }} />}
    <Kicker text="TẬP XONG MỖI NGÀY" start={0} end={f(HOOK_END)} y={560} color={C.gold} />
    <BigText start={0} end={f(HOOK_END)} y={620} slam lines={[{ text: "Có cần", color: C.white, size: 112 }]} />
    <BigText start={f(0.55)} end={f(HOOK_END)} y={745} slam lines={[{ text: "lau thảm?", color: C.accent, size: 124 }]} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Nên lau!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 90} rot={-8} size={120} />
  </>
);

// "...lau thảm, vệ sinh thảm được thì nó cũng sẽ rất là tốt"
const GoodScene: React.FC = () => <Pill text="✓ Lau thảm sau buổi tập" start={f(4.74)} end={f(7.88)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />;

// "mỗi buổi tập thì lượng mồ hôi, tay chân massage với cả dẫm lên thảm rất là nhiều"
const SweatScene: React.FC = () => {
  const s = f(7.92);
  const e = f(14.38);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "sinh-hoat/sinh-hoat_263_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Mỗi buổi tập" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={30} size={30} color={C.dim} spacing={3} weight={800}>Trên mặt thảm</Label>
      <Pill text="① Mồ hôi" start={f(10.1)} end={e} x={500} y={110} bg={C.white} fg={C.ink} size={38} />
      <Pill text="② Tay chân tì, dẫm" start={f(11.1)} end={e} x={600} y={195} bg={C.pinkDeep} size={38} />
      <Pill text="Rất nhiều" start={f(13.99)} end={e} x={790} y={110} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// "mồ hôi thấm ra thảm nhiều mà mình để lâu, không vệ sinh thì chắc chắn sẽ để lại mùi" — odour waves + stamp.
const OdorScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(14.34);
  const e = f(20.14);
  return (
    <>
      <TopShade start={f(MUI) - 3} end={e} />
      <Kicker text="MỒ HÔI THẤM VÀO THẢM" start={s} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "be-mat/be-mat_108_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Bề mặt thảm" x={30} y={25} w={280} h={220} start={s} end={e} />
        <div style={{ position: "absolute", left: 330, top: 30, width: 150, height: 210 }}>
          {[0, 1, 2].map((i) => {
            const t = (frame - s + i * 12) % 36;
            const op = frame < f(16.93) ? 0 : interpolate(t, [0, 10, 36], [0, 0.9, 0]);
            return (
              <svg key={i} width={40} height={200} style={{ position: "absolute", left: 10 + i * 46, top: interpolate(t, [0, 36], [20, -20]), opacity: op }}>
                <path d="M20,195 C0,165 40,135 20,105 C0,75 40,45 20,15" stroke="rgba(190,220,120,0.95)" strokeWidth={8} fill="none" strokeLinecap="round" />
              </svg>
            );
          })}
        </div>
        <Label x={500} y={36} size={46} color={C.white}>Để lâu</Label>
        <Pill text="✕ Không vệ sinh" start={f(17.53)} end={e} x={680} y={150} bg={C.white} fg={C.ink} size={38} />
      </Panel>
      <Stamp text="Để lại mùi!" start={f(MUI)} end={e} x={540} y={450} rot={-7} size={104} />
    </>
  );
};

// "Đối với tần suất tập hằng ngày"
const DailyScene: React.FC = () => (
  <>
    <TopShade start={f(20.19)} end={f(21.73)} />
    <Pill text="Tập hằng ngày" start={f(20.19)} end={f(21.73)} x={W / 2} y={230} bg={C.pinkDeep} size={56} />
  </>
);

// "sau mỗi buổi tập thì nên dùng cái khăn mềm ẩm, lau qua cái bề mặt thảm"
const TowelScene: React.FC = () => {
  const s = f(21.97);
  const e = f(26.52);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "khan/khan_061_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn mềm" x={30} y={25} w={300} h={220} start={s} end={e} highlight />
      <Label x={370} y={34} size={30} color={C.dim} spacing={3} weight={800}>Dùng khăn</Label>
      <Label x={370} y={76} size={64} color={C.white}>mềm</Label>
      <Label x={560} y={76} size={64} color={C.accent}>ẩm</Label>
      <Pill text="Lau qua bề mặt thảm" start={f(25.22)} end={e} x={600} y={200} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// "để lau đi bớt cái mồ hôi này hay là các cái bụi bẩn bám vào trên bề mặt thảm"
const WipeScene: React.FC = () => {
  const s = f(26.57);
  const e = f(30.9);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "sinh-hoat/sinh-hoat_110_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Lau sạch" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={34} size={30} color={C.dim} spacing={3} weight={800}>Lau đi bớt</Label>
      <Pill text="Mồ hôi" start={f(27.96)} end={e} x={480} y={110} bg={C.white} fg={C.ink} size={42} />
      <Pill text="Bụi bẩn bám" start={f(29.4)} end={e} x={560} y={195} bg={C.pinkDeep} size={42} />
    </Panel>
  );
};

// "nhất là thời tiết nóng ẩm, để thảm ẩm, cất đi trong thời gian dài"
const HumidScene: React.FC = () => {
  const s = f(34.97);
  const e = f(42.52);
  return (
    <>
      <Kicker text="NHẤT LÀ KHI" start={s} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <Pill text="Trời nóng ẩm" start={f(36.97)} end={e} x={450} y={50} bg={C.white} fg={C.ink} size={40} />
        <Pill text="Thảm còn ẩm → cất luôn" start={f(38.35)} end={e} x={450} y={135} bg={C.pinkDeep} size={40} />
        <Pill text="Trong thời gian dài" start={f(41.17)} end={e} x={450} y={220} bg={C.gold} fg={C.ink} size={40} />
      </Panel>
    </>
  );
};

// "thì chắc chắn là cái độ bền của thảm nó cũng sẽ giảm đi luôn" — 5-cell durability gauge drains, stamp.
const DurabilityScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(42.57);
  const e = f(46.42);
  const left = interpolate(frame, [f(43.61), f(45.37)], [5, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={50} y={30} size={30} color={C.dim} spacing={3} weight={800}>Độ bền thảm</Label>
      <div style={{ position: "absolute", left: 50, top: 90, width: 470, height: 140, borderRadius: 18, border: "6px solid rgba(255,255,255,0.8)", display: "flex", padding: 10, gap: 10 }}>
        {[0, 1, 2, 3, 4].map((i) => {
          const on = Math.max(0, Math.min(1, left - i));
          return <div key={i} style={{ flex: 1, borderRadius: 8, background: i === 0 ? "#FF4D4D" : C.accent, opacity: 0.12 + 0.88 * on }} />;
        })}
      </div>
      <div style={{ position: "absolute", left: 530, top: 135, width: 20, height: 50, borderRadius: 6, background: "rgba(255,255,255,0.8)" }} />
      <Stamp text="Giảm!" start={f(GIAM)} end={e} x={720} y={160} rot={-8} size={84} />
    </Panel>
  );
};

// "mình nên để thảm cho nó thoáng ra, cho nó bay bớt các cái hơi nước đi" — slam + vapour rising free.
const AirScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(48.47);
  const e = f(52.12);
  return (
    <>
      <TopShade start={f(THOANG)} end={f(48.52)} />
      <BigText
        start={f(THOANG)}
        end={f(48.52)}
        y={220}
        slam
        lines={[
          { text: "Để thảm", color: C.white, size: 100 },
          { text: "thoáng ra", color: C.accent, size: 116 },
        ]}
      />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "sinh-hoat/sinh-hoat_264_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Sau khi tập" x={30} y={25} w={260} h={220} start={s} end={e} />
        <div style={{ position: "absolute", left: 320, top: 20, width: 220, height: 230 }}>
          {[0, 1, 2, 3, 4].map((i) => {
            const t = (frame - s + i * 9) % 45;
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 10 + i * 42,
                  top: interpolate(t, [0, 45], [200, -10]),
                  opacity: interpolate(t, [0, 8, 34, 45], [0, 0.9, 0.9, 0]),
                  width: 24,
                  height: 32,
                  borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%",
                  background: "rgba(150,205,255,0.85)",
                  boxShadow: "0 0 12px rgba(150,205,255,0.6)",
                }}
              />
            );
          })}
        </div>
        <Label x={570} y={36} size={30} color={C.dim} spacing={3} weight={800}>Bay bớt</Label>
        <Pill text="Hơi nước" start={f(49.36)} end={e} x={700} y={120} bg={C.white} fg={C.ink} size={38} />
        <Pill text="Hơi mồ hôi" start={f(50.3)} end={e} x={700} y={200} bg={C.pinkDeep} size={38} />
      </Panel>
    </>
  );
};

// Closing checklist answers the hook.
const Closing: React.FC = () => (
  <DoDont
    title="SAU MỖI BUỔI TẬP"
    rows={[
      ["Lau bằng khăn mềm ẩm", 52.32, true],
      ["Để thoáng cho khô", 53.02, true],
      ["Khô rồi mới cất đi", 53.73, true],
    ]}
    start={52.17}
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
      <Kicker text="xem thêm mẹo vệ sinh thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src={PH + "khan/khan_060_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn lau" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
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
        <GoodScene />
        <SweatScene />
        <OdorScene />
        <DailyScene />
        <TowelScene />
        <WipeScene />
        <Pill text="✓ Sạch hơn" start={f(33.54)} end={f(34.92)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />
        <HumidScene />
        <DurabilityScene />
        <AirScene />
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
