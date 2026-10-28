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
// LOUIS YOGA REEL — STYLE 1.  Reel "Chai xịt vệ sinh thảm: xịt lên khăn, đừng xịt thẳng lên thảm"
// (series Săn thảm 24/10, video 02). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// Two speakers: Phúc standing (clean 0–25.95, head high in frame → hook + panels in the LOWER band),
// Thắm seated (25.95–end, head low → titles in the TOP band, panels below).
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands
const SWITCH = 25.95; // source join Phúc → Thắm (not a cut of ours, but needs a zoom change)
const JOIN2 = 47.5; // source join inside Thắm's part (small camera shift)
const CAP_A = 1250; // captions while Phúc speaks
const CAP_B = 1200; // captions while Thắm speaks
const G = 1400;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 8 cuts + 2 source joins = 11 segments, alternate tight/wide.
const ALL_CUTS = [...CUTS, SWITCH, JOIN2].sort((a, b) => a - b);
const SEG_ZOOM = [1.2, 1.1, 1.16, 1.1, 1.2, 1.12, 1.22, 1.12, 1.26, 1.12, 1.24];
const HOOK_DROP = 1.84;
const LOANG = 9.55;
const KHAN = 12.37;
const BEN = 53.58;
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.6, 0.2], // hook drop
  [4.28, 4.9, 0.08], // "không đều"
  [LOANG, 10.1, 0.1], // "vết loang"
  [27.13, 28.0, 0.08], // "nhạy cảm"
  [32.89, 33.9, 0.08], // "giảm bớt mùi"
  [36.23, 36.7, 0.08], // "chuyên dụng"
  [43.74, 44.4, 0.1], // "khô nhanh hơn"
  [51.42, 52.0, 0.1], // "khô rồi"
];
// Phúc wipes the hanging mat (left of frame) with the towel — slide the camera onto his hand.
const FOCUS: Focus[] = [[14.55, 16.3, 380, 840, 1.16]];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 16.9, end: 19.2, film: 0, src: PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg", mode: "photo", label: "Mùi hương dễ chịu" },
  { start: 40.45, end: 42.2, film: 0, src: PH + "khan/khan_060_khan-lau-mo-hoi-tap-yoga.jpg", mode: "photo", label: "Xịt ra khăn rồi lau" },
  { start: 52.05, end: 53.3, film: 0, src: PH + "cuon-tham/cuon-tham_266_tham-tap-yoga-cao-su-xo-dua-aura.jpg", mode: "photo", label: "Khô rồi mới cuộn" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.76, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [LOANG, 7, 9, 0],
  [51.42, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.55/s), one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.76, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [2.95, "quick-swoosh.mp3", 0.5], // panel: xịt thẳng
  [4.28, "pop.mp3", 0.5], // ✕ không đều
  [5.25, "quick-swoosh.mp3", 0.47], // panel: đọng lại
  [6.65, "pop-2.mp3", 0.5], // đọng lại
  [LOANG, "punch.mp3", 0.8], // VẾT LOANG!
  [10.8, "quick-swoosh.mp3", 0.5], // panel: khăn sạch
  [KHAN, "quick-ting.mp3", 0.53], // ✓ khăn sạch
  [14.75, "pop-2.mp3", 0.5], // ✓ lau nhẹ
  [16.9, "swoosh.mp3", 0.55], // photo in
  [20.9, "quick-swoosh.mp3", 0.47], // panel: lợi ích
  [21.0, "quick-ting.mp3", 0.5], // ✓ mùi dễ chịu
  [24.25, "quick-ting.mp3", 0.53], // ✓ kháng khuẩn
  [27.13, "punch.mp3", 0.75], // slam: nhạy cảm mùi cao su
  [29.45, "quick-swoosh.mp3", 0.47], // panel: hoặc muốn
  [32.17, "pop-2.mp3", 0.5], // sạch hơn
  [32.89, "pop.mp3", 0.5], // giảm bớt mùi
  [34.0, "quick-swoosh.mp3", 0.5], // panel: chuyên dụng
  [36.23, "pop-2.mp3", 0.55], // ✓ chuyên dụng
  [37.85, "quick-ting.mp3", 0.5], // ít ảnh hưởng bề mặt
  [40.45, "swoosh.mp3", 0.55], // photo in: khăn
  [42.25, "quick-swoosh.mp3", 0.47], // panel: so sánh
  [43.74, "quick-ting.mp3", 0.53], // ✓ xịt ra khăn
  [44.04, "pop-2.mp3", 0.5], // khô nhanh hơn
  [45.6, "pop.mp3", 0.47], // ✕ xịt thẳng
  [47.5, "pop-2.mp3", 0.45], // quan trọng
  [51.42, "punch.mp3", 0.75], // slam: khô rồi mới cuộn
  [52.05, "swoosh.mp3", 0.5], // photo in: cuộn
  [53.35, "quick-swoosh.mp3", 0.47], // checklist
  [53.6, "quick-ting.mp3", 0.5],
  [BEN, "pop-2.mp3", 0.5], // thảm bền hơn
  [54.15, "quick-ting.mp3", 0.5],
  [54.7, "correct.mp3", 0.53],
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

// Hook (0–2.9 s): Phúc's head fills the top band, so the hook lives in the lower band.
// "XỊT THẲNG / LÊN THẢM?" slams twice, gets crossed out, "SAI CÁCH!" stamp drops.
const Hook: React.FC = () => (
  <>
    <BottomShade start={0} end={f(2.95)} />
    <BigText start={0} end={f(2.95)} y={1215} slam lines={[{ text: "Xịt thẳng", color: C.white, size: 108 }]} />
    <BigText start={f(0.76)} end={f(2.95)} y={1340} slam lines={[{ text: "lên thảm?", color: C.accent, size: 116 }]} />
    <StrikeLine d="M150,1450 L930,1290" start={f(HOOK_DROP)} end={f(2.95)} length={800} />
    <Stamp text="Sai cách!" start={f(HOOK_DROP)} end={f(2.9)} x={540} y={1580} rot={-8} size={104} />
  </>
);

// "lúc mình xịt, mình xịt không đều" — spray bottle photo + ✕ không đều.
const UnevenScene: React.FC = () => {
  const s = f(2.95);
  const e = f(5.15);
  return (
    <Panel start={s} end={e} y={G} h={250}>
      <PhotoCard src={PH + "xit-ve-sinh/xit-ve-sinh_318_xit-tham-yoga-huong-chanh-sa.jpg"} label="Xịt thẳng" x={30} y={20} w={280} h={210} start={s} end={e} />
      <Label x={350} y={36} size={30} color={C.dim} spacing={3} weight={800}>Xịt lên thảm</Label>
      <Label x={350} y={80} size={62} color={C.white}>dễ xịt</Label>
      <Label x={350} y={146} size={62} color={C.accent}>không đều</Label>
      <Pill text="✕" start={f(4.28)} end={e} x={800} y={70} bg={C.pinkDeep} size={60} />
    </Panel>
  );
};

// "nước vệ sinh thảm đọng lại trên bề mặt thảm → vết loang" — drops fall, a stain spreads, stamp.
const StainScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(5.25);
  const e = f(10.15);
  const pool = interpolate(frame, [f(6.65), f(LOANG)], [0.15, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <Panel start={s} end={e} y={G} h={250}>
      <div style={{ position: "absolute", left: 40, top: 30, width: 420, height: 190, borderRadius: 18, background: "#2F6B5A", overflow: "hidden", border: "3px solid rgba(255,255,255,0.8)" }}>
        {[0, 1, 2].map((i) => {
          const t = (frame - s + i * 11) % 33;
          const top = interpolate(t, [0, 33], [-30, 120]);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 150 + i * 50,
                top,
                width: 22,
                height: 30,
                borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%",
                background: "rgba(170,215,255,0.9)",
              }}
            />
          );
        })}
        <div
          style={{
            position: "absolute",
            left: 210 - 170 * pool,
            top: 140 - 40 * pool,
            width: 340 * pool,
            height: 80 * pool,
            borderRadius: "48% 52% 45% 55% / 55% 45% 55% 45%",
            background: "rgba(20,45,38,0.85)",
            boxShadow: "0 0 18px rgba(10,30,25,0.9) inset",
          }}
        />
        <div style={{ position: "absolute", left: 12, bottom: 10, background: "rgba(14,10,16,0.78)", color: C.white, padding: "6px 14px", borderRadius: 10, ...font(900, 28) }}>Bề mặt thảm</div>
      </div>
      <Label x={500} y={36} size={30} color={C.dim} spacing={3} weight={800}>Nước vệ sinh</Label>
      <Pill text="Đọng lại" start={f(6.65)} end={e} x={690} y={70} bg={C.white} fg={C.ink} size={40} />
      <Stamp text="Vết loang!" start={f(LOANG)} end={e} x={650} y={196} rot={-6} size={60} />
    </Panel>
  );
};

