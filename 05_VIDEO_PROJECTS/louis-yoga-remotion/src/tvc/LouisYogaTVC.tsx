import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { MONTSERRAT, useMontserrat } from "../shared/useMontserrat";

// Footage: segments cut from Louis Yoga's own brand film
// ("Video Hero - Trang chủ.mp4", also published on youtube.com/@louisyoga as AFo_DvpQWf0).
// Each clip in public/tvc/clips is a silent 1920x1080 @30fps copy; the original file is untouched.
// Colors follow the Louis Yoga website design system (docs/LOUIS_YOGA_EDIT_GUIDE.md).
const COLORS = {
  pink: "#d72182",
  wine: "#4a202c",
  white: "#ffffff",
};

const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;
const SRC_W = 1920;
const SRC_H = 1080;

type Shot = {
  file: string;
  frames: number;
  // Horizontal center of the 9:16 window, in source pixels (0..1920).
  centerX: number;
  // End scale of the slow push-in; 1 = static (used where the head sits near the top edge).
  push: number;
  // Show a wider 760px-wide slice over a blurred copy instead of filling the height,
  // so wide content (the logo wordmark) keeps clear of the frame edges.
  fit?: boolean;
  // Source time in the brand film, kept for traceability only.
  source: string;
};

const SHOTS: Shot[] = [
  { file: "s02.mp4", frames: 72, centerX: 620, push: 1.05, source: "50.6–53.0s window light, corner of mat" },
  { file: "s01.mp4", frames: 84, centerX: 825, push: 1, source: "8.0–10.8s pigeon pose, green mat" },
  { file: "s03.mp4", frames: 90, centerX: 940, push: 1.03, source: "13.0–16.0s seated, green mat" },
  { file: "s04.mp4", frames: 84, centerX: 1150, push: 1.05, source: "42.3–45.3s hand over mat surface" },
  { file: "s05.mp4", frames: 90, centerX: 580, push: 1.03, source: "18.0–21.0s headstand, blue mat" },
  { file: "s06.mp4", frames: 72, centerX: 820, push: 1.05, source: "46.5–49.0s lotus motif, blue mat" },
  { file: "s07.mp4", frames: 84, centerX: 320, push: 1.03, source: "62.8–65.8s supine pose, green mat" },
  { file: "s08.mp4", frames: 105, centerX: 1180, push: 1.03, source: "71.0–74.5s seated, eyes closed" },
  { file: "s09.mp4", frames: 36, centerX: 960, push: 1.03, source: "40.5–41.7s rolled blue mat, LOUISYOGA mark" },
  // The source logo is fully formed from frame ~50 and starts fading after frame ~95.
  { file: "s10.mp4", frames: 96, centerX: 960, push: 1, fit: true, source: "89.0–92.2s brand logo animation" },
];

const STARTS = SHOTS.reduce<number[]>(
  (acc, shot, i) => [...acc, i === 0 ? 0 : acc[i - 1] + SHOTS[i - 1].frames],
  [],
);
const DURATION = SHOTS.reduce((sum, shot) => sum + shot.frames, 0);
const END_CARD_START = STARTS[SHOTS.length - 1];

// Scale the 16:9 source so its height fills the 9:16 frame, then slide it so centerX lands mid-frame.
const SCALE = HEIGHT / SRC_H;

