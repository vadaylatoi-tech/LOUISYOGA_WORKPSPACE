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
import { DoDont, NumberRows } from "../kit/scenes";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  "Phòng tập đã xịt khử khuẩn, thảm vẫn cần lau?"
// (đợt Săn thảm 24/10, video 01). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// Source livestream PiP (top-left, 0–336 x 0–584) and the "Tháng của nàng" sticker (78–634 x 1479–1632)
// were painted out in work/raw_patched.mp4 before cutting (static harmonic fill from a median frame).
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — man standing behind a white table (towel box + mat rolls bottom), shelf behind.
const CAP_Y = 1170;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 9 segments (8 cuts), alternate tight/wide.
const SEG_ZOOM = [1.16, 1.26, 1.12, 1.28, 1.14, 1.24, 1.12, 1.26, 1.14];
const HOOK_DROP = 2.2; // "thì vẫn không sạch hả"
const KY = 18.53; // "kỹ càng hơn"
const NGUOC = 35.07; // "thấm ngược lại vào cái khăn"
const BEN = 40.75; // "bền hơn"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 3.0, 0.22],
  [6.63, 7.3, 0.08], // "rất nhiều mồ hôi"
  [14.53, 15.2, 0.1], // "không gian chung"
  [KY, 19.2, 0.12],
  [29.67, 30.4, 0.08], // "lau nhẹ"
  [NGUOC, 35.8, 0.1],
  [BEN, 41.3, 0.1],
];
// "một cái tấm khăn sạch như thế này" — slide the camera onto the towel in his hands
const FOCUS: Focus[] = [[23.6, 25.4, 400, 930, 1.3]];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 8.13, end: 9.85, film: 0, src: PH + "be-mat/be-mat_269_tham-tap-yoga-cao-su-xo-dua-aura.jpg", mode: "photo", label: "Rơi thẳng xuống mặt thảm" },
  { start: 30.83, end: 32.5, film: 0, src: PH + "tu-the/tu-the_097_tham-tap-yoga-cao-su-asana.jpg", mode: "photo", label: "Mồ hôi lúc tập" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.6, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [KY, 7, 9, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.5/s), one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.6, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [4.0, "quick-swoosh.mp3", 0.53], // panel: mồ hôi
  [6.63, "pop-2.mp3", 0.5], // rất nhiều
  [8.13, "swoosh.mp3", 0.5], // photo in
  [10.09, "pop.mp3", 0.5], // thấm vào bề mặt
  [13.9, "quick-swoosh.mp3", 0.5], // panel: không gian ≠ bề mặt
  [14.53, "pop-2.mp3", 0.5], // không gian chung
  [16.01, "pop.mp3", 0.5], // bề mặt thảm
  [KY, "punch.mp3", 0.85], // CẦN LAU KỸ!
  [19.61, "punch.mp3", 0.7], // slam: lau rất nhanh
  [22.2, "quick-swoosh.mp3", 0.5], // steps panel
  [24.39, "pop-2.mp3", 0.5], // ① khăn sạch
  [26.83, "pop.mp3", 0.5], // ② vắt ẩm
  [29.67, "pop-2.mp3", 0.5], // ③ lau nhẹ
  [30.83, "swoosh.mp3", 0.5], // photo in
  [32.6, "quick-swoosh.mp3", 0.5], // panel: thấm ngược
  [NGUOC, "quick-ting.mp3", 0.53],
  [36.3, "quick-swoosh.mp3", 0.5], // checklist
  [39.07, "quick-ting.mp3", 0.53],
  [BEN, "quick-ting.mp3", 0.53],
  [43.25, "correct.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(3.4), f(4.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–3.95 s): "ĐÃ XỊT KHỬ KHUẨN / THẢM SẠCH CHƯA?" slams, gets crossed out, "VẪN PHẢI LAU!" stamp.
const HOOK_END = 3.95;
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Đã xịt khử khuẩn", color: C.white, size: 86 }]} />
    <BigText start={f(0.6)} end={f(HOOK_END)} y={224} slam lines={[{ text: "thảm sạch chưa?", color: C.accent, size: 84 }]} />
    <StrikeLine d="M120,320 L960,268" start={f(HOOK_DROP)} end={f(HOOK_END)} length={870} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Vẫn phải lau!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 150} rot={-8} size={108} />
  </>
);

// "Bởi vì trong quá trình tập luyện ... đổ rất nhiều mồ hôi"
const SweatScene: React.FC = () => {
  const s = f(4.0);
  const e = f(8.1);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "sinh-hoat/sinh-hoat_112_tham-tap-yoga-cao-su-basic-zen-2.jpg"} label="Khi tập" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Trong lúc tập</Label>
      <Label x={370} y={82} size={62} color={C.white}>đổ nhiều</Label>
      <Label x={370} y={148} size={62} color={C.accent}>mồ hôi</Label>
      <Pill text="Rất nhiều" start={f(6.63)} end={e} x={760} y={185} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// "và nó thấm lên bề mặt thảm"
