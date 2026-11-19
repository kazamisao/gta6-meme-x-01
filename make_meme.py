"""Render the gta6-meme-x-01 meme with Pillow (supersampled 3x, flat vector style).

Scene: a Vice City beach at sunset. make.fun's ghost stands on the sand holding
its magenta star coin up high, a sick note in its other hand.
Caption: "SICK DAY FOR GTA 6." / "MY AGENT'S STILL EARNING."
The ghost is drawn from primitives (no downloaded logo or image is used):
white body, thick black outline, two black four-pointed sparkle eyes, a round
little hand, magenta coin with a white star.

Run: python3 make_meme.py   -> writes meme.png (1200x1200) next to this file.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 3                      # supersample factor
W = H = 1200 * S           # working canvas
OUT = Path(__file__).resolve().parent / "meme.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Palette
PURPLE = (43, 16, 85)
MAGENTA = (255, 46, 136)
ORANGE = (255, 154, 61)
PALE = (255, 233, 168)
TEAL = (16, 120, 140)
TEAL_DARK = (10, 88, 110)
SAND = (238, 205, 150)
SAND_DARK = (222, 182, 122)
BLACK = (10, 10, 12)
WHITE = (255, 255, 255)
COIN = (233, 30, 140)
PALM = (24, 60, 44)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def font(size):
    return ImageFont.truetype(BOLD, int(size * S))


def fit_font(text, max_w, start_size):
    size = start_size
    while size > 20:
        f = font(size)
        if f.getlength(text) <= max_w * S:
            return f
        size -= 4
    return font(20)


def text_centered(d, y, text, f, fill, outline_w):
    d.text((W / 2, y), text, font=f, fill=fill, anchor="ma",
           stroke_width=int(outline_w * S), stroke_fill=BLACK)


def star4(cx, cy, r, w):
    """Four-pointed sparkle: points N/E/S/W at r, concave corners at w."""
    return [(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w),
            (cx, cy + r), (cx - w, cy + w), (cx - r, cy), (cx - w, cy - w)]


def star5(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ghost_body_points(cx, top, width, bottom):
    """Outline of a classic ghost: domed top, straight sides, 3-scallop hem."""
    hw = width / 2
    pts = []
    # dome: semicircle from left shoulder over the top to right shoulder
    for i in range(0, 25):
        a = math.pi + i * (math.pi / 24)  # pi -> 2pi
        pts.append((cx + hw * math.cos(a), top + hw + hw * math.sin(a)))
    shoulder_y = top + hw
    # right side down to hem
    pts.append((cx + hw, bottom))
    # hem: three upward scallops, right to left
    n = 3
    seg = width / n
    for k in range(n):
        x_right = cx + hw - k * seg
        x_left = x_right - seg
        x_mid = (x_right + x_left) / 2
        for i in range(1, 13):
            a = i * (math.pi / 12)  # 0 -> pi, arc bulging upward
            pts.append((x_right - seg * i / 12,
                        bottom - (seg / 2) * math.sin(a) * 0.9))
    # left side back up
    pts.append((cx - hw, shoulder_y))
    return pts


def draw_palm(d, base_x, base_y, lean, height, flip):
    """Simple flat palm silhouette: curved trunk + 6 fronds.
    All inputs are in final (1200px) coordinates; scaled here."""
    base_x, base_y, lean, height = base_x * S, base_y * S, lean * S, height * S
    top_x = base_x + lean
    top_y = base_y - height
    # trunk: tapered polygon
    d.polygon([(base_x - 26 * S, base_y), (base_x + 26 * S, base_y),
               (top_x + 14 * S, top_y), (top_x - 14 * S, top_y)], fill=PALM)
    # fronds: bent lines that rise from the crown, then droop down
    for sx, dy in ((-1, -70), (-1, -10), (-1, 60), (1, -70), (1, -10), (1, 60)):
        if flip:
            sx = -sx
        mid = (top_x + sx * 110 * S, top_y + (dy - 60) * S)
        tip = (top_x + sx * 200 * S, top_y + (dy + 70) * S)
        d.line([(top_x, top_y), mid, tip], fill=PALM, width=int(20 * S),
               joint="curve")
        d.ellipse([tip[0] - 12 * S, tip[1] - 12 * S,
                   tip[0] + 12 * S, tip[1] + 12 * S], fill=PALM)
    # coconuts
    d.ellipse([top_x - 30 * S, top_y + 6 * S, top_x - 2 * S, top_y + 34 * S], fill=PALM)
    d.ellipse([top_x + 2 * S, top_y + 6 * S, top_x + 30 * S, top_y + 34 * S], fill=PALM)


def main():
    img = Image.new("RGB", (W, H), PURPLE)
    d = ImageDraw.Draw(img)

    # --- sky gradient: purple -> magenta -> orange -> pale ---
    horizon = int(640 * S)
    for y in range(horizon):
        t = y / horizon
        if t < 0.45:
            c = lerp(PURPLE, MAGENTA, t / 0.45)
        elif t < 0.8:
            c = lerp(MAGENTA, ORANGE, (t - 0.45) / 0.35)
        else:
            c = lerp(ORANGE, PALE, (t - 0.8) / 0.2)
        d.line([(0, y), (W, y)], fill=c)

    # --- clouds: two flat white blobs (tightly overlapping ellipses) ---
    for cx, cy, cw in ((300, 300, 200), (950, 260, 220)):
        cx, cy, cw = cx * S, cy * S, cw * S
        for dx, dy, r in ((-cw // 4, 0, 42), (0, -14, 52), (cw // 4, 0, 42)):
            d.ellipse([cx + dx - r * S, cy + dy * S - r * S,
                       cx + dx + r * S, cy + dy * S + r * S],
                      fill=(255, 240, 235))

    # --- sun + glow (left of the ghost, so the disc stays visible) ---
    sun_cx, sun_cy, sun_r = 280 * S, 590 * S, 120 * S
    for r, col in ((230, (255, 200, 120)), (190, (255, 220, 150))):
        d.ellipse([sun_cx - r * S, sun_cy - r * S, sun_cx + r * S, sun_cy + r * S],
                  fill=col)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=PALE)

    # --- ocean ---
    d.rectangle([0, horizon, W, int(830 * S)], fill=TEAL)
    for i, y in enumerate((680, 720, 760, 800)):
        d.line([(0, y * S), (W, y * S)], fill=TEAL_DARK, width=int(6 * S))
        # sun reflection dashes (under the sun, left of centre)
        for x in range(200, 380, 46):
            d.line([(x * S, y * S), ((x + 26) * S, y * S)],
                   fill=(255, 230, 170), width=int(7 * S))

    # --- sand ---
    d.rectangle([0, int(830 * S), W, H], fill=SAND)
    for x in range(60, W, 240 * S):
        d.ellipse([x, int(900 * S), x + 90 * S, int(915 * S)], fill=SAND_DARK)

    # --- palms at the edges ---
    draw_palm(d, 110, 850, 70, 380, flip=False)
    draw_palm(d, 1090, 850, -70, 380, flip=True)

    # --- ghost: centre, standing on the sand ---
    gx, gtop, gw, gbot = 600 * S, 400 * S, 430 * S, 990 * S
    pts = ghost_body_points(gx, gtop, gw, gbot)
    d.polygon(pts, fill=WHITE, outline=BLACK, width=int(14 * S))

    # sparkle eyes
    eye_y = int(560 * S)
    for ex in (gx - 78 * S, gx + 78 * S):
        d.polygon(star4(ex, eye_y, 52 * S, 15 * S), fill=BLACK)

    # left hand holding the sick note (small white slip, tilted)
    note = Image.new("RGBA", (260 * S, 190 * S), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rounded_rectangle([6 * S, 6 * S, 254 * S, 184 * S], radius=18 * S,
                         fill=WHITE, outline=BLACK, width=int(8 * S))
    nf = font(34)
    nd.text((130 * S, 42 * S), "SICK", font=nf, fill=BLACK, anchor="ma")
    nd.text((130 * S, 92 * S), "NOTE", font=nf, fill=BLACK, anchor="ma")
    for ly in (140, 160):
        nd.line([(30 * S, ly * S), (230 * S, ly * S)], fill=(150, 150, 150),
                width=int(5 * S))
    note = note.rotate(-14, resample=Image.BICUBIC, expand=True)
    img.paste(note, (int(gx - 400 * S), int(760 * S)), note)

    # right arm + round hand raised, holding the magenta coin
    coin_cx, coin_cy, coin_r = int(880 * S), int(430 * S), 78 * S
    d.line([(gx + 150 * S, int(700 * S)), (coin_cx - 30 * S, coin_cy + 30 * S)],
           fill=BLACK, width=int(46 * S))
    d.line([(gx + 150 * S, int(700 * S)), (coin_cx - 30 * S, coin_cy + 30 * S)],
           fill=WHITE, width=int(30 * S))
    d.ellipse([coin_cx - 34 * S, coin_cy + 6 * S, coin_cx + 34 * S, coin_cy + 74 * S],
              fill=WHITE, outline=BLACK, width=int(10 * S))
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
              fill=COIN, outline=BLACK, width=int(12 * S))
    d.polygon(star5(coin_cx, coin_cy, 52 * S, 21 * S), fill=WHITE)

    # --- captions ---
    f_top = fit_font("SICK DAY FOR GTA 6.", 1080, 118)
    text_centered(d, 58 * S, "SICK DAY FOR GTA 6.", f_top, WHITE, 10)
    f_bot = fit_font("MY AGENT'S STILL EARNING.", 1080, 96)
    text_centered(d, 995 * S, "MY AGENT'S STILL EARNING.", f_bot, WHITE, 9)

    # --- make.fun pill, bottom centre ---
    pill_w, pill_h = 340 * S, 92 * S
    px0, py0 = (W - pill_w) / 2, H - pill_h - 28 * S
    d.rounded_rectangle([px0, py0, px0 + pill_w, py0 + pill_h], radius=46 * S,
                        fill=MAGENTA, outline=BLACK, width=int(8 * S))
    f_pill = font(62)
    d.text((W / 2, py0 + pill_h / 2), "make.fun", font=f_pill, fill=WHITE,
           anchor="mm")

    img = img.resize((1200, 1200), Image.LANCZOS)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
