import { MyComposition } from "./Composition";
import { SmokeTestComposition } from "./smoke-test/SmokeTest";
import { LouisYogaTVCComposition } from "./tvc/LouisYogaTVC";
import { LouisYogaReel2Composition } from "./reel2/LouisYogaReel2";
import { LouisYogaReel3Composition } from "./reel3/LouisYogaReel3";
import { ReelsChonThamLayoutDraft } from "./reels-chon-tham/LayoutDraft";
import { ReelsChonThamComposition } from "./reels-chon-tham/ReelsChonTham";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      <SmokeTestComposition />
      <LouisYogaTVCComposition />
      <LouisYogaReel2Composition />
      <LouisYogaReel3Composition />
      <ReelsChonThamLayoutDraft />
      <ReelsChonThamComposition />
    </>
  );
};
