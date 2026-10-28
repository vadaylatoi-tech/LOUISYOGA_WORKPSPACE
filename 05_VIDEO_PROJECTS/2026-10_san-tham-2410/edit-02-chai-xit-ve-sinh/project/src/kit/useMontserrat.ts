import { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

// Montserrat variable font (SIL OFL), shipped in public/fonts.
export const MONTSERRAT = "MontserratLY";

export const useMontserrat = () => {
  const [handle] = useState(() => delayRender("Loading Montserrat"));
  useEffect(() => {
    const font = new FontFace(MONTSERRAT, `url(${staticFile("fonts/Montserrat-Variable.ttf")}) format("truetype")`, {
      weight: "100 900",
    });
    font
      .load()
      .then(() => {
        document.fonts.add(font);
        continueRender(handle);
      })
      .catch((err) => {
        console.error(err);
        continueRender(handle);
      });
  }, [handle]);
};
