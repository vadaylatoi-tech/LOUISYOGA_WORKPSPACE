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
// LOUIS YOGA REEL — STYLE 1.  Reel "Giặt thảm và chà xát mạnh — lỗi làm thảm mất độ bám"
// (series Săn sale, video 04). Built on the approved v4 template / video 02; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — speaker sits lower than in video 01/02 (chin ≈ y 1020–1090),
// so captions go under the chin, panels on the table (yoga blocks) below. No PiP in this video.
const CAP_Y = 1200;
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 15 segments (14 cuts), alternate tight/wide. Segment 13 (55.33–55.53, 0.2 s) = segment 14.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.12, 1.26, 1.1, 1.3, 1.14, 1.24, 1.1, 1.28, 1.12, 1.24, 1.12, 1.12];
const HOOK_DROP = 1.89; // "Chà xát"
const HOOK_END = 3.92;
const BAM = 27.59; // "mất cái độ bám"
const KHONG = 30.53; // "không nên chà xát mạnh"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 2.7, 0.22], // hook drop
  [13.28, 13.9, 0.08], // "mạnh"
  [23.67, 24.3, 0.1], // "bong"
  [BAM, 28.4, 0.14], // "độ bám"
  [KHONG, 31.3, 0.1], // "không nên"
  [42.33, 43.0, 0.08], // "nhạy cảm"
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga photos only (louisyoga.vn), no outside clips.
const BROLL: Broll[] = [
  { start: 12.3, end: 14.85, film: 0, src: PH + "be-mat/be-mat_269_tham-tap-yoga-cao-su-xo-dua-aura.jpg", mode: "photo", label: "Chà xát trên bề mặt thảm" },
  { start: 36.95, end: 39.95, film: 0, src: PH + "be-mat/be-mat_076_tham-tap-yoga-cao-su-asana-25.jpg", mode: "photo", label: "Tùy chất liệu thảm" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [BAM, 7, 9, 0],
  [KHONG, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.5/s), one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [1.89, "riser-metallic.mp3", 0.45],
  [1.89, "punch.mp3", 0.95],
  [3.95, "quick-swoosh.mp3", 0.53], // panel: dính bẩn
  [7.39, "pop-2.mp3", 0.5], // làm sao cho sạch
  [9.77, "pop.mp3", 0.5], // ① mang ra giặt
  [11.92, "pop-2.mp3", 0.5], // ② dùng khăn
  [12.3, "swoosh.mp3", 0.55], // photo in
  [14.9, "quick-swoosh.mp3", 0.47], // panel: chà mạnh
  [17.9, "pop.mp3", 0.47], // hết vết bẩn?
  [19.13, "quick-swoosh.mp3", 0.5], // panel: thực chất
  [23.67, "pop-2.mp3", 0.53], // ① bong
  [24.53, "pop.mp3", 0.5], // ② mủn
  [26.3, "digital-counting-1.mp3", 0.45], // độ bám tụt
  [27.59, "punch.mp3", 0.85], // MẤT ĐỘ BÁM!
  [30.53, "punch.mp3", 0.75], // slam: không chà xát mạnh
  [33.22, "quick-swoosh.mp3", 0.5], // panel: chà mạnh ≠ sạch
  [35.54, "pop-2.mp3", 0.5],
  [36.95, "swoosh.mp3", 0.5], // photo in
  [40.83, "quick-swoosh.mp3", 0.5], // panel: cao su vs TPE
  [42.33, "pop-2.mp3", 0.5], // nhạy cảm hơn
  [44.6, "pop.mp3", 0.5], // TPE
  [48.29, "quick-ting.mp3", 0.53], // giặt được
  [48.63, "pop-2.mp3", 0.47], // riêng thảm cao su
  [51.2, "quick-swoosh.mp3", 0.5], // checklist
  [52.81, "pop-2.mp3", 0.5], // ✕ chất tẩy mạnh
  [53.69, "pop.mp3", 0.5], // ✕ chà xát mạnh
  [58.35, "correct.mp3", 0.53], // ✓ nhẹ nhàng
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(3.3), f(3.9), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–3.9 s): "GIẶT THẢM / CHÀ XÁT MẠNH?" slams twice, gets crossed out, "MẤT ĐỘ BÁM!" stamp drops.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Giặt thảm", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(HOOK_END)} y={232} slam lines={[{ text: "chà xát mạnh?", color: C.accent, size: 96 }]} />
    <StrikeLine d="M120,345 L960,290" start={f(HOOK_DROP)} end={f(HOOK_END)} length={860} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Mất độ bám!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 130} rot={-8} size={108} />
  </>
);

