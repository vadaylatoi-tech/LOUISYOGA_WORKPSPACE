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
// LOUIS YOGA REEL — STYLE 1.  Reel "Khi nào nên thay thảm mới"
// (series Săn sale, video 08). Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — same set as video 01/02/06 (shelf behind, foam blocks / mats on the table below).
const CAP_Y = 1140; // she sits higher than in 06: chin ≈ 1040–1060 at tight zoom (measured on stills)
const G = 1390;

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";
const PH = "louis-photos/";

// ▼ EDIT ▼ camera: 13 segments (12 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.12, 1.26, 1.1, 1.22, 1.14, 1.28, 1.12, 1.24, 1.1, 1.26];
const HOOK_DROP = 4.7; // "không (phải là hoàn toàn ... vệ sinh)"
const HOOK_END = 5.4;
const TIME_TO = 10.13; // "(nên) thay thảm (rồi đấy)"
const NEW_MAT = 33.11; // "(nên) thay thảm mới"
const NOT_GONE = 47.73; // "(nó sẽ) hết (luôn)" — không phải vệ sinh là hết
const END_SLAM = 53.41; // "nên thay thảm mới nhá"
const PUNCHES: Punch[] = [
  [HOOK_DROP, 5.4, 0.22],
  [TIME_TO, 10.9, 0.12],
  [20.51, 21.2, 0.08], // "mủn"
  [NEW_MAT, 33.7, 0.1],
  [NOT_GONE, 48.5, 0.1],
  [END_SLAM, 54.3, 0.12],
];
const FOCUS: Focus[] = [];

