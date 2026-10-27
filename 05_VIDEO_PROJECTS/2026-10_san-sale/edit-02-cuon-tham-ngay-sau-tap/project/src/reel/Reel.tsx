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
// LOUIS YOGA REEL — STYLE 1.  Reel "Tập xong cuộn thảm luôn — lỗi khiến thảm nhanh mủn"
// (series Săn sale, video 02). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same set as video 01 (shelf behind, foam blocks / mats on the table below).
// The source has a picture-in-picture clip bottom-right for clean 6–21.5 s: the lower panels cover it.
const CAP_Y = 1030;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 15 segments (14 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.14, 1.3, 1.12, 1.26, 1.1, 1.22, 1.14, 1.28, 1.12, 1.24, 1.12, 1.22];
const HOOK_DROP = 1.7;
const MUN = 28.55;
const LOOSE = 41.33;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.5, 0.22], // hook drop
  [5.02, 5.7, 0.08], // "rất là nhiều"
  [10.7, 11.5, 0.1], // "kín lại"
  [21.57, 22.3, 0.08], // "hơi ẩm"
  [28.48, 29.3, 0.14], // "mủn"
  [LOOSE, 42.6, 0.12], // "cuộn lỏng tay"
  [55.98, 56.5, 0.08], // "bề mặt thảm"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 19.69, end: 21.55, film: 0, src: PH + "sinh-hoat/sinh-hoat_109_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Cuộn vào, cất đi luôn" },
  { start: 30.79, end: 32.9, film: 0, src: PH + "sinh-hoat/sinh-hoat_113_tham-tap-yoga-cao-su-basic-zen-2.jpg", mode: "photo", label: "Để thoáng cho khô" },
  { start: 48.4, end: 50.6, film: 0, src: PH + "sinh-hoat/sinh-hoat_310_tui-dung-tham-da-nang-cao-cap-m2371.jpg", mode: "photo", label: "Mang thảm về" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [MUN, 7, 9, 0],
  [LOOSE, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.57/s), one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [2.95, "quick-swoosh.mp3", 0.53], // panel: mồ hôi
  [5.02, "pop-2.mp3", 0.5], // rất nhiều
  [6.5, "quick-swoosh.mp3", 0.47], // panel: cuộn luôn
  [10.7, "pop.mp3", 0.5], // kín hơi
  [12.06, "quick-swoosh.mp3", 0.5], // panel: hơi nước
  [14.82, "pop-2.mp3", 0.5], // ✕ không thoát
  [17.2, "pop.mp3", 0.47], // đọng lại
  [19.69, "swoosh.mp3", 0.55], // photo in
  [21.6, "pop-2.mp3", 0.5], // hơi ẩm
  [23.27, "quick-swoosh.mp3", 0.47], // panel: hậu quả
  [24.53, "pop-2.mp3", 0.53], // ① mùi
  [26.51, "pop.mp3", 0.5], // ② độ bền
  [MUN, "punch.mp3", 0.85], // DỄ MỦN!
  [29.41, "punch.mp3", 0.75], // slam: đừng cuộn khi ướt
  [30.79, "swoosh.mp3", 0.5], // photo in
  [32.95, "quick-ting.mp3", 0.53], // ✓ khô rồi mới cuộn
  [35.1, "quick-swoosh.mp3", 0.5], // panel: không có thời gian
  [36.3, "pop-2.mp3", 0.5],
  [38.83, "pop.mp3", 0.47],
  [LOOSE, "punch.mp3", 0.7], // CUỘN LỎNG TAY
  [45.45, "quick-ting.mp3", 0.53], // ✓ vẫn thoáng
  [48.4, "swoosh.mp3", 0.5], // photo in
  [51.55, "pop-2.mp3", 0.5], // về nhà mở thảm
  [53.9, "quick-swoosh.mp3", 0.5], // checklist
  [54.9, "quick-ting.mp3", 0.53],
  [56.63, "quick-ting.mp3", 0.53],
  [57.89, "correct.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.4), f(3.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–2.9 s): "TẬP XONG / CUỘN THẢM LUÔN?" slams twice, gets crossed out, "DỄ MỦN THẢM!" stamp drops.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(2.95)} />
    <BigText start={0} end={f(2.95)} y={120} slam lines={[{ text: "Tập xong", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(2.95)} y={232} slam lines={[{ text: "cuộn thảm luôn?", color: C.accent, size: 94 }]} />
    <StrikeLine d="M120,345 L960,290" start={f(HOOK_DROP)} end={f(2.95)} length={860} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.9)} />
    <Stamp text="Dễ mủn thảm!" start={f(HOOK_DROP)} end={f(2.9)} x={540} y={G + 130} rot={-8} size={112} />
  </>
);

// "Khi tập thì mồ hôi nó thấm ra thảm rất là nhiều" — practice photo + text.
const SweatScene: React.FC = () => {
  const s = f(2.95);
  const e = f(6.45);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "sinh-hoat/sinh-hoat_112_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Khi tập" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Mồ hôi</Label>
      <Label x={370} y={82} size={58} color={C.white}>thấm ra</Label>
      <Label x={370} y={142} size={58} color={C.accent}>mặt thảm</Label>
      <Pill text="Rất nhiều" start={f(5.02)} end={e} x={760} y={40} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// "Tập xong cuộn lại luôn ... nó sẽ kín lại như này" — rolling photo + ✕ kín hơi.
const RollScene: React.FC = () => {
  const s = f(6.5);
  const e = f(12.0);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "cuon-tham/cuon-tham_266_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Cuộn ngay" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Tập xong</Label>
      <Label x={370} y={82} size={66} color={C.white}>cuộn</Label>
      <Label x={370} y={150} size={66} color={C.accent}>luôn</Label>
      <Pill text="✕ Kín hơi" start={f(10.7)} end={e} x={720} y={150} bg={C.pinkDeep} size={42} />
    </Panel>
  );
};

// "không có không gian để thoát hơi nước ... đọng hơi nước trong bề mặt thảm" — droplets rise and get trapped.
const VaporScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(12.06);
  const e = f(19.6);
  const lid = f(14.82);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "be-mat/be-mat_269_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Bề mặt thảm" x={30} y={25} w={260} h={220} start={s} end={e} />
      <div style={{ position: "absolute", left: 330, top: 30, width: 240, height: 210 }}>
        {[0, 1, 2, 3, 4].map((i) => {
          const t = (frame - s + i * 9) % 45;
          // free rise before the lid closes, then bounce under it
          const top = frame < lid ? interpolate(t, [0, 45], [190, -10]) : 30 + Math.abs(Math.sin((frame + i * 7) / 6)) * 26;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 20 + i * 44,
                top,
                width: 26,
                height: 34,
                borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%",
                background: "rgba(150,205,255,0.85)",
                boxShadow: "0 0 12px rgba(150,205,255,0.6)",
              }}
            />
          );
        })}
        {frame >= lid && <div style={{ position: "absolute", left: 0, top: 6, width: 240, height: 14, borderRadius: 8, background: C.accent, boxShadow: `0 0 16px ${C.accent}` }} />}
      </div>
      <Label x={600} y={40} size={30} color={C.dim} spacing={3} weight={800}>Hơi nước</Label>
      <Pill text="✕ không thoát" start={lid} end={e} x={735} y={100} bg={C.white} fg={C.ink} size={32} />
      <Pill text="Đọng lại" start={f(17.2)} end={e} x={735} y={178} bg={C.pinkDeep} size={36} />
    </Panel>
  );
};

