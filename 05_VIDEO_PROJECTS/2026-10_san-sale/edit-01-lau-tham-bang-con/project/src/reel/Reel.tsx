import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import {
  BigText,
  BottomShade,
  CalloutLine,
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
  useLife,
} from "../kit/atoms";
import { Broll, BrollLayer, Captions, Focus, Punch, TalkingHead } from "../kit/media";
import { Cue, SoundLayer, STEM } from "../kit/sound";
import { C, clamp, f, font, FPS, W } from "../kit/theme";
import { MONTSERRAT, useMontserrat } from "../kit/useMontserrat";
import { CAPTIONS, CLEAN_DURATION, CUTS, FACE } from "./data";

// =====================================================================================
// LOUIS YOGA REEL — STYLE 1.  Reel "Lau thảm bằng cồn có sao không?" (series Săn sale, video 01).
// Built on the approved v4 template; only the ▼ EDIT ▼ blocks differ.
// =====================================================================================

const VIDEO_FRAMES = Math.round(CLEAN_DURATION * FPS);
const TAIL = 54; // CTA hold after the last word (1.8 s)
const DURATION = VIDEO_FRAMES + TAIL;

// ▼ EDIT ▼ layout bands — measured on this footage: face y≈560–780, spray box on the table
// (610,1290), foam blocks / mats fill y 1300–1860 (decor, safe to cover with panels).
const CAP_Y = 1030; // on the shirt, between chin and the spray box
const G = 1390; // top of the lower graphics band

const FOOTAGE = "footage/clean.mp4";
const FILM = "broll/louisyoga_brand_film_30fps.mp4";
const MUSIC = "music/Inspired_KevinMacLeod_CCBY4.mp3";

// ▼ EDIT ▼ camera: 14 segments (13 cuts), alternate tight/wide.
const SEG_ZOOM = [1.24, 1.1, 1.28, 1.14, 1.3, 1.12, 1.26, 1.1, 1.22, 1.14, 1.28, 1.12, 1.24, 1.12];
const PUNCHES: Punch[] = [
  [1.75, 2.55, 0.22], // hook drop
  [5.66, 6.4, 0.08], // "làm sạch rất là tốt"
  [8.94, 9.3, 0.1], // "cao su"
  [28.62, 29.7, 0.14], // "mủn"
  [38.49, 39.8, 0.08], // "không sử dụng được"
  [47.66, 48.6, 0.12], // "nhà sản xuất"
];
const FOCUS: Focus[] = [
  [9.32, 10.5, 900, 1420, 1.32], // "như thế này này" → onto the rubber mat roll
  [32.4, 35.0, 610, 1290, 1.62], // "sản phẩm chuyên dụng" → onto the Louis Yoga mat spray box
];

// ▼ EDIT ▼ B-roll cutaways from the Louis Yoga brand film (references/broll-index.md)
const BROLL: Broll[] = [
  { start: 17.55, end: 19.95, film: 46.2, cx: 1000, label: "Bề mặt thảm" },
  { start: 40.95, end: 43.15, film: 52.8, cx: 900, label: "Chất lượng thảm" },
  // The source footage has a picture-in-picture clip sliding in from 52.9 s to the end; cover it
  // (and the CTA freeze) with a calm meditation shot. No label; soft swoosh on entry.
  { start: 52.9, end: (VIDEO_FRAMES + TAIL) / FPS + 0.3, film: 12.3, cx: 940, label: "" },
];

// ▼ EDIT ▼ shake/flash only on the heaviest hits: [s, frames, px, flash]
const HOOK_DROP = 1.75;
const MUN = 28.66;
const ADVICE = 47.7;
const IMPACTS: Impact[] = [
  [0.0, 6, 10, 0.35],
  [0.55, 5, 7, 0],
  [HOOK_DROP, 10, 18, 0.6],
  [MUN, 7, 9, 0],
  [ADVICE, 5, 7, 0],
];

