import {
  AbsoluteFill,
  Audio,
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
import { TIMELINE } from "./timeline.gen";

// Reels "Ra nhiều mồ hôi, chọn thảm nào?" — plan: docs/LOUIS_YOGA_REELS_CHON_THAM_PLAN.md.
// Source is an already-edited Louis Yoga clip with a pink card burned into y≈1060–1660, so the
// speaker keeps the top of the frame and a new graphics panel covers everything below PANEL_TOP.
// Every time value comes from timeline.gen.ts (generated from the transcript), never typed here.
const COLORS = {
  pink: "#d72182",
  wine: "#4a202c",
  blush: "#fcefef",
  rose: "#fed8e3",
  white: "#ffffff",
};

const FPS = TIMELINE.fps;
const WIDTH = 1080;
const HEIGHT = 1920;
const PANEL_TOP = 1030;
// Content stays inside x 90–910: the Reels/TikTok action column sits on the right edge.
const CONTENT_LEFT = 90;
const CONTENT_WIDTH = 820;
const GRAPHIC_TOP = 1075;
const CAPTION_TOP = 1350;
const END_CARD_FRAMES = 75;
const LOGO_TRIM = 20; // s10.mp4: start on the outline reveal, logo fully formed by ~frame 50
const DURATION = TIMELINE.speechFrames + END_CARD_FRAMES;
const SOURCE = staticFile("reels-chon-tham/source/source-1080p.mp4");

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Soft entrance used by every graphic element (no bounce, per the brand guide).
const useAppear = (at: number) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - at, fps, config: { damping: 200 }, durationInFrames: 9 });
};

