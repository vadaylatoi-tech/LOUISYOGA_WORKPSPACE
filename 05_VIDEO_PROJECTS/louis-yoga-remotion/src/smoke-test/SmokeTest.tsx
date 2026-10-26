import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { MONTSERRAT, useMontserrat } from "../shared/useMontserrat";

// Technical smoke test only — not a publishable video.
// Colors come from the Louis Yoga website design system (docs/LOUIS_YOGA_EDIT_GUIDE.md),
// not from an approved video guideline.
const COLORS = {
  bg: "#fcefef",
  pink: "#d72182",
  wine: "#4a202c",
};

const FPS = 30;
const DURATION = 8 * FPS;
const FADE = 15;

// Scene boundaries overlap by FADE frames so neighbouring scenes cross-fade.
const SCENES = [
  // "|" marks a deliberate line break, so lines split by meaning, not by width.
  { from: 0, to: 90, text: "Một khoảng nhỏ|cho mình" },
  { from: 90 - FADE, to: 165, text: "Bắt đầu|từ tấm thảm" },
  { from: 165 - FADE, to: DURATION, text: "Louis Yoga" },
];

const FONT_FAMILY = MONTSERRAT;

const SceneFade: React.FC<{
  durationInFrames: number;
  fadeIn: boolean;
  fadeOut: boolean;
  children: React.ReactNode;
}> = ({ durationInFrames, fadeIn, fadeOut, children }) => {
  const frame = useCurrentFrame();
  const inOpacity = fadeIn
    ? interpolate(frame, [0, FADE], [0, 1], { extrapolateRight: "clamp" })
    : 1;
  const outOpacity = fadeOut
    ? interpolate(frame, [durationInFrames - FADE, durationInFrames], [1, 0], {
        extrapolateLeft: "clamp",
      })
    : 1;
  return (
    <AbsoluteFill style={{ opacity: Math.min(inOpacity, outOpacity) }}>
      {children}
    </AbsoluteFill>
  );
};

const RiseText: React.FC<{ text: string; size: number; weight: number }> = ({
  text,
  size,
  weight,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  let wordIndex = 0;
  return (
    <div
      style={{
        fontFamily: FONT_FAMILY,
        fontSize: size,
        fontWeight: weight,
        color: COLORS.wine,
        textAlign: "center",
        lineHeight: 1.25,
        padding: "0 120px",
      }}
    >
      {text.split("|").map((line, lineIndex) => {
        const words = line.split(" ");
        return (
          <div key={lineIndex} style={{ whiteSpace: "nowrap" }}>
            {words.map((word, i) => {
              const progress = spring({
                frame: frame - 6 - wordIndex++ * 4,
                fps,
                config: { damping: 200 },
              });
              return (
                <span
                  key={i}
                  style={{
                    display: "inline-block",
                    whiteSpace: "pre",
                    opacity: progress,
                    transform: `translateY(${(1 - progress) * 40}px)`,
                  }}
                >
                  {word + (i < words.length - 1 ? " " : "")}
                </span>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

// A rounded bar that "unrolls" from the left — an abstract stand-in for a mat.
const MatShape: React.FC<{ delay: number; vertical: boolean }> = ({
  delay,
  vertical,
}) => {
  const frame = useCurrentFrame();
  const unroll = interpolate(frame - delay, [0, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const width = vertical ? 360 : 720;
  const height = vertical ? 640 : 120;
  return (
    <div
      style={{
        width,
        height,
        borderRadius: 60,
        backgroundColor: COLORS.pink,
        opacity: 0.9,
        transform: vertical ? `scaleY(${unroll})` : `scaleX(${unroll})`,
        transformOrigin: vertical ? "center top" : "left center",
      }}
    />
  );
};

const SmokeTest: React.FC = () => {
  useMontserrat();
  const frame = useCurrentFrame();
  // One continuous, very slow drift across the whole timeline (no segmented keyframes).
  const drift = interpolate(frame, [0, DURATION], [1, 1.03]);

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <AbsoluteFill style={{ transform: `scale(${drift})` }}>
        {SCENES.map((scene, i) => {
          const duration = scene.to - scene.from;
          const isLast = i === SCENES.length - 1;
          return (
            <Sequence
              key={scene.text}
              from={scene.from}
              durationInFrames={duration}
            >
              <SceneFade
                durationInFrames={duration}
                fadeIn={i > 0}
                fadeOut={!isLast}
              >
                <AbsoluteFill
                  style={{
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column",
                    gap: 80,
                  }}
                >
                  {i === 0 ? <MatShape delay={20} vertical={false} /> : null}
                  {i === 1 ? <MatShape delay={10} vertical /> : null}
                  <RiseText
                    text={scene.text}
                    size={isLast ? 120 : 84}
                    weight={isLast ? 700 : 600}
                  />
                  {isLast ? <AccentLine /> : null}
                </AbsoluteFill>
              </SceneFade>
            </Sequence>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const AccentLine: React.FC = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [20, 45], [0, 240], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        width,
        height: 8,
        borderRadius: 4,
        backgroundColor: COLORS.pink,
      }}
    />
  );
};

export const SmokeTestComposition: React.FC = () => {
  return (
    <Composition
      id="louis-yoga-remotion-smoke-test"
      component={SmokeTest}
      durationInFrames={DURATION}
      fps={FPS}
      width={1080}
      height={1920}
    />
  );
};
