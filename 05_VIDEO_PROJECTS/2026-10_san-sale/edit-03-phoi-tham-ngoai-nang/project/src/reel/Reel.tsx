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
// LOUIS YOGA REEL — STYLE 1.  Reel "Phơi thảm ngoài nắng cho nhanh khô — sai lầm"
// (series Săn sale, video 03). Built on the approved v4 template / video 02; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same set as video 01/02 (shelf behind, foam blocks / mats on the table below).
// Standing (0–10.7 s, 26.4 s–end, holding a purple mat) and seated (10.7–26.4 s) takes alternate.
const CAP_Y = 1030;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 8 segments (7 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.12, 1.26, 1.1, 1.22, 1.14];
const HOOK_DROP = 1.7;
const HARM = 18.15; // "bề mặt thảm"
const DUR = 25.23; // "độ bền"
const SLAM = 31.32; // "Phơi ở trong bóng mát"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.5, 0.22], // hook drop
  [5.84, 6.4, 0.08], // "thảm cao su"
  [8.22, 8.62, 0.1], // "bóng mát"
  [14.53, 15.1, 0.08], // "phơi nắng"
  [HARM, 18.78, 0.12], // "bề mặt thảm"
  [DUR, 26.0, 0.14], // "độ bền"
  [32.0, 32.6, 0.1], // "bóng mát"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga material only (louisyoga.vn photo + brand film), no outside clips.
const BROLL: Broll[] = [
  { start: 12.25, end: 13.88, film: 0, src: PH + "be-mat/be-mat_075_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "Chất liệu cao su" },
  { start: 19.8, end: 21.85, film: 50.0, cx: 620, mode: "crop", label: "Dưới ánh nắng" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [HARM, 6, 8, 0],
  [DUR, 7, 9, 0],
  [SLAM, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density, one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [4.32, "quick-swoosh.mp3", 0.5], // panel: không nha
  [5.84, "pop.mp3", 0.47], // "cao su"
  [7.34, "quick-ting.mp3", 0.53], // ✓ bóng mát
  [8.64, "quick-swoosh.mp3", 0.47], // panel: sun
  [9.86, "pop-2.mp3", 0.5], // ✕ on the sun
  [12.25, "swoosh.mp3", 0.5], // photo in
  [14.53, "pop-2.mp3", 0.5], // ① phơi nắng
  [16.33, "pop.mp3", 0.5], // ② tẩy rửa mạnh
  [HARM, "punch.mp3", 0.8], // HẠI BỀ MẶT
  [19.8, "swoosh.mp3", 0.5], // film in
  [23.25, "pop-2.mp3", 0.5], // vô tình
  [23.95, "quick-swoosh.mp3", 0.47], // panel: độ bền
  [DUR, "punch.mp3", 0.85], // GIẢM ĐỘ BỀN
  [26.45, "quick-swoosh.mp3", 0.47], // panel: tập xong
  [28.15, "pop.mp3", 0.47], // thảm còn ướt
  [SLAM, "punch.mp3", 0.75], // slam: phơi trong bóng mát
  [32.0, "quick-ting.mp3", 0.53], // ✓ bóng mát
  [33.18, "pop-2.mp3", 0.5], // ✕ nắng trực tiếp
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

// Hook (0–2.9 s): "PHƠI NẮNG / CHO NHANH KHÔ?" slams twice, gets crossed out, "SAI LẦM!" stamp drops.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(2.95)} />
    <BigText start={0} end={f(2.95)} y={120} slam lines={[{ text: "Phơi nắng", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(2.95)} y={232} slam lines={[{ text: "cho nhanh khô?", color: C.accent, size: 94 }]} />
    <StrikeLine d="M120,345 L960,290" start={f(HOOK_DROP)} end={f(2.95)} length={860} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.9)} />
    <Stamp text="Sai lầm!" start={f(HOOK_DROP)} end={f(2.9)} x={540} y={G + 130} rot={-8} size={120} />
  </>
);

// "Nhưng mà không nha, đối với dòng thảm cao su thì phơi ở trong bóng mát".
const RubberScene: React.FC = () => {
  const s = f(4.32);
  const e = f(7.3);
  const frame = useCurrentFrame();
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "be-mat/be-mat_076_tham-tap-yoga-cao-su-asana-25.jpg"} label="Thảm cao su" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Với dòng</Label>
      <Label x={360} y={82} size={58} color={C.white}>Thảm</Label>
      {frame >= f(5.84) && (
        <Label x={360} y={146} size={58} color={C.accent}>
          cao su
        </Label>
      )}
      <Pill text="✕ Không nha" start={s} end={e} x={740} y={48} bg={C.white} fg={C.ink} size={34} />
    </Panel>
  );
};

// "Không phơi trực tiếp dưới ánh nắng mặt trời" — a sun gets crossed out.
const SunScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(8.64);
  const e = f(10.7);
  const x = f(9.86);
  const cross = interpolate(frame, [x, x + 6], [0, 1], clamp);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <div style={{ position: "absolute", left: 60, top: 25, width: 220, height: 220, transform: `rotate(${(frame - s) * 1.5}deg)` }}>
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            style={{ position: "absolute", left: 104, top: 0, width: 12, height: 40, borderRadius: 6, background: C.gold, transformOrigin: "6px 110px", transform: `rotate(${i * 30}deg)` }}
          />
        ))}
        <div style={{ position: "absolute", left: 45, top: 45, width: 130, height: 130, borderRadius: 99, background: C.gold, boxShadow: `0 0 40px ${C.gold}` }} />
      </div>
      {cross > 0 && (
        <svg width={260} height={260} style={{ position: "absolute", left: 40, top: 5 }}>
          <path d={`M30,30 L${30 + 200 * cross},${30 + 200 * cross}`} stroke={C.accent} strokeWidth={22} strokeLinecap="round" />
          <path d={`M230,30 L${230 - 200 * cross},${30 + 200 * cross}`} stroke={C.accent} strokeWidth={22} strokeLinecap="round" />
        </svg>
      )}
      <Label x={340} y={40} size={30} color={C.dim} spacing={3} weight={800}>Không phơi</Label>
      <Label x={340} y={82} size={62} color={C.white}>nắng</Label>
      <Label x={340} y={146} size={62} color={C.accent}>trực tiếp</Label>
    </Panel>
  );
};

