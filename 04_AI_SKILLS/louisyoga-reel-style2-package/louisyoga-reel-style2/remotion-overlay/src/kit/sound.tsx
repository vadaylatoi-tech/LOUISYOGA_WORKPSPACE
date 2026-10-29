import React from "react";
import { Audio, getInputProps, interpolate, Sequence, staticFile } from "remotion";
import { clamp, f } from "./theme";

// Audio stems: "all" = preview with the footage's own voice; "sfx" / "music" are rendered alone
// (`--props '{"stem":"sfx"}' --codec=wav`) and mixed with the PROCESSED voice by scripts/mix_stems.py.
// "none" = silent (use with --muted for the picture render).
export type Stem = "all" | "sfx" | "music" | "none";
export const STEM = ((getInputProps() as { stem?: string }).stem ?? "all") as Stem;

// Seconds of lead-in before each file's transient (measured), so the hit lands on the cue time.
export const ONSET: Record<string, number> = {
  "swoosh.mp3": 0.07,
  "quick-swoosh.mp3": 0.04,
  "pop.mp3": 0.23,
  "pop-2.mp3": 0.066,
  "punch.mp3": 0.107,
  "riser-metallic.mp3": 1.809,
  "camera-shutter.mp3": 0.04,
  "digital-counting-1.mp3": 0.063,
  "ding.mp3": 0.149,
  "quick-ting.mp3": 0.019,
  "correct.mp3": 0.079,
  // style 2 (bright "attention" sounds from 03_MEDIA_LIBRARY/shared-sources/sound-effects; glitch.mp3 starts at once)
  "glasses-cheers-2.wav": 0.49,
  "ting.wav": 0.97,
  "new-item.wav": 0.65,
};

// [time s where the hit should land, file in public/sfx, volume]
export type Cue = [number, string, number];

// Music volume keyframes: [frame, volume] pairs (light under the voice; louder in hook and CTA tail).
export type MusicCurve = [number[], number[]];

export const SoundLayer: React.FC<{ cues: Cue[]; music: string; curve: MusicCurve }> = ({ cues, music, curve }) => (
  <>
    {(STEM === "all" || STEM === "music") && (
      <Audio src={staticFile(music)} volume={(fr) => interpolate(fr, curve[0], curve[1], clamp)} />
    )}
    {(STEM === "all" || STEM === "sfx") &&
      cues.map(([t, file, vol], i) => {
        // A sound whose lead-in is longer than t (e.g. the riser) is trimmed from the front instead.
        const from = f(t - (ONSET[file] ?? 0));
        return (
          <Sequence key={i} from={Math.max(0, from)} durationInFrames={f(3)} layout="none">
            <Audio src={staticFile(`sfx/${file}`)} startFrom={Math.max(0, -from)} volume={vol} />
          </Sequence>
        );
      })}
  </>
);