// "Bởi vì nó đã dính bẩn đi. Làm sao để vệ sinh được cái vết bẩn đấy, làm sao cho nó sạch".
const DirtScene: React.FC = () => {
  const s = f(3.95);
  const e = f(8.3);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "be-mat/be-mat_077_tham-tap-yoga-cao-su-asana-25.jpg"} label="Mặt thảm" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={34} size={30} color={C.dim} spacing={3} weight={800}>Thảm</Label>
      <Label x={370} y={74} size={62} color={C.white}>dính bẩn</Label>
      <Pill text="Làm sao cho sạch?" start={f(7.39)} end={e} x={620} y={168} bg={C.gold} fg={C.ink} size={36} />
    </Panel>
  );
};

// "Thường là mọi người sẽ mang ra giặt. Mang giặt xong lại dùng cái khăn".
const WashScene: React.FC = () => {
  const s = f(8.37);
  const e = f(12.25);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src={PH + "khan/khan_060_khan-lau-mo-hoi-tap-yoga.jpg"} label="Cái khăn" x={30} y={25} w={300} h={220} start={s} end={e} />
      <Label x={370} y={30} size={30} color={C.dim} spacing={3} weight={800}>Thường thì</Label>
      <Pill text="① Mang ra giặt" start={f(9.77)} end={e} x={610} y={80} bg={C.white} fg={C.ink} size={40} />
      <Pill text="② Lấy khăn chà" start={f(11.92)} end={e} x={610} y={166} bg={C.pinkDeep} size={40} />
    </Panel>
  );
};

// "...ở trên cái bề mặt, trên cái vết bẩn đấy. Làm sao để cho nó hết được cái vết bẩn ấy" — towel rubs a stain.
const RubScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(14.9);
  const e = f(19.0);
  const t = frame - s;
  const tx = Math.sin(t / 2.2) * 70; // fast back-and-forth rub
  const stain = interpolate(frame, [s, f(18.6)], [0.9, 0.35], clamp);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <div style={{ position: "absolute", left: 30, top: 25, width: 360, height: 220, borderRadius: 18, background: "linear-gradient(135deg,#E9A5BE,#D97FA3)", overflow: "hidden", border: "3px solid rgba(255,255,255,0.85)" }}>
        <div style={{ position: "absolute", left: 120, top: 70, width: 120, height: 80, borderRadius: "50%", background: `rgba(95,62,40,${stain})`, filter: "blur(6px)" }} />
        <div
          style={{
            position: "absolute",
            left: 110 + tx,
            top: 50,
            width: 140,
            height: 120,
            borderRadius: 16,
            background: "repeating-linear-gradient(90deg,#F6F0F3 0 8px,#E8DDE3 8px 14px)",
            boxShadow: "0 8px 18px rgba(0,0,0,0.35)",
            transform: `rotate(${tx / 12}deg)`,
          }}
        />
      </div>
      <Label x={420} y={34} size={30} color={C.dim} spacing={3} weight={800}>Chà thật mạnh</Label>
      <Label x={420} y={76} size={56} color={C.white}>cho hết</Label>
      <Label x={420} y={140} size={56} color={C.accent}>vết bẩn</Label>
      <Pill text="?" start={f(17.9)} end={e} x={790} y={140} bg={C.gold} fg={C.ink} size={48} />
    </Panel>
  );
};

// "Thì thực chất là ... dễ làm bị bong với cả bị mủn ... rất là dễ làm bị mất cái độ bám tại cái vị trí mà mình chà xát".
const HarmScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(19.13);
  const e = f(29.1);
  const bar = interpolate(frame, [f(26.3), f(27.5)], [1, 0.25], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const red = interpolate(frame, [f(26.3), f(27.5)], [0, 1], clamp);
  return (
    <>
      <Kicker text="Thực chất là" start={s} end={f(22.6)} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <Label x={50} y={26} size={30} color={C.dim} spacing={3} weight={800}>Chỗ bị chà xát mạnh</Label>
        <Pill text="① Bong tróc" start={f(23.67)} end={e} x={220} y={80} bg={C.white} fg={C.ink} size={38} />
        <Pill text="② Mủn" start={f(24.53)} end={e} x={520} y={80} bg={C.gold} fg={C.ink} size={38} />
        <Label x={50} y={166} size={26} color={C.dim} spacing={3} weight={800}>Độ bám</Label>
        <div style={{ position: "absolute", left: 50, top: 204, width: 800, height: 40, borderRadius: 12, background: "rgba(255,255,255,0.12)" }}>
          <div
            style={{
              width: 800 * bar,
              height: 40,
              borderRadius: 12,
              background: `linear-gradient(90deg, ${C.accent}, rgba(${Math.round(226 + 29 * red)},${Math.round(49 + 40 * red)},${Math.round(139 - 80 * red)},1))`,
            }}
          />
        </div>
        <Stamp text="Mất độ bám!" start={f(BAM)} end={e} x={640} y={170} rot={-8} size={74} />
      </Panel>
    </>
  );
};

