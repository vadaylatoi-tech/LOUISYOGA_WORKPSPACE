"""Composite product PNGs over the approved square background without altering the mat."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def remove_connected_white(img: Image.Image) -> Image.Image:
    """Make near-white pixels connected to image edges transparent; retain mat pixels."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    pix = rgb.load()
    candidate = Image.new("L", (w, h), 0)
    cp = candidate.load()
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            if min(r, g, b) >= 238 and max(r, g, b) - min(r, g, b) <= 24:
                cp[x, y] = 255
    # Flood fill connected near-white edge regions. Threshold 0 means exact binary match.
    for x in range(w):
        for y in (0, h - 1):
            if cp[x, y] == 255:
                ImageDraw.floodfill(candidate, (x, y), 128, thresh=0)
    for y in range(h):
        for x in (0, w - 1):
            if cp[x, y] == 255:
                ImageDraw.floodfill(candidate, (x, y), 128, thresh=0)

    # Start from a distance-to-white matte so antialiased edge pixels blend cleanly.
    alpha = Image.new("L", (w, h))
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if cp[x, y] == 128:
                ap[x, y] = 0
                continue
            r, g, b = pix[x, y]
            distance = 255 - min(r, g, b)
            ap[x, y] = max(0, min(255, int(distance * 255 / 50)))
    # Slightly soften only the alpha edge; source RGB remains unchanged.
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.45))
    rgba = rgb.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def composite(source: Path, background: Path, output: Path, canvas_size: int = 1254) -> None:
    bg = Image.open(background).convert("RGB").resize((canvas_size, canvas_size), Image.Resampling.LANCZOS)
    mat = remove_connected_white(Image.open(source))
    bbox = mat.getbbox()
    if not bbox:
        raise ValueError(f"No product found after background removal: {source}")
    mat = mat.crop(bbox)
    target_h = round(canvas_size * 0.90)
    target_w = round(mat.width * target_h / mat.height)
    mat = mat.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (canvas_size - target_w) // 2
    y = round(canvas_size * 0.05)

    # Add a soft silhouette shadow and a clearer horizontal contact shadow at the foot.
    shadow_alpha = Image.new("L", (canvas_size, canvas_size), 0)
    shadow_shape = Image.new("L", mat.size, 0)
    shadow_shape.paste(mat.getchannel("A"))
    shadow_alpha.paste(shadow_shape, (x, y + 3))
    shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(8)).point(lambda a: int(a * 0.16))
    contact = Image.new("L", (canvas_size, canvas_size), 0)
    contact_draw = ImageDraw.Draw(contact)
    foot = y + target_h
    contact_draw.ellipse((x - 62, foot - 7, x + target_w + 62, foot + 22), fill=150)
    contact = contact.filter(ImageFilter.GaussianBlur(11))
    shadow_alpha = Image.frombytes("L", shadow_alpha.size, bytes(max(a, b) for a, b in zip(shadow_alpha.tobytes(), contact.tobytes())))
    shadow = Image.new("RGB", (canvas_size, canvas_size), (45, 45, 45))
    bg.paste(shadow, (0, 0), shadow_alpha)
    bg.paste(mat, (x, y), mat)
    output.parent.mkdir(parents=True, exist_ok=True)
    bg.save(output, "JPEG", quality=94, optimize=True, subsampling=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("background", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    composite(args.source, args.background, args.output)
    print("Avatar exported")
