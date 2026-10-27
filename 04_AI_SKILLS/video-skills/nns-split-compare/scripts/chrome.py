# -*- coding: utf-8 -*-
"""Ve 2 lop giao dien PNG (RGBA) — moi pha 1 lop.

Lop nay chua TAT CA tru pixel cua video dang chay: nen, luoi, nhan, badge VS,
badge AI, pill thoi luong, vien + glow, VA CA khung dung hinh (da lam toi) cua
ben khong chay. Cho video dang chay la mot LO trong suot bo goc -> goc bo cua
khung dang chay do chinh lop nay che, khong can mask rieng trong ffmpeg.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def _pil():
    try:
        from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
        return Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
    except Exception:
        C.die("Thieu Pillow. Cai:  pip install Pillow")


def grab_frame(video, index, out_png):
    """Trich DUNG frame thu `index` (0-based).

    Dung select=eq(n\\,N), KHONG dung -ss: fast seek nhay sai frame tren file
    co B-frame — cai bay nay da lam hong verify cua nns-cut-silence mot lan.
    """
    C.need_tool("ffmpeg")
    C.run(["ffmpeg", "-y", "-v", "error", "-i", video,
           "-vf", "select=eq(n\\,%d)" % index, "-fps_mode", "passthrough",
           "-frames:v", "1", out_png])
    if not os.path.isfile(out_png):
        C.die("Khong trich duoc frame %d cua %s" % (index, video))
    return out_png


def _dim(img, ImageEnhance):
    img = ImageEnhance.Color(img).enhance(C.DIM_SAT)
    return ImageEnhance.Brightness(img).enhance(C.DIM_BRIGHT)


def _fade(rgba, k):
    r, g, b, a = rgba
    return (r, g, b, int(a * k))


def _star(d, cx, cy, r, color):
    """Sao 4 canh ve tay — khong dua vao glyph U+2726, font co the khong co."""
    t = r * 0.30
    d.polygon([(cx, cy - r), (cx + t, cy - t), (cx + r, cy), (cx + t, cy + t),
               (cx, cy + r), (cx - t, cy + t), (cx - r, cy), (cx - t, cy - t)],
              fill=color)


def build(plan, active, frozen_png, fonts, outfile):
    """active: 'left' hoac 'right' — ben dang CHAY (duoc duc lo trong suot)."""
    Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont = _pil()
    f_label, f_pill, f_vs = fonts["label"], fonts["pill"], fonts["vs"]

    base = Image.new("RGBA", (C.W, C.H), C.BG)
    d = ImageDraw.Draw(base, "RGBA")

    for x in range(0, C.W, C.GRID_STEP):
        d.line([(x, 0), (x, C.H)], fill=C.GRID, width=1)
    for y in range(0, C.H, C.GRID_STEP):
        d.line([(0, y), (C.W, y)], fill=C.GRID, width=1)

    lx, rx, py = C.LEFT_X, C.RIGHT_X, C.PANEL_Y
    pw, ph, rad = C.PANEL_W, C.PANEL_H, C.RADIUS
    box_l = [lx, py, lx + pw, py + ph]
    box_r = [rx, py, rx + pw, py + ph]
    box_active = box_l if active == "left" else box_r
    box_frozen = box_r if active == "left" else box_l

    # glow quanh khung dang chay: ve tren lop rieng roi blur, khong ve thang
    glow = Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for grow, alpha in ((16, 70), (8, 110), (2, 160)):
        gd.rounded_rectangle([box_active[0] - grow, box_active[1] - grow,
                              box_active[2] + grow, box_active[3] + grow],
                             radius=rad + grow, width=6,
                             outline=_fade(C.YELLOW, alpha / 255.0))
    base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(base, "RGBA")

    # khung DUNG HINH: dan frame da lam toi, bo goc bang mask
    fr = Image.open(frozen_png).convert("RGB").resize((pw, ph), Image.LANCZOS)
    fr = _dim(fr, ImageEnhance).convert("RGBA")
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=rad, fill=255)
    base.paste(fr, (box_frozen[0], box_frozen[1]), mask)
    d.rounded_rectangle(box_frozen, radius=rad, outline=C.DIM_BORDER, width=3)
    d.rounded_rectangle(box_active, radius=rad, outline=C.YELLOW, width=5)

    a_l = 1.0 if active == "left" else C.DIM_UI_ALPHA
    a_r = 1.0 if active == "right" else C.DIM_UI_ALPHA

    d.text((lx + pw // 2, C.LABEL_CY), plan["left"]["label"], font=f_label,
           fill=_fade(C.WHITE, a_l), anchor="mm")
    if active == "right":
        gl = Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).text((rx + pw // 2, C.LABEL_CY), plan["right"]["label"],
                                font=f_label, fill=_fade(C.YELLOW, 0.55), anchor="mm")
        base = Image.alpha_composite(base, gl.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(base, "RGBA")
    d.text((rx + pw // 2, C.LABEL_CY), plan["right"]["label"], font=f_label,
           fill=_fade(C.YELLOW, a_r), anchor="mm")

    # badge VS o giua 2 khung
    cx, cy = C.W // 2, py + ph // 2
    d.ellipse([cx - C.VS_R, cy - C.VS_R, cx + C.VS_R, cy + C.VS_R],
              fill=C.VS_BG, outline=C.VS_BORDER, width=3)
    d.text((cx, cy + 1), "VS", font=f_vs, fill=C.WHITE, anchor="mm")

    def pill(text, cx_, bg, fg, alpha):
        w = int(d.textlength(text, font=f_pill) + 56)
        x0, y0 = cx_ - w // 2, C.PILL_Y
        d.rounded_rectangle([x0, y0, x0 + w, y0 + C.PILL_H], radius=C.PILL_H // 2,
                            fill=_fade(bg, alpha))
        d.text((cx_, y0 + C.PILL_H // 2 + 1), text, font=f_pill,
               fill=_fade(fg, alpha), anchor="mm")

    pill(plan["left"]["pill"], lx + pw // 2, C.PILL_GREY_BG, C.PILL_GREY_FG, a_l)
    pill(plan["right"]["pill"], rx + pw // 2, C.YELLOW, C.PILL_YEL_FG, a_r)

    # DUC LO trong suot cho khung dang chay.
    # Phai duc TRUOC khi ve badge AI: badge nam BEN TRONG khung phai, neu duc sau
    # thi o pha 2 (phai dang chay) lo se xoa mat badge — da dinh loi nay 1 lan.
    ImageDraw.Draw(base).rounded_rectangle(box_active, radius=rad, fill=(0, 0, 0, 0))

    # badge AI goc tren khung phai — ve SAU cung, de len ca lo
    bt, bh = "AI", C.AI_BADGE_H
    bw = int(d.textlength(bt, font=f_pill) + bh * 1.55)
    bx, by = rx + 20, py + 20
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2,
                        fill=_fade(C.YELLOW, a_r))
    _star(d, bx + bh * 0.52, by + bh / 2, bh * 0.24, _fade(C.PILL_YEL_FG, a_r))
    d.text((bx + bh * 0.92, by + bh / 2 + 1), bt, font=f_pill,
           fill=_fade(C.PILL_YEL_FG, a_r), anchor="lm")

    base.save(outfile)
    return outfile


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--resources", default=None)
    a = ap.parse_args()

    C.head("CHROME (ve giao dien)")
    plan = C.load_json(a.plan)
    os.makedirs(a.outdir, exist_ok=True)

    fdir = C.font_dir(a.resources)
    if not fdir:
        C.die("Khong thay font Be Vietnam Pro. Chay preflight.py de xem huong dan.")
    Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont = _pil()
    fonts = {
        "label": ImageFont.truetype(C.font_file(fdir, "Black"), C.LABEL_SIZE),
        "pill": ImageFont.truetype(C.font_file(fdir, "Bold"), C.PILL_TEXT),
        "vs": ImageFont.truetype(C.font_file(fdir, "Black"), C.VS_TEXT),
    }

    # Pha 1: trai chay -> khung phai dung hinh o FRAME DAU cua ban AI
    # Pha 2: phai chay -> khung trai dung hinh o FRAME CUOI cua ban tho
    fz1 = grab_frame(plan["right"]["path"], 0,
                     os.path.join(a.outdir, "_frozen_right_first.png"))
    fz2 = grab_frame(plan["left"]["path"], plan["left"]["nframes"] - 1,
                     os.path.join(a.outdir, "_frozen_left_last.png"))

    p1 = build(plan, "left", fz1, fonts, os.path.join(a.outdir, "chrome_p1.png"))
    p2 = build(plan, "right", fz2, fonts, os.path.join(a.outdir, "chrome_p2.png"))
    print("    pha 1 -> %s" % p1)
    print("    pha 2 -> %s" % p2)
    print("")


if __name__ == "__main__":
    main()