// "làm giảm độ bền ... dễ bị mủn" — ① mùi, ② độ bền, durability bar drops, stamp.
const HarmScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(23.27);
  const e = f(29.35);
  const bar = interpolate(frame, [f(26.7), f(27.9)], [1, 0.28], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const red = interpolate(frame, [f(26.7), f(27.9)], [0, 1], clamp);
  return (
    <>
      <Kicker text="Thảm bị ẩm lâu" start={s} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <Pill text="① Để lại mùi" start={f(24.53)} end={e} x={240} y={28} bg={C.white} fg={C.ink} size={38} />
        <Pill text="② Giảm độ bền" start={f(26.51)} end={e} x={650} y={28} bg={C.gold} fg={C.ink} size={38} />
        <Label x={50} y={132} size={30} color={C.dim} spacing={3} weight={800}>Độ bền thảm</Label>
        <div style={{ position: "absolute", left: 50, top: 178, width: 800, height: 46, borderRadius: 12, background: "rgba(255,255,255,0.12)" }}>
          <div
            style={{
              width: 800 * bar,
              height: 46,
              borderRadius: 12,
              background: `linear-gradient(90deg, ${C.accent}, rgba(${Math.round(226 + 29 * red)},${Math.round(49 + 40 * red)},${Math.round(139 - 80 * red)},1))`,
            }}
          />
        </div>
        <Stamp text="Dễ mủn!" start={f(MUN)} end={e} x={640} y={196} rot={-8} size={84} />
      </Panel>
    </>
  );
};

