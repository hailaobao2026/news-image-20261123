#!/usr/bin/env python3
"""news-image-20261123: draw Monday 23 November 2026's world news as a
one-page newspaper front page, 1024x1024, with Pillow only.

Run:  python3 main.py            (writes /output/entry.png, or
       $MAKEFUN_OUTPUT_DIR/entry.png when set)
The picture is fully deterministic: no randomness, no clock, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 227)   # warm newsprint
INK = (25, 25, 25)
RED = (179, 39, 30)
NAVY = (30, 74, 110)
TEAL = (38, 110, 96)
AMBER = (198, 124, 22)
GREY = (104, 104, 100)
LIGHT = (233, 226, 208)
WHITE = (252, 250, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def centre(draw, y, text, fnt, color, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=color)
    return y


def rule(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- art panels
def art_globe(d, x, y, w, h):
    """A warming globe under grey smoke, with a red NO DEAL ribbon."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240), outline=NAVY, width=3)
    cx, cy, r = x + w // 2, y + h // 2 + 8, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 205),
              outline=NAVY, width=3)
    for k in (1, 2):  # meridians as nested ellipses
        d.ellipse([cx - r + k * 20, cy - r, cx + r - k * 20, cy + r],
                  outline=NAVY, width=2)
    d.line([cx, cy - r, cx, cy + r], fill=NAVY, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    d.arc([cx - r, cy - r - 34, cx + r, cy + r - 34], 30, 150,
          fill=NAVY, width=2)
    d.arc([cx - r, cy - r + 34, cx + r, cy + r + 34], 210, 330,
          fill=NAVY, width=2)
    # land blobs
    d.ellipse([cx - 42, cy - 38, cx - 8, cy - 8], fill=(96, 150, 92))
    d.ellipse([cx + 6, cy + 6, cx + 44, cy + 40], fill=(96, 150, 92))
    d.ellipse([cx + 14, cy - 44, cx + 40, cy - 22], fill=(96, 150, 92))
    # smoke plumes
    for sx, sy, sr in [(x + 34, y + 26, 13), (x + 62, y + 16, 10),
                       (x + w - 40, y + 22, 12), (x + w - 66, y + 14, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 116))
    # red ribbon
    d.rectangle([x, y + h - 34, x + w, y + h], fill=RED)
    centre(d, y + h - 30, "NO DEAL", SANS_B(22), WHITE, cx=x + w // 2)


def art_badge(d, x, y, w, h):
    """A law-enforcement star badge over dark blue."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 58, 94), outline=NAVY, width=3)
    cx, cy = x + w // 2, y + h // 2 - 6
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 52 if i % 2 == 0 else 22
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 184, 64), outline=(120, 86, 20))
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(31, 58, 94))
    d.text((cx - 5, cy - 11), "10", font=SANS_B(18), fill=WHITE)
    centre(d, y + h - 30, "FBI TOP 10", SANS_B(16), WHITE, cx=x + w // 2)


def art_ship(d, x, y, w, h):
    """A ship on waves under an orange explosion burst."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 222, 235), outline=NAVY, width=3)
    # explosion burst
    import math
    bx, by = x + w - 42, y + 40
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = 34 if i % 2 == 0 else 16
        pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 140, 32), outline=(179, 39, 30))
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(250, 210, 90))
    # hull
    d.polygon([(x + 18, y + h - 62), (x + w - 30, y + h - 62),
               (x + w - 52, y + h - 34), (x + 38, y + h - 34)],
              fill=(60, 60, 64), outline=INK)
    d.rectangle([x + 48, y + h - 92, x + 76, y + h - 62], fill=(120, 60, 50))
    d.line([x + 62, y + h - 118, x + 62, y + h - 92], fill=INK, width=3)
    # waves
    for wy in (y + h - 26, y + h - 12):
        for k in range(4):
            d.arc([x + 8 + k * 34, wy - 8, x + 34 + k * 34, wy + 8],
                  180, 360, fill=NAVY, width=3)