// "hãy xịt lên trên bề mặt cái khăn sạch như thế này" — the core advice, towel photo.
const TowelScene: React.FC = () => {
  const s = f(10.8);
  const e = f(13.65);
  return (
    <Panel start={s} end={e} y={G} h={250}>
      <PhotoCard src={PH + "khan/khan_059_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn sạch" x={30} y={20} w={280} h={210} start={s} end={e} highlight />
      <Label x={350} y={36} size={30} color={C.dim} spacing={3} weight={800}>Hãy xịt lên</Label>
      <Label x={350} y={84} size={92} color={C.accent}>KHĂN</Label>
      <Pill text="✓ Sạch" start={f(KHAN)} end={e} x={770} y={110} bg={C.gold} fg={C.ink} size={44} />
    </Panel>
  );
};

// "Và nó cũng sẽ giúp cho bề mặt thảm được kháng khuẩn tốt hơn" — benefits of the towel method.
const BenefitScene: React.FC = () => (
  <DoDont
    title="XỊT KHĂN RỒI LAU"
    rows={[
      ["Mùi hương dễ chịu", 21.0, true],
      ["Kháng khuẩn tốt hơn", 24.25, true],
    ]}
    start={20.9}
    end={SWITCH - 0.05}
    y={G}
  />
);

// Thắm: "Nếu mà mọi người bị nhạy cảm với các mùi thảm cao su này" — top-band slam.
const SensitiveScene: React.FC = () => (
  <>
    <TopShade start={f(27.13)} end={f(29.4)} />
    <BigText
      start={f(27.13)}
      end={f(29.4)}
      y={150}
      slam
      lines={[
        { text: "Nhạy cảm", color: C.white, size: 100 },
        { text: "mùi cao su?", color: C.accent, size: 100 },
      ]}
    />
  </>
);

// "Hoặc là muốn vệ sinh thảm sạch hơn, giảm bớt mùi"
const CleanerScene: React.FC = () => {
  const s = f(29.45);
  const e = f(33.95);
  return (
    <Panel start={s} end={e} y={G} h={250}>
      <div style={{ position: "absolute", top: 26, left: 0, width: 900, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>Hoặc muốn</div>
      <Pill text="Thảm sạch hơn" start={f(32.17)} end={e} x={250} y={110} bg={C.white} fg={C.ink} size={42} />
      <Pill text="Giảm bớt mùi" start={f(32.89)} end={e} x={660} y={110} bg={C.pinkDeep} size={42} />
    </Panel>
  );
};

// "nên sử dụng thêm các nước vệ sinh thảm chuyên dụng nhé → ít bị ảnh hưởng đến bề mặt thảm"
const SprayScene: React.FC = () => {
  const s = f(34.0);
  const e = f(40.35);
  return (
    <Panel start={s} end={e} y={G} h={250}>
      <PhotoCard src={PH + "xit-ve-sinh/xit-ve-sinh_026_combo-tham-yoga-basic-khan-da-nang-va-xi.jpg"} label="Xịt thảm" x={30} y={20} w={280} h={210} start={s} end={e} />
      <Label x={350} y={30} size={30} color={C.dim} spacing={3} weight={800}>Nước vệ sinh thảm</Label>
      <Label x={350} y={72} size={64} color={C.accent}>chuyên dụng</Label>
      <Pill text="✓ Ít ảnh hưởng bề mặt" start={f(37.85)} end={e} x={610} y={160} bg={C.gold} fg={C.ink} size={34} />
    </Panel>
  );
};

// "xịt ra cái khăn rồi lau thì khô nhanh hơn so với xịt trực tiếp lên bề mặt"
const DryScene: React.FC = () => (
  <>
    <TopShade start={f(42.25)} end={f(47.4)} />
    <Kicker text="CÁI NÀO KHÔ NHANH HƠN?" start={f(42.25)} end={f(47.4)} y={240} color={C.gold} />
    <DoDont
      title="LAU THẢM"
      rows={[
        ["Xịt ra khăn → khô nhanh", 43.74, true],
        ["Xịt thẳng lên thảm", 45.6, false],
      ]}
      start={42.25}
      end={47.4}
      y={G}
    />
  </>
);

// "Quan trọng là ... nên để thảm cho nó khô rồi mình mới cuộn vào cất đi"
const RollScene: React.FC = () => (
  <>
    <TopShade start={f(47.5)} end={f(51.35)} />
    <Kicker text="QUAN TRỌNG" start={f(47.5)} end={f(51.35)} y={240} color={C.gold} />
    <Pill text="Vệ sinh xong" start={f(49.06)} end={f(51.35)} x={W / 2} y={G + 90} bg={C.pinkDeep} size={46} />
    <TopShade start={f(51.42)} end={f(52.05)} />
    <BigText
      start={f(51.42)}
      end={f(52.05)}
      y={170}
      slam
      lines={[
        { text: "Khô rồi", color: C.white, size: 104 },
        { text: "mới cuộn", color: C.accent, size: 112 },
      ]}
    />
  </>
);

// Closing checklist answers the hook + "độ bền" stamp.
const Closing: React.FC = () => (
  <>
    <DoDont
      title="VỆ SINH THẢM ĐÚNG CÁCH"
      rows={[
        ["Xịt lên khăn sạch", 53.6, true],
        ["Lau nhẹ bề mặt", 54.15, true],
        ["Khô rồi mới cuộn", 54.7, true],
      ]}
      start={53.35}
      end={CLEAN_DURATION - 0.05}
      y={G - 60}
    />
    <TopShade start={f(BEN)} end={f(CLEAN_DURATION - 0.05)} />
    <BigText start={f(BEN)} end={f(CLEAN_DURATION - 0.05)} y={225} slam lines={[{ text: "Thảm bền hơn", color: C.gold, size: 84 }]} />
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
      <Kicker text="xem thêm mẹo dùng thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src={PH + "xit-ve-sinh/xit-ve-sinh_320_xit-tham-yoga-huong-chanh-sa.jpg"} label="Xịt thảm" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "khan/khan_060_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn Louis" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <TalkingHead src={FOOTAGE} videoFrames={VIDEO_FRAMES} duration={DURATION} cuts={ALL_CUTS} face={FACE} segZoom={SEG_ZOOM} punches={PUNCHES} focus={FOCUS} muted={STEM !== "all"} />
        <BrollLayer items={BROLL} src={FILM} />
        <Hook />
        <SeriesTag start={f(2.95)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <UnevenScene />
        <StainScene />
        <TowelScene />
        <Pill text="✓ Lau nhẹ bề mặt thảm" start={f(14.75)} end={f(16.85)} x={W / 2} y={G + 90} bg={C.gold} fg={C.ink} size={46} />
        <BenefitScene />
        <SensitiveScene />
        <CleanerScene />
        <SprayScene />
        <DryScene />
        <RollScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_A} from={2.9} until={SWITCH} />
        <Captions lines={CAPTIONS} y={CAP_B} from={SWITCH} until={CLEAN_DURATION} />
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