// "Không cuộn thảm khi ướt" — the main advice slams; "rồi mới cuộn vào" gets a ✓.
const AdviceScene: React.FC = () => (
  <>
    <TopShade start={f(29.41)} end={f(30.75)} />
    <BigText
      start={f(29.41)}
      end={f(30.75)}
      y={200}
      slam
      lines={[
        { text: "Đừng cuộn", color: C.white, size: 100 },
        { text: "khi còn ướt", color: C.accent, size: 104 },
      ]}
    />
    <Pill text="✓ Khô rồi mới cuộn" start={f(32.95)} end={f(35.0)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />
  </>
);

// "Không có nhiều thời gian / để thảm ở phòng tập → cuộn lỏng tay".
const BusyScene: React.FC = () => {
  const s = f(35.1);
  const e = f(41.25);
  return (
    <>
      <Panel start={s} end={e} y={G} h={270}>
        <Label x={0} y={26} size={30} color={C.dim} spacing={4} weight={800}>
          <div style={{ width: 900, textAlign: "center" }}>Nếu bạn</div>
        </Label>
        <Pill text="Không có nhiều thời gian" start={f(36.3)} end={e} x={450} y={88} bg={C.white} fg={C.ink} size={40} />
        <Pill text="Để thảm ở phòng tập" start={f(38.83)} end={e} x={450} y={172} bg={C.pinkDeep} size={40} />
      </Panel>
      <TopShade start={f(LOOSE)} end={f(43.45)} />
      <BigText
        start={f(LOOSE)}
        end={f(43.45)}
        y={210}
        slam
        lines={[
          { text: "Cuộn", color: C.white, size: 96 },
          { text: "lỏng tay", color: C.accent, size: 116 },
        ]}
      />
    </>
  );
};

// Closing checklist answers the hook.
const Closing: React.FC = () => (
  <DoDont
    title="SAU KHI TẬP"
    rows={[
      ["Lau qua bề mặt thảm", 54.9, true],
      ["Để thoáng cho khô", 56.63, true],
      ["Khô rồi mới cất đi", 57.89, true],
    ]}
    start={53.9}
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
      <Polaroid src={PH + "cuon-tham/cuon-tham_005_combo-tham-yoga-aura-khan-da-nang-va-gac.jpg"} label="Thảm cao su" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_258_tham-tap-yoga-cao-su-sunflower-2.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(2.95)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <SweatScene />
        <RollScene />
        <VaporScene />
        <Pill text="Hơi ẩm bị giữ lại" start={f(21.6)} end={f(23.2)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
        <HarmScene />
        <AdviceScene />
        <BusyScene />
        <Pill text="✓ Vẫn thoáng khí" start={f(45.45)} end={f(47.7)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />
        <Pill text="Về nhà → mở thảm ra" start={f(51.55)} end={f(53.8)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={2.9} until={CLEAN_DURATION} />
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