def art_capitol(d, x, y, w, h):
    """A capitol dome with a big 258 beneath it."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240), outline=NAVY, width=3)
    cx = x + w // 2
    d.rectangle([cx - 46, y + 58, cx + 46, y + 92], fill=WHITE, outline=INK, width=2)
    d.pieslice([cx - 40, y + 12, cx + 40, y + 62], 180, 360,
               fill=WHITE, outline=INK, width=2)
    d.line([cx, y + 2, cx, y + 14], fill=INK, width=3)
    d.polygon([(cx, y + 2), (cx + 12, y + 7), (cx, y + 12)], fill=RED)
    for k in (-30, -10, 10, 30):
        d.rectangle([cx + k - 4, y + 62, cx + k + 4, y + 92], fill=INK)
    centre(d, y + h - 34, "258 SEATS", SANS_B(20), NAVY, cx=cx)


def art_factory(d, x, y, w, h):
    """A factory with flames and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 224, 200), outline=NAVY, width=3)
    # sawtooth factory
    d.polygon([(x + 14, y + h - 30), (x + 14, y + 78), (x + 44, y + 58),
               (x + 74, y + 78), (x + 104, y + 58), (x + w - 16, y + 78),
               (x + w - 16, y + h - 30)], fill=(150, 90, 70), outline=INK)
    d.rectangle([x + w - 42, y + 34, x + w - 28, y + 78], fill=(110, 70, 60))
    # flames
    for fx, fh in [(x + 30, 34), (x + 62, 44), (x + 94, 30)]:
        d.polygon([(fx - 12, y + 78), (fx, y + 78 - fh), (fx + 12, y + 78)],
                  fill=(232, 120, 30), outline=(179, 39, 30))
        d.polygon([(fx - 6, y + 78), (fx, y + 78 - fh + 14), (fx + 6, y + 78)],
                  fill=(250, 210, 90))
    # smoke
    for sx, sy, sr in [(x + 26, y + 22, 10), (x + 48, y + 12, 8),
                       (x + w - 36, y + 18, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 106))