// "phơi nắng hay sử dụng chất tẩy rửa mạnh".
const CauseScene: React.FC = () => {
  const s = f(13.93);
  const e = f(16.75);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={0} y={26} size={30} color={C.dim} spacing={4} weight={800}>
        <div style={{ width: 900, textAlign: "center" }}>Thảm cao su sợ</div>
      </Label>
      <Pill text="① Phơi nắng" start={f(14.53)} end={e} x={450} y={100} bg={C.white} fg={C.ink} size={42} />
      <Pill text="② Chất tẩy rửa mạnh" start={f(16.33)} end={e} x={450} y={190} bg={C.pinkDeep} size={42} />
    </Panel>
  );
};

// "Nó sẽ ảnh hưởng rất là nhiều đến cái bề mặt thảm".
const SurfaceScene: React.FC = () => {
  const s = f(16.77);
  const e = f(19.75);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "be-mat/be-mat_269_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Bề mặt thảm" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Ảnh hưởng</Label>
      <Label x={370} y={82} size={62} color={C.white}>rất nhiều</Label>
      <Stamp text="Hại bề mặt!" start={f(HARM)} end={e} x={660} y={205} rot={-7} size={66} />
    </Panel>
  );
};

// "làm giảm cái độ bền thảm của mình" — durability bar drops, stamp.
const DurabilityScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(23.95);
  const e = f(26.38);
  const bar = interpolate(frame, [f(24.6), f(25.5)], [1, 0.3], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Label x={50} y={40} size={30} color={C.dim} spacing={3} weight={800}>Độ bền thảm</Label>
      <div style={{ position: "absolute", left: 50, top: 92, width: 800, height: 46, borderRadius: 12, background: "rgba(255,255,255,0.12)" }}>
        <div style={{ width: 800 * bar, height: 46, borderRadius: 12, background: `linear-gradient(90deg, ${C.accent}, ${C.pinkDeep})` }} />
      </div>
      <Stamp text="Giảm độ bền!" start={f(DUR)} end={e} x={450} y={205} rot={-6} size={76} />
    </Panel>
  );
};

// "Tập xong thảm còn ướt → phơi lên như em này" — standing take, shady-spot photo.
const WetScene: React.FC = () => {
  const s = f(26.45);
  const e = f(31.25);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "sinh-hoat/sinh-hoat_265_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Để nơi thoáng" x={30} y={25} w={300} h={220} start={f(28.83)} end={e} />
      <Label x={370} y={40} size={30} color={C.dim} spacing={3} weight={800}>Tập xong</Label>
      <Pill text="Thảm còn ướt" start={f(28.15)} end={e} x={600} y={120} bg={C.pinkDeep} size={44} />
      <Pill text="→ phơi lên" start={f(30.24)} end={e} x={600} y={205} bg={C.white} fg={C.ink} size={38} />
    </Panel>
  );
};

// Closing: advice slams, Do/Don't answers the hook.
const Closing: React.FC = () => (
  <>
    <TopShade start={f(SLAM)} end={f(32.95)} />
    <BigText
      start={f(SLAM)}
      end={f(32.95)}
      y={170}
      slam
      lines={[
        { text: "Phơi trong", color: C.white, size: 100 },
        { text: "bóng mát", color: C.accent, size: 112 },
      ]}
    />
    <DoDont
      title="PHƠI THẢM CAO SU"
      rows={[
        ["Phơi trong bóng mát", 32.0, true],
        ["Nắng trực tiếp", 33.18, false],
      ]}
      start={SLAM}
      end={CLEAN_DURATION - 0.05}
      y={G - 20}
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
      <Kicker text="xem thêm mẹo bảo quản thảm" start={s + 10} end={DURATION + 1} y={360} color={C.gold} />
      <Polaroid src={PH + "sinh-hoat/sinh-hoat_258_tham-tap-yoga-cao-su-sunflower-2.jpg"} label="Thảm cao su" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "be-mat/be-mat_076_tham-tap-yoga-cao-su-asana-25.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(2.95)} end={f(SLAM)} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <SeriesTag start={f(32.95)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <RubberScene />
        <Pill text="✓ Phơi trong bóng mát" start={f(7.34)} end={f(8.6)} x={W / 2} y={G + 110} bg={C.gold} fg={C.ink} size={46} />
        <SunScene />
        <Kicker text="Khi phơi nắng…" start={f(10.75)} end={f(12.2)} y={300} color={C.gold} />
        <CauseScene />
        <SurfaceScene />
        <Pill text="Lý do vô tình" start={f(23.25)} end={f(23.92)} x={W / 2} y={G + 110} bg={C.pinkDeep} size={46} />
        <DurabilityScene />
        <WetScene />
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