const Appear: React.FC<{ at: number; children: React.ReactNode; dy?: number }> = ({
  at,
  children,
  dy = 24,
}) => {
  const p = useAppear(at);
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * dy}px)` }}>{children}</div>
  );
};

// ---------- Speaker (top) ----------

const punchScale = (frame: number) => {
  for (const p of TIMELINE.punches) {
    const ramp = interpolate(frame, [p.from, p.from + 6, p.to - 10, p.to], [0, 1, 1, 0], {
      ...clamp,
      easing: Easing.inOut(Easing.cubic),
    });
    if (ramp > 0) {
      return { scale: 1 + 0.07 * ramp, x: p.x, y: p.y };
    }
  }
  return { scale: 1, x: 540, y: 500 };
};

const SpeakerLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const { scale, x, y } = punchScale(frame);
  let offset = 0;
  return (
    <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: `${x}px ${y}px` }}>
      {TIMELINE.keep.map((k, i) => {
        const len = k.srcTo - k.srcFrom;
        const from = offset;
        offset += len;
        const first = i === 0;
        const last = i === TIMELINE.keep.length - 1;
        return (
          <Sequence key={k.srcFrom} from={from} durationInFrames={len}>
            <OffthreadVideo
              src={SOURCE}
              trimBefore={k.srcFrom}
              trimAfter={k.srcTo}
              // 3-frame ramps hide clicks in the baked-in music bed at each cut.
              volume={(f) =>
                interpolate(f, [0, 3, len - 3, len], [first ? 1 : 0, 1, 1, last ? 1 : 0], clamp)
              }
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- Icons (simple line drawings, brand colours) ----------

const Drop: React.FC<{ size: number; color?: string }> = ({ size, color = COLORS.pink }) => (
  <svg width={size} height={size * 1.3} viewBox="0 0 40 52">
    <path d="M20 2 C20 2 4 22 4 33 a16 16 0 0 0 32 0 C36 22 20 2 20 2 Z" fill={color} />
    <path d="M12 34 a8 8 0 0 0 7 8" stroke={COLORS.white} strokeWidth={3} fill="none" strokeLinecap="round" />
  </svg>
);

const Thermometer: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size * 0.5} height={size} viewBox="0 0 30 60">
    <rect x={9} y={3} width={12} height={40} rx={6} fill="none" stroke={COLORS.wine} strokeWidth={3} />
    <circle cx={15} cy={47} r={10} fill={COLORS.pink} />
    <rect x={12.5} y={18} width={5} height={28} rx={2.5} fill={COLORS.pink} />
  </svg>
);

const MatRoll: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 60 60">
    <rect x={8} y={12} width={44} height={36} rx={4} fill={COLORS.rose} stroke={COLORS.wine} strokeWidth={3} />
    <circle cx={14} cy={30} r={10} fill={COLORS.pink} stroke={COLORS.wine} strokeWidth={3} />
    <circle cx={14} cy={30} r={4} fill={COLORS.white} />
  </svg>
);

const Person: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 60 60">
    <circle cx={30} cy={16} r={9} fill={COLORS.pink} />
    <path d="M14 54 c0-14 7-22 16-22 s16 8 16 22" fill="none" stroke={COLORS.wine} strokeWidth={4} strokeLinecap="round" />
  </svg>
);

const Check: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 40 40">
    <circle cx={20} cy={20} r={19} fill={COLORS.pink} />
    <path d="M11 21 l6 6 l12 -13" stroke={COLORS.white} strokeWidth={4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const ArrowUp: React.FC<{ size: number }> = ({ size }) => {
  const frame = useCurrentFrame();
  const bob = Math.sin(frame / 5) * 6;
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" style={{ transform: `translateY(${bob}px)` }}>
      <path d="M20 36 V6 M8 18 L20 6 L32 18" stroke={COLORS.pink} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
};

// ---------- Panel beats ----------

const Label: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ fontSize: 32, fontWeight: 700, letterSpacing: 5, color: COLORS.pink, whiteSpace: "nowrap" }}>
    {children}
  </div>
);

const Title: React.FC<{ children: string }> = ({ children }) => (
  <div
    style={{
      fontSize: children.length > 16 ? 70 : 92,
      fontWeight: 800,
      lineHeight: 1.05,
      color: COLORS.wine,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </div>
);

const Row: React.FC<{ icon: React.ReactNode; children: React.ReactNode }> = ({ icon, children }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
    <div style={{ flexShrink: 0 }}>{icon}</div>
    <div>{children}</div>
  </div>
);

const Pill: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 14,
      padding: "10px 26px",
      borderRadius: 999,
      background: COLORS.pink,
      color: COLORS.white,
      fontSize: 40,
      fontWeight: 700,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </div>
);

type Beat = (typeof TIMELINE.beats)[number];

const BeatView: React.FC<{ beat: Beat }> = ({ beat }) => {
  const frame = useCurrentFrame();
  const center: React.CSSProperties = { display: "flex", flexDirection: "column", alignItems: "center", gap: 10 };
  switch (beat.kind) {
    case "title":
      return (
        <div style={center}>
          <Appear at={beat.from}>
            <Label>{beat.label}</Label>
          </Appear>
          <Appear at={beat.from + 4}>
            <Title>{beat.title}</Title>
          </Appear>
        </div>
      );
    case "material":
      return (
        <div style={{ ...center, gap: 22 }}>
          <Appear at={beat.from}>
            <Row icon={<MatRoll size={140} />}>
              <Label>CHẤT LIỆU</Label>
              <Title>Cao su tự nhiên</Title>
            </Row>
          </Appear>
          <Appear at={beat.pop}>
            <Pill>
              <Drop size={30} color={COLORS.white} /> Thấm hút mồ hôi tốt
            </Pill>
          </Appear>
        </div>
      );
    case "hotyoga":
      return (
        <Row icon={<Thermometer size={150} />}>
          <Appear at={beat.from}>
            <Label>HAY TẬP THEO</Label>
          </Appear>
          <Appear at={beat.pop}>
            <div style={{ fontSize: 120, fontWeight: 800, color: COLORS.pink, lineHeight: 1 }}>Hot yoga</div>
          </Appear>
        </Row>
      );
    case "pointer":
      return (
        <Row icon={<ArrowUp size={120} />}>
          <Appear at={beat.from}>
            <Label>{beat.label}</Label>
            <Title>{beat.title}</Title>
          </Appear>
        </Row>
      );
    case "audience": {
      const titleAt = "pop" in beat ? beat.pop : beat.from + 4;
      return (
        <Row icon={<Person size={130} />}>
          <Appear at={beat.from}>
            <Label>{beat.label}</Label>
          </Appear>
          <Appear at={titleAt}>
            <Title>{beat.title}</Title>
          </Appear>
        </Row>
      );
    }
    case "stat": {
      const count = interpolate(frame, [beat.pop, beat.pop + 12], [0, 4.5], {
        ...clamp,
        easing: Easing.out(Easing.cubic),
      });
      const shown = count.toFixed(1).replace(".", ",");
      const badge = frame >= beat.extra ? "Thậm chí còn dư" : "Vừa đủ";
      return (
        <div style={{ ...center, gap: 6 }}>
          <Appear at={beat.from}>
            <Label>ĐỘ DÀY · NGƯỜI MỚI TẬP</Label>
          </Appear>
          <div style={{ display: "flex", alignItems: "center", gap: 36 }}>
            <div style={{ fontSize: 150, fontWeight: 800, color: COLORS.wine, lineHeight: 1, opacity: frame < beat.pop ? 0 : 1 }}>
              {shown}
              <span style={{ fontSize: 80, marginLeft: 14 }}>ly</span>
            </div>
            <Appear at={beat.enough} dy={0}>
              <div style={{ transform: `scale(${frame >= beat.enough ? 1 : 0.8})` }}>
                <Pill>
                  <Check size={36} /> {badge}
                </Pill>
              </div>
            </Appear>
          </div>
        </div>
      );
    }
    case "checklist":
      return (
        <div style={{ ...center, alignItems: "flex-start", gap: 4, paddingLeft: 120 }}>
          <Appear at={beat.from}>
            <Label>BỀ MẶT THẢM CẦN</Label>
          </Appear>
          {beat.items.map((it) => (
            <Appear key={it.text} at={it.at} dy={0}>
              <Row icon={<Check size={44} />}>
                <div style={{ fontSize: 48, fontWeight: 700, color: COLORS.wine, whiteSpace: "nowrap" }}>{it.text}</div>
              </Row>
            </Appear>
          ))}
        </div>
      );
    case "brand":
      return (
        <div style={{ ...center, gap: 18 }}>
          <Appear at={beat.from}>
            <Label>CÁC DÒNG THẢM</Label>
          </Appear>
          <Appear at={beat.from + 4}>
            <div style={{ fontSize: 96, fontWeight: 800, letterSpacing: 6, color: COLORS.wine, whiteSpace: "nowrap" }}>
              LOUIS YOGA
            </div>
          </Appear>
          <Appear at={beat.pop}>
            <Pill>
              <Check size={36} /> Đều đáp ứng được
            </Pill>
          </Appear>
        </div>
      );
    default:
      return null;
  }
};

const Panel: React.FC = () => {
  const frame = useCurrentFrame();
  return (
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
        boxShadow: "0 -12px 40px rgba(74,32,44,0.22)",
      }}
    >
      {TIMELINE.beats.map((b) => {
        if (frame < b.from || frame >= b.to) return null;
        const out = interpolate(frame, [b.to - 5, b.to], [1, 0], clamp);
        return (
          <div
            key={`${b.kind}-${b.from}`}
            style={{
              position: "absolute",
              left: CONTENT_LEFT,
              width: CONTENT_WIDTH,
              top: GRAPHIC_TOP - PANEL_TOP,
              height: CAPTION_TOP - GRAPHIC_TOP - 20,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              opacity: out,
            }}
          >
            <BeatView beat={b} />
          </div>
        );
      })}
    </div>
  );
};

// ---------- Full-screen cards over the stretches where the speaker leaves frame ----------

type Card = (typeof TIMELINE.cards)[number];

const FALLING = [
  { x: 120, delay: 0, size: 60 },
  { x: 300, delay: 14, size: 44 },
  { x: 760, delay: 6, size: 70 },
  { x: 900, delay: 22, size: 40 },
  { x: 560, delay: 30, size: 50 },
  { x: 200, delay: 40, size: 36 },
  { x: 680, delay: 48, size: 46 },
];

const SweatCard: React.FC<{ card: Card }> = ({ card }) => {
  const frame = useCurrentFrame();
  const t = frame - card.from;
  return (
    <>
      {FALLING.map((d) => {
        const y = ((t * 7 + d.delay * 9) % 1000) + 60;
        return (
          <div key={d.x} style={{ position: "absolute", left: d.x, top: y, opacity: 0.35 }}>
            <Drop size={d.size} />
          </div>
        );
      })}
      <div style={{ position: "absolute", top: 330, left: CONTENT_LEFT, width: CONTENT_WIDTH, display: "flex", flexDirection: "column", alignItems: "center", gap: 30 }}>
        <Appear at={card.from}>
          <Drop size={220} />
        </Appear>
        <Appear at={card.from + 5}>
          <Label>TẬP LUYỆN · VẬN ĐỘNG</Label>
        </Appear>
        {"pop" in card ? (
          <Appear at={card.pop}>
            <div style={{ fontSize: 104, fontWeight: 800, color: COLORS.wine, textAlign: "center", lineHeight: 1.05 }}>
              Ra nhiều
              <br />
              <span style={{ color: COLORS.pink }}>mồ hôi</span>
            </div>
          </Appear>
        ) : null}
      </div>
    </>
  );
};

const ThicknessCard: React.FC<{ card: Card }> = ({ card }) => {
  const frame = useCurrentFrame();
  const grow = interpolate(frame, [card.from + 6, card.from + 22], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const bar = (h: number, color: string, label: string, at: number) => (
    <Appear at={at}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
        <div style={{ width: 330, height: 320, display: "flex", alignItems: "flex-end" }}>
          <div style={{ width: "100%", height: h, borderRadius: 14, background: color, boxShadow: "0 10px 24px rgba(74,32,44,0.18)" }} />
        </div>
        <div style={{ fontSize: 50, fontWeight: 700, color: COLORS.wine, whiteSpace: "nowrap" }}>{label}</div>
      </div>
    </Appear>
  );
  return (
    <div style={{ position: "absolute", top: 380, left: CONTENT_LEFT, width: CONTENT_WIDTH, display: "flex", flexDirection: "column", alignItems: "center", gap: 70 }}>
      <Appear at={card.from}>
        <div style={{ fontSize: 88, fontWeight: 800, color: COLORS.wine, whiteSpace: "nowrap" }}>Độ dày thảm</div>
      </Appear>
      <div style={{ display: "flex", gap: 80, alignItems: "flex-end" }}>
        {bar(60, "rgba(74,32,44,0.25)", "Thảm mỏng", card.from + 2)}
        {bar(60 + 140 * grow, COLORS.pink, "Dày hơn", card.from + 6)}
      </div>
    </div>
  );
};

const Cards: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      {TIMELINE.cards.map((c) => {
        if (frame < c.from - 1 || frame >= c.to) return null;
        const vis = interpolate(frame, [c.from - 1, c.from + 5, c.to - 6, c.to], [0, 1, 1, 0], clamp);
        // Slow continuous push (≤ 4%) so the card never sits still.
        const drift = interpolate(frame, [c.from, c.to], [1, 1.04], clamp);
        return (
          <AbsoluteFill
            key={c.kind}
            style={{
              background: `linear-gradient(180deg, ${COLORS.white} 0%, ${COLORS.blush} 55%, ${COLORS.rose} 100%)`,
              opacity: vis,
              transform: `scale(${(1.04 - 0.04 * vis) * drift})`,
            }}
          >
            {c.kind === "sweat" ? <SweatCard card={c} /> : <ThicknessCard card={c} />}
          </AbsoluteFill>
        );
      })}
    </>
  );
};

// ---------- Karaoke caption ----------

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const line = TIMELINE.captions.find((c) => frame >= c.from && frame < c.to);
  if (!line) return null;
  const inP = interpolate(frame, [line.from, line.from + 4], [0, 1], clamp);
  return (
    <div
      style={{
        position: "absolute",
        top: CAPTION_TOP,
        left: CONTENT_LEFT,
        width: CONTENT_WIDTH,
        textAlign: "center",
        fontSize: 52,
        fontWeight: 700,
        lineHeight: 1.28,
        textWrap: "balance",
        opacity: inP,
        transform: `translateY(${(1 - inP) * 10}px)`,
      }}
    >
      {line.words.map((w, i) => {
        const next = line.words[i + 1]?.start ?? line.to;
        const active = frame >= w.start && frame < next;
        const said = frame >= w.start;
        return (
          // inline-block keeps each word (and its Vietnamese diacritics) on one line.
          <span
            key={i}
            style={{
              display: "inline-block",
              marginRight: 14,
              color: active ? COLORS.pink : COLORS.wine,
              opacity: said ? 1 : 0.4,
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};

// ---------- End card: Louis Yoga's own logo animation (from the brand film) ----------

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const src = staticFile("tvc/clips/s10.mp4");
  const ctaIn = spring({ frame: frame - 24, fps: FPS, config: { damping: 200 }, durationInFrames: 12 });
  const scale = 1.25;
  return (
    <AbsoluteFill style={{ backgroundColor: "#e4e4e4" }}>
      <OffthreadVideo
        src={src}
        muted
        trimBefore={LOGO_TRIM}
        style={{ position: "absolute", top: 0, left: -1100, width: 3413, height: HEIGHT, filter: "blur(40px)" }}
      />
      <OffthreadVideo
        src={src}
        muted
        trimBefore={LOGO_TRIM}
        style={{
          position: "absolute",
          top: 260,
          left: WIDTH / 2 - (1920 * scale) / 2,
          width: 1920 * scale,
          height: 1080 * scale,
          maskImage: "radial-gradient(ellipse 38% 45% at 50% 50%, black 60%, transparent 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 1230,
          left: CONTENT_LEFT,
          width: CONTENT_WIDTH,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 26,
          opacity: ctaIn,
          transform: `translateY(${(1 - ctaIn) * 24}px)`,
        }}
      >
        <div style={{ fontSize: 60, fontWeight: 800, color: COLORS.wine, whiteSpace: "nowrap" }}>
          Muốn chọn đúng thảm?
        </div>
        <div style={{ transform: "scale(1.35)", margin: "14px 0" }}>
          <Pill>Theo dõi Louis Yoga</Pill>
        </div>
        <div style={{ fontSize: 44, fontWeight: 600, color: COLORS.wine, whiteSpace: "nowrap" }}>
          để xem thêm mẹo chọn thảm
        </div>
      </div>
    </AbsoluteFill>
  );
};

const ReelsChonTham: React.FC = () => {
  useMontserrat();
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.blush, fontFamily: MONTSERRAT }}>
      <Sequence durationInFrames={TIMELINE.speechFrames}>
        <SpeakerLayer />
        <Panel />
        <Cards />
        <Captions />
      </Sequence>
      <Sequence from={TIMELINE.speechFrames}>
        <EndCard />
      </Sequence>
      {TIMELINE.sfx.map((s, i) => (
        <Sequence key={i} from={s.at} durationInFrames={2 * FPS}>
          <Audio src={staticFile(`reels-chon-tham/sfx/${s.file}`)} volume={s.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const ReelsChonThamComposition: React.FC = () => (
  <Composition
    id="louis-yoga-reels-chon-tham"
    component={ReelsChonTham}
    durationInFrames={DURATION}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
);