// "Nên là mọi người lưu ý là mình không nên chà xát mạnh ở trên bề mặt thảm nhé" — main advice slams.
const AdviceScene: React.FC = () => (
  <>
    <TopShade start={f(KHONG)} end={f(33.1)} />
    <BigText
      start={f(KHONG)}
      end={f(33.1)}
      y={200}
      slam
      lines={[
        { text: "Không chà xát", color: C.white, size: 96 },
        { text: "mạnh tay", color: C.accent, size: 112 },
      ]}
    />
  </>
);

// "Không phải lúc nào mình chà xát mạnh thì nó cũng sạch đâu".
const NotCleanScene: React.FC = () => {
  const s = f(33.22);
  const e = f(36.85);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <div style={{ position: "absolute", left: 0, top: 30, width: 900, textAlign: "center", ...font(900, 64), color: C.white }}>
        Chà mạnh <span style={{ color: C.gold }}>≠</span> <span style={{ color: C.accent }}>sạch hơn</span>
      </div>
      <Pill text="✕ Không phải lúc nào cũng sạch" start={f(35.54)} end={e} x={450} y={150} bg={C.white} fg={C.ink} size={36} />
    </Panel>
  );
};

// "Cái thảm cao su thì nó sẽ hơi nhạy cảm hơn ... TPE thì nó sẽ dễ hơn ... TPE thì cũng có thể là giặt được".
const MaterialScene: React.FC = () => {
  const s = f(40.83);
  const e = f(51.1);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src="brand/rubber_rolls.jpg" label="Cao su" x={24} y={20} w={250} h={160} start={s} end={e} highlight />
      <Pill text="Nhạy cảm hơn" start={f(42.33)} end={e} x={180} y={194} bg={C.pinkDeep} size={28} />
      <div style={{ position: "absolute", left: 0, top: 70, width: 900, textAlign: "center", ...font(900, 64), color: C.gold }}>VS</div>
      <TpeCard s={f(44.6)} e={e} />
      <Pill text="✓ Giặt được" start={f(48.29)} end={e} x={751} y={194} bg={C.gold} fg={C.ink} size={30} />
    </Panel>
  );
};
const TpeCard: React.FC<{ s: number; e: number }> = ({ s, e }) => {
  const frame = useCurrentFrame();
  if (frame < s) return null;
  const p = interpolate(frame, [s, s + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 900, height: 270, transform: `translateX(${(1 - p) * 120}px)`, opacity: p }}>
      <PhotoCard src={PH + "tu-the/tu-the_291_tham-tap-yoga-tpe-dinh-tuyen-tpe9.jpg"} label="TPE" x={626} y={20} w={250} h={160} start={s} end={e} />
    </div>
  );
};

// Closing checklist (answers the hook): no strong cleaners, no hard rubbing → gentle cleaning.
const Closing: React.FC = () => (
  <>
    <Kicker text="Riêng thảm cao su" start={f(48.63)} end={f(51.4)} y={300} color={C.gold} />
    <DoDont
      title="LÀM SẠCH THẢM CAO SU"
      rows={[
        ["Chất tẩy rửa mạnh", 52.81, false],
        ["Chà xát mạnh", 53.69, false],
        ["Làm sạch nhẹ nhàng", 58.35, true],
      ]}
      start={51.2}
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
      <Polaroid src={PH + "be-mat/be-mat_075_tham-tap-yoga-cao-su-asana-25.jpg"} label="Thảm cao su" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "khan/khan_061_khan-lau-mo-hoi-tap-yoga.jpg"} label="Louis Yoga" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <DirtScene />
        <WashScene />
        <RubScene />
        <HarmScene />
        <AdviceScene />
        <NotCleanScene />
        <MaterialScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={HOOK_END - 0.05} until={CLEAN_DURATION} />
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