// ▼ EDIT ▼ SFX — reel-2 density (~0.6/s), one sound per beat.
const CUES: Cue[] = [
  [0.0, "swoosh.mp3", 0.65],
  [0.05, "punch.mp3", 0.8],
  [0.55, "pop-2.mp3", 0.59],
  [HOOK_DROP, "riser-metallic.mp3", 0.45],
  [HOOK_DROP, "punch.mp3", 0.95],
  [3.3, "quick-swoosh.mp3", 0.53], // panel: cồn
  [5.66, "quick-ting.mp3", 0.53], // ✓ làm sạch tốt
  [6.85, "quick-swoosh.mp3", 0.47], // panel: cao su
  [9.04, "pop-2.mp3", 0.53], // cao su tag
  [11.66, "quick-swoosh.mp3", 0.53], // cồn + cao su = ?
  [14.55, "pop.mp3", 0.53], // "?"
  [17.55, "swoosh.mp3", 0.59], // B-roll in
  [21.72, "pop-2.mp3", 0.53], // pill: lau cồn
  [23.5, "pop.mp3", 0.47], // pill: phơi nắng
  [25.5, "quick-swoosh.mp3", 0.47], // durability bar drops
  [MUN, "punch.mp3", 0.85], // DỄ MỦN!
  [29.94, "quick-swoosh.mp3", 0.47], // kicker "tốt nhất"
  [32.59, "punch.mp3", 0.7], // slam "dùng đồ chuyên dụng"
  [33.4, "pop-2.mp3", 0.53], // callout on the spray box
  [35.33, "correct.mp3", 0.53], // ✓ tốt hơn
  [37.15, "quick-swoosh.mp3", 0.53], // panel: còn cồn thì
  [38.49, "pop-2.mp3", 0.53], // không cấm
  [40.0, "pop.mp3", 0.47], // tùy chất lượng
  [40.95, "swoosh.mp3", 0.53], // B-roll in
  [43.48, "quick-swoosh.mp3", 0.47], // "có gì dùng nấy"
  [44.62, "pop-2.mp3", 0.47], // strike
  [ADVICE, "punch.mp3", 0.8], // HỎI NHÀ SẢN XUẤT
  [50.3, "quick-ting.mp3", 0.53],
  [51.34, "quick-ting.mp3", 0.53],
  [52.4, "quick-ting.mp3", 0.53],
  [52.9, "swoosh.mp3", 0.4], // closing B-roll in
  [53.3, "correct.mp3", 0.53],
  [54.4, "punch.mp3", 0.7],
  [54.65, "camera-shutter.mp3", 0.53],
  [55.0, "ding.mp3", 0.41],
];
const MUSIC_CURVE: [number[], number[]] = [
  [0, 4, f(2.4), f(3.0), VIDEO_FRAMES - 4, VIDEO_FRAMES + 6, DURATION - 12, DURATION],
  [0, 0.2, 0.2, 0.09, 0.09, 0.26, 0.26, 0],
];

// ▼ EDIT ▼ scenes ------------------------------------------------------------------

// Hook (0–3 s): "LAU THẢM / BẰNG CỒN?" slams twice, gets crossed out, "DỄ MỦN THẢM!" stamp drops.
const Hook: React.FC = () => (
  <>
    <TopShade start={0} end={f(3.1)} />
    <BigText start={0} end={f(3.1)} y={120} slam lines={[{ text: "Lau thảm", color: C.white, size: 108 }]} />
    <BigText start={f(0.55)} end={f(3.1)} y={232} slam lines={[{ text: "bằng cồn?", color: C.accent, size: 128 }]} />
    <StrikeLine d="M230,340 L850,290" start={f(HOOK_DROP)} end={f(3.1)} />
    <BottomShade start={f(HOOK_DROP) - 2} end={f(2.75)} />
    <Stamp text="Dễ mủn thảm!" start={f(HOOK_DROP)} end={f(2.75)} x={540} y={G + 130} rot={-8} size={112} />
  </>
);