const ShotLayer: React.FC<{ shot: Shot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  // Slow push-in within each shot, one continuous interpolate per shot.
  const push = interpolate(frame, [0, shot.frames], [1, shot.push], {
    extrapolateRight: "clamp",
  });
  const src = staticFile(`tvc/clips/${shot.file}`);
  const scale = shot.fit ? WIDTH / 760 : SCALE;
  const width = SRC_W * scale;
  const height = SRC_H * scale;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      {shot.fit ? (
        <OffthreadVideo
          src={src}
          muted
          style={{
            position: "absolute",
            top: 0,
            left: WIDTH / 2 - shot.centerX * SCALE,
            width: SRC_W * SCALE,
            height: HEIGHT,
            filter: "blur(40px)",
          }}
        />
      ) : null}
      <AbsoluteFill style={{ transform: `scale(${push})` }}>
        <OffthreadVideo
          src={src}
          muted
          style={{
            position: "absolute",
            top: (HEIGHT - height) / 2,
            left: WIDTH / 2 - shot.centerX * scale,
            width,
            height,
            // Feather the top/bottom edges into the blurred copy behind it.
            maskImage: shot.fit
              ? "linear-gradient(to bottom, transparent 0%, black 14%, black 86%, transparent 100%)"
              : undefined,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Caption: React.FC<{
  lines: string[];
  color: string;
  top: number;
  durationInFrames: number;
}> = ({ lines, color, top, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 10, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const shadow =
    color === COLORS.white
      ? "0 2px 18px rgba(0,0,0,0.45)"
      : "0 0 24px rgba(255,255,255,0.85)";
  return (
    <div
      style={{
        position: "absolute",
        top,
        // Keep clear of the right-hand action buttons on Reels.
        left: 80,
        right: 160,
        textAlign: "center",
        fontFamily: MONTSERRAT,
        fontWeight: 600,
        fontSize: 74,
        lineHeight: 1.22,
        color,
        textShadow: shadow,
        opacity: fadeOut,
      }}
    >
      {lines.map((line, i) => {
        const progress = spring({
          frame: frame - i * 6,
          fps,
          config: { damping: 200 },
        });
        return (
          <div
            key={line}
            style={{
              whiteSpace: "nowrap",
              opacity: progress,
              transform: `translateY(${(1 - progress) * 30}px)`,
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};

const CallToAction: React.FC = () => {
  const frame = useCurrentFrame();
  const appear = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        position: "absolute",
        top: 1360,
        left: 80,
        right: 160,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 28,
        opacity: appear,
        transform: `translateY(${(1 - appear) * 24}px)`,
      }}
    >
      <div
        style={{
          fontFamily: MONTSERRAT,
          fontWeight: 700,
          fontSize: 66,
          color: COLORS.wine,
          whiteSpace: "nowrap",
        }}
      >
        Khám phá Louis Yoga
      </div>
      <div
        style={{
          width: 200 * appear,
          height: 6,
          borderRadius: 3,
          backgroundColor: COLORS.pink,
        }}
      />
    </div>
  );
};

// Brief white flash-fade into the logo card; the logo footage itself has a light background.
const WhiteDip: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 8, 18], [0, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ backgroundColor: "#fff", opacity }} />;
};

const LouisYogaTVC: React.FC = () => {
  useMontserrat();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {SHOTS.map((shot, i) => (
        <Sequence
          key={shot.file}
          from={STARTS[i]}
          durationInFrames={shot.frames}
        >
          <ShotLayer shot={shot} />
        </Sequence>
      ))}

      {/* Captions sit only on close-ups of the mat, so they never cover a face. */}
      <Sequence from={4} durationInFrames={68}>
        <Caption
          lines={["Một khoảng nhỏ", "cho riêng mình"]}
          color={COLORS.white}
          top={300}
          durationInFrames={68}
        />
      </Sequence>
      <Sequence from={STARTS[3] + 6} durationInFrames={78}>
        <Caption
          lines={["Bắt đầu", "từ tấm thảm"]}
          color={COLORS.white}
          top={300}
          durationInFrames={78}
        />
      </Sequence>
      <Sequence from={STARTS[5] + 4} durationInFrames={68}>
        <Caption
          lines={["Chậm lại", "một chút"]}
          color={COLORS.white}
          top={300}
          durationInFrames={68}
        />
      </Sequence>

      <Sequence from={END_CARD_START - 8} durationInFrames={18}>
        <WhiteDip />
      </Sequence>
      <Sequence from={END_CARD_START} durationInFrames={SHOTS[9].frames}>
        <CallToAction />
      </Sequence>
    </AbsoluteFill>
  );
};

export const LouisYogaTVCComposition: React.FC = () => {
  return (
    <Composition
      id="louis-yoga-tvc"
      component={LouisYogaTVC}
      durationInFrames={DURATION}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