def art_drone(d, x, y, w, h):
    """A quadcopter drone over a pale UN-blue field."""
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 240), outline=NAVY, width=3)
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 34, cy - 14, cx + 34, cy + 14], fill=(70, 70, 76))
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=RED)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * 52, cy + sy * 26
            d.line([cx + sx * 30, cy + sy * 12, ax, ay], fill=INK, width=3)
            d.ellipse([ax - 20, ay - 4, ax + 20, ay + 4], fill=(160, 160, 156))
    d.line([cx, cy - 14, cx, cy - 34], fill=INK, width=3)
    d.ellipse([cx - 4, cy - 40, cx + 4, cy - 32], fill=RED)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead
    centre(d, 30, "THE WORLD IN ONE DAY", SERIF_B(52), INK)
    rule(d, M + 120, W - M - 120, 96, RED, 3)
    centre(d, 106, "MONDAY  ·  23 NOVEMBER 2026", SANS_B(30), RED)
    centre(d, 142, "Six stories that defined the day — and three more below",
           SANS(17), GREY)

    # ---- lead story: COP31
    ly = 178
    art_globe(d, M, ly, 300, 196)
    tx = M + 318
    d.text((tx, ly + 2), "CLIMATE  ·  ANTALYA, TURKEY", font=SANS_B(16), fill=TEAL)
    d.text((tx, ly + 28), "COP31 COLLAPSES", font=SANS_B(46), fill=INK)
    para(d, tx, ly + 88,
         "Two weeks of climate talks end with no deal. The final text never "
         "even mentions fossil fuels — the longest COP ever, and the first "
         "collapse since 2009.", SANS(19), INK, W - M - tx, 26)
    rule(d, M, W - M, ly + 208, INK, 2)

    # ---- 2 x 2 grid, stories 2-5
    gy, gh, gw, gap = 398, 158, 476, 12
    cells = [
        (art_badge, "MEXICO  ·  SINALOA", "“EL CHAPO ISIDRO” CAPTURED",
         "FBI most-wanted cartel boss Fausto Isidro Meza Flores seized in a "
         "night raid; 11 killed as gunmen fought back."),
        (art_ship, "WAR AT SEA  ·  LIBYA & THE BALTIC", "RUSSIAN SHIPS HIT FAR FROM HOME",
         "Ukrainian sea drones sink the corvette Merkury off Libya and set "
         "the cargo ship Sparta II ablaze off Finland."),
        (art_capitol, "USA  ·  MIDTERMS", "DEMOCRATS’ RECORD HOUSE WIN",
         "258 seats — the biggest majority since 1992 — as North Carolina "
         "seals a 44-seat sweep of the House."),
        (art_factory, "INDONESIA  ·  NEAR JAKARTA", "FACTORY FIRE: DOZENS MISSING",
         "At least 3 dead after a candy factory burns in Banten; rescuers "
         "search the wreckage for missing workers."),
    ]
    for i, (art, kick, head, sub) in enumerate(cells):
        cx0 = M + (i % 2) * (gw + gap)
        cy0 = gy + (i // 2) * (gh + gap)
        d.rectangle([cx0, cy0, cx0 + gw, cy0 + gh], outline=INK, width=2)
        art(d, cx0 + 8, cy0 + 8, 140, gh - 16)
        tx = cx0 + 160
        d.text((tx, cy0 + 10), kick, font=SANS_B(13), fill=TEAL)
        y = para(d, tx, cy0 + 30, head, SANS_B(21), INK, gw - 172, 25)
        para(d, tx, y + 2, sub, SANS(15), (60, 60, 60), gw - 172, 19)

    # ---- bottom band: story 6 + ALSO TODAY
    by = 738
    bw = 476
    d.rectangle([M, by, M + bw, by + 190], outline=INK, width=2)
    art_drone(d, M + 8, by + 8, 140, 174)
    tx = M + 160
    d.text((tx, by + 12), "UNITED NATIONS  ·  GENEVA", font=SANS_B(13), fill=TEAL)
    y = para(d, tx, by + 32, "KILLER-ROBOT TALKS LIVE ON", SANS_B(21), INK,
             bw - 172, 25)
    para(d, tx, y + 2,
         "128 nations agree to two more years of talks on lethal autonomous "
         "weapons — but no binding treaty, as the US, Russia and Israel hold "
         "out.", SANS(15), (60, 60, 60), bw - 172, 19)

    ax0 = M + bw + gap
    d.rectangle([ax0, by, ax0 + bw, by + 190], fill=LIGHT, outline=INK, width=2)
    d.text((ax0 + 14, by + 10), "ALSO TODAY", font=SANS_B(20), fill=RED)
    items = [
        ("NEPAL IN DELHI —", "PM Balendra Shah holds talks with Narendra Modi on a state visit."),
        ("SEOUL —", "Education minister quits over an AI exam-cheating scandal."),
        ("LAS VEGAS GP —", "Verstappen wins a chaotic race as the Ferraris clash."),
    ]
    yy = by + 42
    for lead, rest in items:
        yy = para(d, ax0 + 14, yy, lead + " " + rest, SANS(15), INK,
                  bw - 28, 19)
        yy += 8

    # ---- footer
    rule(d, M, W - M, 944, INK, 2)
    centre(d, 956, "Sources: AP · Reuters · CNN · WSJ · Le Monde · The Times · AFP",
           SANS(14), GREY)
    centre(d, 978, "Drawn entirely with code — no photograph, no AI image",
           SANS(13), GREY)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.png")
    img.save(path, "PNG", optimize=True)
    os.chmod(path, 0o644)
    print("wrote", path)


if __name__ == "__main__":
    main()
