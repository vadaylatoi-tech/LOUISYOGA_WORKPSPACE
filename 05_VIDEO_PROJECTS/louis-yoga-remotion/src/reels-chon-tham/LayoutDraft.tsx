import {
  AbsoluteFill,
  Composition,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { MONTSERRAT, useMontserrat } from "../shared/useMontserrat";

// LAYOUT MOCKUP ONLY (docs/LOUIS_YOGA_REELS_CHON_THAM_PLAN.md §3.2) — for approving the
// split layout before the real timeline is generated from the transcript. Not a final edit:
// no cuts, no animation; the two text states below are placed by hand just to show the look.
// Source has a pink card burned into y≈1060–1660, so the lower panel covers everything below PANEL_TOP.
const COLORS = {
  pink: "#d72182",
  wine: "#4a202c",
  blush: "#fcefef",
  rose: "#fed8e3",
  white: "#ffffff",
};

const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;
const DURATION = 1466; // 48.866s source, ffprobe
const PANEL_TOP = 1030;

const Panel: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      position: "absolute",
      left: 0,
      right: 0,
      top: PANEL_TOP,
      bottom: 0,
      background: `linear-gradient(180deg, ${COLORS.blush} 0%, ${COLORS.rose} 100%)`,
      borderTopLeftRadius: 56,
      borderTopRightRadius: 56,
      boxShadow: "0 -12px 40px rgba(74,32,44,0.25)",
      fontFamily: MONTSERRAT,
      color: COLORS.wine,
    }}
  >
    {children}
  </div>
);

const Caption: React.FC<{ words: string[]; active: number }> = ({ words, active }) => (
  <div
    style={{
      position: "absolute",
      left: 70,
      right: 70,
      top: 330,
      textAlign: "center",
      fontSize: 54,
      fontWeight: 700,
      lineHeight: 1.25,
    }}
  >
    {words.map((w, i) => (
      <span
        key={i}
        style={{
          display: "inline-block",
          marginRight: 14,
          color: i === active ? COLORS.pink : COLORS.wine,
          opacity: i > active ? 0.45 : 1,
        }}
      >
        {w}
      </span>
    ))}
  </div>
);

const HookState: React.FC = () => (
  <Panel>
    <div style={{ position: "absolute", top: 70, left: 0, right: 0, textAlign: "center" }}>
      <div style={{ fontSize: 34, fontWeight: 700, letterSpacing: 4, color: COLORS.pink }}>
        RA NHIỀU MỒ HÔI
      </div>
      <div style={{ fontSize: 92, fontWeight: 800, lineHeight: 1.05, marginTop: 10 }}>
        Chọn thảm nào?
      </div>
    </div>
    <Caption words={["Thảm", "loại", "nào", "hút", "mồ", "hôi", "tốt"]} active={4} />
  </Panel>
);

const StatState: React.FC = () => (
  <Panel>
    <div style={{ position: "absolute", top: 60, left: 0, right: 0, textAlign: "center" }}>
      <div style={{ fontSize: 34, fontWeight: 700, letterSpacing: 4, color: COLORS.pink }}>
        MỚI TẬP · ĐỘ DÀY
      </div>
      <div style={{ fontSize: 150, fontWeight: 800, lineHeight: 1, marginTop: 6 }}>
        4,5 <span style={{ fontSize: 90 }}>ly</span>
      </div>
      {/* Mat cross-section: thickness bar drawn to scale against a 6 mm reference. */}
      <div style={{ margin: "26px auto 0", width: 620, position: "relative", height: 40 }}>
        <div style={{ position: "absolute", inset: 0, borderRadius: 12, background: "rgba(74,32,44,0.12)" }} />
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            bottom: 0,
            width: `${(4.5 / 6) * 100}%`,
            borderRadius: 12,
            background: COLORS.pink,
          }}
        />
      </div>
    </div>
    <Caption words={["độ", "dày", "của", "thảm", "sẽ", "là", "4,5", "ly"]} active={7} />
  </Panel>
);

const LayoutDraft: React.FC = () => {
  useMontserrat();
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.blush }}>
      <OffthreadVideo src={staticFile("reels-chon-tham/source/source-1080p.mp4")} muted />
      {frame < 29 * FPS ? <HookState /> : <StatState />}
    </AbsoluteFill>
  );
};

export const ReelsChonThamLayoutDraft: React.FC = () => (
  <Composition
    id="louis-yoga-reels-chon-tham-layout-draft"
    component={LayoutDraft}
    durationInFrames={DURATION}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
);