// "cồn hỗ trợ làm sạch rất là tốt" — real photo of rubbing alcohol + ✓.
const AlcoholScene: React.FC = () => {
  const s = f(3.3);
  const e = f(6.75);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src="img/chai_con.jpg" label="Cồn" x={30} y={25} w={300} h={220} start={s} end={e} />
      <div style={{ position: "absolute", left: 370, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Công dụng</div>
      <div style={{ position: "absolute", left: 370, top: 82, ...font(900, 58), color: C.white }}>Hỗ trợ</div>
      <div style={{ position: "absolute", left: 370, top: 142, ...font(900, 58), color: C.accent }}>làm sạch</div>
      <Pill text="✓ Tốt" start={f(5.66)} end={e} x={770} y={110} bg={C.gold} fg={C.ink} size={40} />
      <div style={{ position: "absolute", right: 14, bottom: 6, fontFamily: MONTSERRAT, fontSize: 12, color: "rgba(255,255,255,0.45)" }}>
        Ảnh cồn: Craig Spurrier · CC BY 2.5
      </div>
    </Panel>
  );
};

// "Tuy nhiên ... chất liệu nó là cao su" — Louis Yoga rubber mats photo.
const RubberScene: React.FC = () => {
  const s = f(6.85);
  const e = f(9.3);
  return (
    <>
      <Kicker text="Tuy nhiên" start={s} end={e} y={300} color={C.gold} />
      <Panel start={s} end={e} y={G} h={270}>
        <PhotoCard src="img/cuon_caosu.jpg" label="Louis Yoga" x={30} y={25} w={360} h={220} start={s} end={e} />
        <div style={{ position: "absolute", left: 430, top: 40, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Thảm chất liệu</div>
        <div style={{ position: "absolute", left: 430, top: 90, ...font(900, 92), color: C.accent }}>Cao su</div>
        <Pill text="tự nhiên" start={f(9.04)} end={e} x={600} y={196} bg={C.white} fg={C.ink} size={30} />
      </Panel>
    </>
  );
};

// "dùng cồn mà chưa biết có phù hợp với dòng chất liệu này hay không" — CỒN + CAO SU = ?
const MatchScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(11.66);
  const e = f(16.45);
  const q = interpolate(frame, [f(14.55), f(14.55) + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2.5)) });
  const wob = frame > f(14.55) + 8 ? Math.sin((frame - f(14.55)) / 4) * 6 : 0;
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <PhotoCard src="img/chai_con.jpg" label="Cồn" x={30} y={25} w={250} h={220} start={s} end={e} />
      <div style={{ position: "absolute", left: 296, top: 92, ...font(900, 72), color: C.gold }}>+</div>
      <PhotoCard src="img/cuon_caosu.jpg" label="Cao su" x={360} y={25} w={280} h={220} start={s} end={e} />
      <div style={{ position: "absolute", left: 656, top: 92, ...font(900, 72), color: C.gold }}>=</div>
      <div
        style={{
          position: "absolute",
          left: 730,
          top: 20,
          width: 140,
          textAlign: "center",
          ...font(900, 210),
          color: C.accent,
          transform: `scale(${q}) rotate(${wob}deg)`,
          textShadow: "0 0 30px rgba(255,90,174,0.55)",
        }}
      >
        ?
      </div>
    </Panel>
  );
};

// "dùng cồn hay phơi nắng ... làm giảm độ bền ... dễ bị mủn" — two causes + durability bar + stamp.
const DamageScene: React.FC = () => {
  const frame = useCurrentFrame();
  const s = f(21.6);
  const e = f(29.85);
  const bar = interpolate(frame, [f(25.5), f(27.1)], [1, 0.28], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const red = interpolate(frame, [f(25.5), f(27.1)], [0, 1], clamp);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <Pill text="Lau cồn" start={f(21.72)} end={e} x={230} y={28} bg={C.pinkDeep} size={40} />
      <Pill text="Phơi nắng trực tiếp" start={f(23.5)} end={e} x={620} y={28} bg={C.gold} fg={C.ink} size={36} />
      <div style={{ position: "absolute", left: 50, top: 132, ...font(800, 30), color: C.dim, letterSpacing: 3 }}>Độ bền thảm</div>
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
  );
};

// "Tốt nhất ... dùng sản phẩm chuyên dụng để vệ sinh thảm cao su" — camera moves onto the spray box.
const BestScene: React.FC = () => {
  const s = f(29.94);
  const e = f(36.3);
  const cs = f(33.4);
  const ce = f(35.0);
  const life = useLife(cs, ce);
  return (
    <>
      <TopShade start={s} end={e} />
      <Kicker text="Tốt nhất nên" start={s} end={e} y={250} color={C.gold} />
      <BigText
        start={f(32.59)}
        end={e}
        y={310}
        slam
        lines={[
          { text: "Dùng đồ", color: C.white, size: 92 },
          { text: "chuyên dụng", color: C.accent, size: 104 },
        ]}
      />
      {life > 0 && (
        <>
          <CalloutLine d="M330,1500 C330,1420 400,1330 505,1300" tip={[505, 1300]} start={cs} end={ce} />
          <Pill text="Xịt thảm Louis Yoga" start={cs + 3} end={ce} x={330} y={1500} size={40} />
        </>
      )}
      <Polaroid src="img/xit_cafe.jpg" label="Xịt thảm yoga" start={f(35.0)} end={e} x={620} y={G - 60} w={250} h={250} rot={6} />
      <Pill text="✓ Tốt hơn cho thảm" start={f(35.33)} end={e} x={330} y={G + 120} bg={C.gold} fg={C.ink} size={42} />
    </>
  );
};