const SoakPill: React.FC = () => <Pill text="Thấm vào bề mặt thảm" start={f(10.09)} end={f(11.35)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />;

// "xịt khử khuẩn ... chỉ là ở cái không gian chung thôi / nhưng trên bề mặt tấm thảm ... rất cần vệ sinh kỹ càng"
const ScopeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(13.9);
  const e = f(19.5);
  const neq = interpolate(frame, [f(16.01), f(16.01) + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
  return (
    <>
      <Panel start={s} end={e} y={G} h={270}>
        <Label x={0} y={26} size={28} color={C.dim} spacing={4} weight={800}>
          <div style={{ width: 900, textAlign: "center" }}>XỊT KHỬ KHUẨN XỬ LÝ</div>
        </Label>
        <Pill text="Không gian chung" start={f(14.53)} end={e} x={215} y={150} bg={C.white} fg={C.ink} size={32} />
        {frame >= f(16.01) && (
          <div style={{ position: "absolute", left: 428, top: 100, ...font(900, 80), fontFamily: "Arial, sans-serif", color: C.gold, transform: `scale(${neq})` }}>≠</div>
        )}
        <Pill text="Bề mặt thảm" start={f(16.01)} end={e} x={700} y={150} bg={C.pinkDeep} size={34} />
      </Panel>
      <Stamp text="Cần lau kỹ!" start={f(KY)} end={e} x={540} y={350} rot={-6} size={96} />
    </>
  );
};

// "Vệ sinh rất là nhanh thôi ... không có gì là khó khăn đâu"
const EasyScene: React.FC = () => (
  <>
    <BottomShade start={f(19.61)} end={f(22.15)} />
    <BigText
      start={f(19.61)}
      end={f(22.15)}
      y={1360}
      slam
      lines={[
        { text: "Lau rất nhanh", color: C.white, size: 100 },
        { text: "không khó!", color: C.accent, size: 108 },
      ]}
    />
  </>
);

// "lấy một cái tấm khăn sạch ... nhúng vào nước ... vắt ... lau nhẹ trên bề mặt"
const StepsScene: React.FC = () => (
  <NumberRows
    title="LAU THẢM SAU BUỔI TẬP"
    rows={[
      ["Khăn sạch", 24.39],
      ["Nhúng nước, vắt ẩm", 26.83],
      ["Lau nhẹ bề mặt", 29.67],
    ]}
    start={22.2}
    end={30.8}
    y={1300}
  />
);

// "mồ hôi ... đã thấm vào bề mặt thảm thì nó sẽ thấm ngược lại vào cái khăn này"
const WickScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(32.6);
  const e = f(36.25);
  const k = interpolate(frame, [f(NGUOC), f(NGUOC) + 14], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={40} y={30} size={30} color={C.dim} spacing={3} weight={800}>Mồ hôi trong thảm</Label>
      <div style={{ position: "absolute", left: 40, top: 190, width: 330, height: 40, borderRadius: 10, background: "#2E7D74" }} />
      {[0, 1, 2, 3, 4].map((i) => {
        const drift = (frame + i * 11) % 40;
        const x = 60 + i * 62 + k * (560 - i * 20);
        const y = 160 - k * 90 + Math.sin((drift / 40) * Math.PI * 2) * 4;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: 24,
              height: 30,
              borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%",
              background: "rgba(150,205,255,0.9)",
              boxShadow: "0 0 12px rgba(150,205,255,0.6)",
            }}
          />
        );
      })}
      <div style={{ position: "absolute", left: 600, top: 70, width: 270, height: 60, borderRadius: 12, background: "#4C8DE0", border: "3px solid rgba(255,255,255,0.6)" }} />
      <Label x={620} y={140} size={30} color={C.white} weight={800}>Khăn ẩm</Label>
      <Pill text="Thấm ngược vào khăn" start={f(NGUOC)} end={e} x={450} y={220} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// Closing checklist answers the hook.
const Closing: React.FC = () => (
  <>
    <Kicker text="Sau mỗi buổi tập" start={f(36.3)} end={VIDEO_FRAMES} y={300} color={C.gold} />
    <DoDont
      title="LAU THẢM BẰNG KHĂN ẨM"
      rows={[
        ["Thảm sạch mồ hôi", 39.07, true],
        ["Thảm bền hơn", BEN, true],
        ["Dùng lâu dài hơn", 43.25, true],
      ]}
      start={36.3}
      end={CLEAN_DURATION - 0.05}
      y={G - 40}
    />
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
      <Polaroid src={PH + "khan/khan_061_khan-lau-mo-hoi-tap-yoga.jpg"} label="Khăn Louis Yoga" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_258_tham-tap-yoga-cao-su-sunflower-2.jpg"} label="Thảm cao su" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(HOOK_END)} end={VIDEO_FRAMES} tag="Mẹo vệ sinh thảm" brand="Louis Yoga" />
        <SweatScene />
        <SoakPill />
        <ScopeScene />
        <EasyScene />
        <StepsScene />
        <WickScene />
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