// ▼ EDIT ▼ cutaways — Louis Yoga brand film + louisyoga.vn photos only, no outside clips.
const BROLL: Broll[] = [
  { start: 13.97, end: 15.55, film: 58.0, mode: "fit", label: "Tập hằng ngày" },
  { start: 21.63, end: 23.95, film: 60.0, cx: 960, mode: "crop", label: "Chỗ tay chân ma sát nhiều" },
  { start: 40.3, end: 42.4, film: 0, src: PH + "tu-the/tu-the_243_tham-tap-yoga-cao-su-queen.jpg", mode: "photo", label: "Hiệu quả tập luyện tốt hơn" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [2.85, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [TIME_TO, 6, 8, 0],
  [NOT_GONE, 6, 8, 0],
  [END_SLAM, 6, 8, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.5/s), one sound per beat. Times written as numbers (measure_sfx.py).
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [2.85, "pop-2.mp3", 0.59], // "bị mủn?"
  [4.7, "riser-metallic.mp3", 0.45],
  [4.7, "punch.mp3", 0.95], // strike + stamp
  [8.84, "quick-swoosh.mp3", 0.5], // "Đến lúc"
  [10.13, "punch.mp3", 0.8], // "thay thảm mới"
  [11.2, "quick-swoosh.mp3", 0.47], // panel: dùng lâu
  [13.53, "pop-2.mp3", 0.5], // "đã lâu"
  [13.97, "swoosh.mp3", 0.5], // film in
  [15.75, "pop-2.mp3", 0.5], // ① tập hằng ngày
  [16.45, "pop.mp3", 0.47], // ② ma sát
  [19.8, "quick-swoosh.mp3", 0.47], // panel: thảm sẽ bị
  [20.51, "pop-2.mp3", 0.5], // mủn
  [21.25, "pop.mp3", 0.47], // bong tróc
  [21.63, "swoosh.mp3", 0.5], // film in
  [27.6, "quick-swoosh.mp3", 0.47], // rows: nếu thảm đã
  [28.89, "pop.mp3", 0.47], // ✕ mủn
  [29.65, "pop-2.mp3", 0.5], // ✕ bong tróc
  [30.3, "quick-swoosh.mp3", 0.47], // panel: giải pháp
  [33.11, "punch.mp3", 0.75], // stamp THAY THẢM MỚI
  [33.8, "quick-swoosh.mp3", 0.47], // rows
  [36.09, "pop-2.mp3", 0.5], // ① sức khỏe
  [38.67, "pop.mp3", 0.47], // ② tập luyện
  [40.3, "swoosh.mp3", 0.5], // photo in
  [43.92, "pop-2.mp3", 0.5], // "Bị bong, bị mủn"
  [45.62, "pop.mp3", 0.47], // "vệ sinh là hết?"
  [47.73, "punch.mp3", 0.8], // KHÔNG HẾT ĐÂU
  [48.65, "quick-swoosh.mp3", 0.5], // checklist
  [49.83, "quick-ting.mp3", 0.53],
  [51.37, "quick-ting.mp3", 0.53],
  [52.45, "correct.mp3", 0.45],
  [53.41, "punch.mp3", 0.8], // NÊN THAY THẢM MỚI
  [VIDEO_FRAMES / FPS + 0.1, "punch.mp3", 0.7],
  [VIDEO_FRAMES / FPS + 0.35, "camera-shutter.mp3", 0.53],
  [VIDEO_FRAMES / FPS + 0.7, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(5.2), f(5.8), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
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

// Hook (0–5.4 s): "THẢM MẤT ĐỘ BÁM / HAY BỊ MỦN?" → "do vệ sinh?" crossed out → stamp "KHÔNG HẲN!".
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(HOOK_END)} />
    <BigText start={0} end={f(HOOK_END)} y={120} slam lines={[{ text: "Thảm mất độ bám", color: C.white, size: 88 }]} />
    <BigText start={f(2.85)} end={f(HOOK_END)} y={226} slam lines={[{ text: "hay bị mủn?", color: C.accent, size: 112 }]} />
    <BigText start={f(3.55)} end={f(HOOK_END)} y={372} lines={[{ text: "Do vệ sinh?", color: C.white, size: 76 }]} />
    <StrikeLine d="M260,430 L820,410" start={f(HOOK_DROP)} end={f(HOOK_END)} length={600} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(HOOK_END)} />
    <Stamp text="Không hẳn!" start={f(HOOK_DROP)} end={f(HOOK_END)} x={540} y={G + 130} rot={-8} size={104} />
  </>
);

// "Đôi khi là nó cũng là đến cái thời gian mà mình nên thay thảm rồi đấy mọi người".
const TimeToChange: React.FC = () => (
  <>
    <TopShade start={f(8.84)} end={f(11.1)} />
    <BigText start={f(8.84)} end={f(11.1)} y={190} slam lines={[{ text: "Đến lúc", color: C.white, size: 100 }]} />
    <BigText start={f(TIME_TO)} end={f(11.1)} y={310} slam lines={[{ text: "thay thảm mới", color: C.accent, size: 104 }]} />
  </>
);

// "Bởi vì là khi mà mọi người sử dụng một cái thảm mà nó lâu" → film "tập hằng ngày" → 2 rows.
const WhyScene: React.FC = () => {
  const s = f(11.2);
  const e = f(13.95);
  return (
    <>
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "cuon-tham/cuon-tham_268_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Thảm tập" x={30} y={25} w={300} h={220} start={s} end={e} />
        <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Bởi vì khi</Label>
        <Label x={370} y={80} size={56} color={C.white}>dùng thảm</Label>
        <Pill text="Đã lâu" start={f(13.53)} end={e} x={760} y={190} bg={C.pinkDeep} size={44} />
      </Panel>
      <NumberRows
        title="NHẤT LÀ KHI"
        rows={[
          ["Tập hằng ngày", 15.75],
          ["Ma sát nhiều", 16.45],
        ]}
        start={15.6}
        end={18.0}
        y={G - 40}
      />
    </>
  );
};

// "Thì sau một thời gian dài nó sẽ có cái tình trạng là bị mủn và bị bong tróc".
const WearScene: React.FC = () => {
  const s = f(18.1);
  const e = f(21.6);
  return (
    <>
      <Kicker text="Sau một thời gian dài" start={s} end={e} y={300} color={C.gold} />
      <Panel start={f(19.8)} end={e} y={G} h={270}>
        <Label x={0} y={30} size={34} color={C.dim} spacing={4} weight={800}>
          <div style={{ width: 900, textAlign: "center" }}>Thảm sẽ bị</div>
        </Label>
        <Pill text="Mủn" start={f(20.51)} end={e} x={270} y={150} bg={C.white} fg={C.ink} size={60} />
        <Pill text="Bong tróc" start={f(21.25)} end={e} x={630} y={150} bg={C.pinkDeep} size={60} />
      </Panel>
    </>
  );
};

// "Nếu như mà cái thảm của mình mà nó đã có cái tình trạng gọi là bị mủn với cả bị bong tróc ấy".
const SignScene: React.FC = () => (
  <NumberRows
    title="NẾU THẢM ĐÃ"
    rows={[
      ["Bị mủn", 28.89],
      ["Bị bong tróc", 29.65],
    ]}
    start={27.6}
    end={30.15}
    y={G - 40}
  />
);

// "Thì cái giải pháp tốt nhất là mình nên thay thảm mới".
const SolutionScene: React.FC = () => {
  const s = f(30.3);
  const e = f(33.75);
  return (
    <>
      <Kicker text="Giải pháp tốt nhất" start={s} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src={PH + "cuon-tham/cuon-tham_267_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Thảm mới" x={30} y={25} w={300} h={220} start={s} end={e} />
        <Label x={370} y={36} size={30} color={C.dim} spacing={3} weight={800}>Mủn, bong tróc</Label>
        <Label x={370} y={78} size={56} color={C.white}>thì nên</Label>
        <Stamp text="Thay thảm mới" start={f(NEW_MAT)} end={e} x={620} y={190} rot={-5} size={50} />
      </Panel>
    </>
  );
};

// "Để thứ nhất là đảm bảo được về cái sức khỏe, thứ hai là hỗ trợ ... hiệu quả tập luyện tốt hơn".
const BenefitScene: React.FC = () => (
  <NumberRows
    title="THAY THẢM MỚI ĐỂ"
    rows={[
      ["Đảm bảo sức khỏe", 36.09],
      ["Tập hiệu quả hơn", 38.67],
    ]}
    start={33.8}
    end={40.25}
    y={G - 40}
  />
);

// "Chứ không phải là nó bị bong hay là nó bị mủn, mọi người vệ sinh là nó sẽ sạch lại, nó sẽ hết luôn".
const MythScene: React.FC = () => (
  <>
    <Kicker text="Chứ không phải là…" start={f(42.5)} end={f(43.9)} y={300} color={C.gold} />
    <TopShade start={f(43.92)} end={f(48.6)} />
    <BigText start={f(43.92)} end={f(48.6)} y={190} slam lines={[{ text: "Bị bong, bị mủn", color: C.white, size: 84 }]} />
    <BigText start={f(45.62)} end={f(48.6)} y={300} slam lines={[{ text: "vệ sinh là hết?", color: C.accent, size: 92 }]} />
    <StrikeLine d="M150,360 L930,340" start={f(NOT_GONE)} end={f(48.6)} length={800} />
    <BottomShade start={f(NOT_GONE) - 2} end={f(48.6)} />
    <Stamp text="Không hết đâu!" start={f(NOT_GONE)} end={f(48.6)} x={540} y={G + 130} rot={-6} size={84} />
  </>
);

// Closing checklist answers the hook: "Nếu dùng đã lâu rồi mà nó mất độ bám hay bị bong tróc thì nên thay thảm mới".
const Closing: React.FC = () => (
  <>
    <DoDont
      title="KHI NÀO NÊN THAY THẢM?"
      rows={[
        ["Dùng đã lâu", 49.83, true],
        ["Mất độ bám", 51.37, true],
        ["Bong tróc, mủn", 52.45, true],
      ]}
      start={48.65}
      end={CLEAN_DURATION - 0.05}
      y={G - 40}
    />
    <TopShade start={f(END_SLAM)} end={VIDEO_FRAMES} />
    <BigText start={f(END_SLAM)} end={VIDEO_FRAMES} y={210} slam lines={[{ text: "Thay thảm mới!", color: C.accent, size: 100 }]} />
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
      <Polaroid src={PH + "cuon-tham/cuon-tham_261_tham-tap-yoga-cao-su-xo-dua-aura.jpg"} label="Thảm Aura" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src={PH + "tu-the/tu-the_196_tham-tap-yoga-cao-su-cao-cap-lilium.jpg"} label="Thảm Lilium" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <TimeToChange />
        <WhyScene />
        <WearScene />
        <SignScene />
        <SolutionScene />
        <BenefitScene />
        <MythScene />
        <Closing />
        <Captions lines={CAPTIONS} y={CAP_Y} from={3.55} until={CLEAN_DURATION} />
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