// "Còn cồn thì ... không phải là không sử dụng được, nhưng tùy thuộc chất lượng sản phẩm".
const NuanceScene: React.FC = () => {
  const s = f(37.15);
  const e = f(40.95);
  return (
    <Panel start={s} end={e} y={G} h={270}>
      <div style={{ position: "absolute", top: 26, left: 0, right: 0, textAlign: "center", ...font(800, 30), color: C.dim, letterSpacing: 4 }}>
        Còn cồn thì sao?
      </div>
      <Pill text="Không cấm" start={f(38.49)} end={e} x={250} y={92} bg={C.white} fg={C.ink} size={46} />
      <Pill text="Tùy chất lượng thảm" start={f(40.0)} end={e} x={450} y={176} bg={C.pinkDeep} size={46} />
    </Panel>
  );
};

// Conclusion: "thay vì có gì dùng nấy → tham khảo khuyến nghị của nhà sản xuất / bên bán".
const AdviceScene: React.FC = () => (
  <>
    <BottomShade start={f(43.48)} end={f(49.9)} />
    <BigText start={f(43.48)} end={f(45.5)} y={G + 40} lines={[{ text: "Có gì dùng nấy?", color: C.white, size: 84 }]} />
    <StrikeLine d="M150,1475 L930,1440" start={f(44.62)} end={f(45.5)} length={800} />
    <Kicker text="Hãy tham khảo" start={f(45.6)} end={f(49.9)} y={G + 10} color={C.gold} />
    <BigText
      start={f(ADVICE)}
      end={f(49.9)}
      y={G + 70}
      slam
      lines={[
        { text: "Nhà sản xuất", color: C.accent, size: 104 },
        { text: "hoặc bên bán", color: C.white, size: 70 },
      ]}
    />
  </>
);

// Closing checklist (long labels → one item per row instead of the 2x2 CheckGrid).
const CheckList: React.FC<{ items: [string, number][]; start: number; end: number; y: number }> = ({ items, start, end, y }) => {
  const frame = useCurrentFrame();
  return (
    <Panel start={start} end={end} y={y} h={290}>
      {items.map(([label, at], i) => {
        if (frame < f(at)) return null;
        const p = interpolate(frame, [f(at), f(at) + 6], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
        return (
          <div key={i} style={{ position: "absolute", left: 50, top: 22 + i * 64, display: "flex", alignItems: "center", opacity: p, transform: `translateX(${(1 - p) * -60}px)` }}>
            <div style={{ width: 50, height: 50, borderRadius: 99, background: C.pinkDeep, display: "flex", alignItems: "center", justifyContent: "center", color: C.white, ...font(900, 30), boxShadow: "0 0 18px rgba(255,90,174,0.5)" }}>✓</div>
            <div style={{ marginLeft: 20, ...font(900, 44), color: C.white }}>{label}</div>
          </div>
        );
      })}
    </Panel>
  );
};

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
      <Polaroid src="img/xit_4.jpg" label="Xịt thảm yoga" start={s + 8} end={DURATION + 1} x={80} y={G - 70} w={240} h={240} rot={-7} />
      <Polaroid src="img/cuon_caosu.jpg" label="Thảm cao su" start={s + 12} end={DURATION + 1} x={700} y={G - 60} w={240} h={240} rot={6} />
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
        <SeriesTag start={f(3.1)} end={VIDEO_FRAMES} tag="Mẹo dùng thảm" brand="Louis Yoga" />
        <AlcoholScene />
        <RubberScene />
        <MatchScene />
        <DamageScene />
        <BestScene />
        <NuanceScene />
        <AdviceScene />
        <CheckList
          items={[
            ["Hạn chế lau cồn", 50.3],
            ["Tránh phơi nắng gắt", 51.34],
            ["Dùng xịt chuyên dụng", 52.4],
            ["Hỏi nhà sản xuất", 53.3],
          ]}
          start={f(50.2)}
          end={f(54.05)}
          y={G - 20}
        />
        <Captions lines={CAPTIONS} y={CAP_Y} from={2.6} until={CLEAN_DURATION} />
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
