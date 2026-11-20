"""Deterministic generator for entry.png: world news of Friday 20 November 2026.

Run: python make_image.py   (needs Pillow; fonts are bundled in ./fonts, SIL OFL)
Everything is drawn at 2x and downsampled; no randomness, no timestamps.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"
S, W = 2, 1024  # supersampling factor, canvas size

INK, PAPER, NAVY = "#0E1726", "#F3EFE6", "#0B1B33"
CRIMSON, YELLOW, WHITE, EDGE = "#B3171C", "#FFC93C", "#FFFFFF", "#D9D3C4"
XB, BD = "BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-Bold.ttf"
MED, SEMI = "Barlow-Medium.ttf", "Barlow-SemiBold.ttf"
CAP = 0.7  # Barlow cap height / em

img = Image.new("RGB", (W * S, W * S), PAPER)
d = ImageDraw.Draw(img)
boxes = []  # (label, x0, y0, x1, y1) of every checked text block, 1x units


def sc(v):
    return int(round(v * S))


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), sc(size))


def rect(x0, y0, x1, y1, fill, r=0, outline=None):
    d.rounded_rectangle([sc(x0), sc(y0), sc(x1) - 1, sc(y1) - 1], radius=sc(r), fill=fill,
                        outline=outline, width=sc(1.5) if outline else 0)


def poly(pts, fill):
    d.polygon([(sc(x), sc(y)) for x, y in pts], fill=fill)


def ell(cx, cy, r, fill=None, outline=None, w=0):
    d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)], fill=fill, outline=outline, width=sc(w))


def line(pts, fill, w):
    d.line([(sc(x), sc(y)) for x, y in pts], fill=fill, width=sc(w), joint="curve")


def wrap(text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if f.getlength(t) <= sc(max_w):
            cur = t
        elif not cur:
            return None  # a single word is wider than the box
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def fit(text, fname, size, min_size, max_w, max_lines):
    while size >= min_size:
        f = font(fname, size)
        lines = wrap(text, f, max_w)
        if lines and len(lines) <= max_lines:
            return f, lines, size
        size -= 1
    raise AssertionError(f"text does not fit: {text!r}")


def put(x, top, lines, f, size, fill, step, label, clip=None, spacing=0):
    """Draw lines with their cap-top at `top`; return bottom (baseline of last line)."""
    y = top + CAP * size
    for ln in lines:
        if spacing:
            cx = x
            for ch in ln:
                d.text((sc(cx), sc(y)), ch, font=f, fill=fill, anchor="ls")
                cx += f.getlength(ch) / S + spacing
            x1 = cx
            bb = (x, y - CAP * size, x1, y)
        else:
            d.text((sc(x), sc(y)), ln, font=f, fill=fill, anchor="ls")
            l, t, r, b = d.textbbox((sc(x), sc(y)), ln, font=f, anchor="ls")
            bb = (l / S, t / S, r / S, b / S)
        if clip:
            assert bb[0] >= clip[0] and bb[2] <= clip[2] and bb[3] <= clip[3], f"text leaves its box: {ln!r} {bb} {clip}"
        boxes.append((f"{label}:{ln}",) + tuple(bb))
        y += step
    return y - step


# ------------------------------------------------------------------ icons
def disc(ix, iy, tint):
    ell(ix + 42, iy + 42, 42, fill=tint)


def icon_tanker(ix, iy):
    disc(ix, iy, "#FFE8CC")
    poly([(ix + 10, iy + 54), (ix + 76, iy + 54), (ix + 66, iy + 70), (ix + 20, iy + 70)], "#343A40")
    rect(ix + 56, iy + 40, ix + 70, iy + 54, "#868E96")
    rect(ix + 14, iy + 48, ix + 52, iy + 54, "#C92A2A")
    poly([(ix + 36, iy + 48), (ix + 28, iy + 36), (ix + 35, iy + 32), (ix + 33, iy + 18),
          (ix + 44, iy + 30), (ix + 49, iy + 24), (ix + 50, iy + 38), (ix + 46, iy + 48)], "#F76707")
    poly([(ix + 38, iy + 48), (ix + 35, iy + 40), (ix + 41, iy + 36), (ix + 46, iy + 48)], YELLOW)


def icon_scales(ix, iy):
    disc(ix, iy, "#E5DBFF")
    c = "#5B34C4"
    line([(ix + 42, iy + 14), (ix + 42, iy + 66)], c, 4)
    rect(ix + 28, iy + 66, ix + 56, iy + 72, c)
    line([(ix + 14, iy + 24), (ix + 70, iy + 24)], c, 4)
    for cx in (14, 70):
        line([(ix + cx, iy + 24), (ix + cx - 9, iy + 48)], c, 2)
        line([(ix + cx, iy + 24), (ix + cx + 9, iy + 48)], c, 2)
        d.chord([sc(ix + cx - 12), sc(iy + 40), sc(ix + cx + 12), sc(iy + 58)], 0, 180, fill=c)


def icon_summit(ix, iy):
    disc(ix, iy, "#D0EBFF")
    pts = [(42, 20, "US", "#1864AB"), (17, 60, "CN", "#C92A2A"), (67, 60, "RU", "#495057")]
    line([(ix + 42, iy + 20), (ix + 17, iy + 60), (ix + 67, iy + 60), (ix + 42, iy + 20)], "#1864AB", 3)
    f = font(BD, 19)
    for x, y, t, col in pts:
        ell(ix + x, iy + y, 15, fill=col)
        d.text((sc(ix + x), sc(iy + y + 0.5)), t, font=f, fill=WHITE, anchor="mm")


def icon_cop(ix, iy):
    disc(ix, iy, "#D3F9D8")
    for cx, cy, r in ((29, 46, 13), (44, 38, 18), (58, 47, 12)):
        ell(ix + cx, iy + cy, r, fill="#495057")
    rect(ix + 29, iy + 46, ix + 58, iy + 59, "#495057")
    d.text((sc(ix + 43), sc(iy + 48)), "CO2", font=font(BD, 19), fill=WHITE, anchor="mm")
    poly([(ix + 20, iy + 66), (ix + 30, iy + 66), (ix + 25, iy + 74)], "#2B8A3E")
    poly([(ix + 50, iy + 66), (ix + 60, iy + 66), (ix + 55, iy + 74)], "#2B8A3E")


def icon_border(ix, iy):
    disc(ix, iy, "#C5F6FA")
    rect(ix + 14, iy + 26, ix + 26, iy + 70, "#343A40", r=2)
    rect(ix + 62, iy + 40, ix + 70, iy + 70, "#343A40", r=2)
    for i in range(5):
        x = ix + 26 + i * 7.2
        poly([(x, iy + 31), (x + 7.2, iy + 31), (x + 7.2, iy + 41), (x, iy + 41)], "#E03131" if i % 2 == 0 else WHITE)
    rect(ix + 26, iy + 31, ix + 62, iy + 41, None, outline="#343A40")
    ell(ix + 20, iy + 34, 3, fill=YELLOW)


def icon_strike(ix, iy):
    disc(ix, iy, "#FFDEEB")
    line([(ix + 24, iy + 14), (ix + 24, iy + 72)], "#343A40", 4)
    for i, col in enumerate(("#2F9E44", WHITE, "#E03131")):
        x = ix + 26 + i * 15
        poly([(x, iy + 18), (x + 15, iy + 18), (x + 15, iy + 48), (x, iy + 48)], col)
    rect(ix + 26, iy + 18, ix + 71, iy + 48, None, outline="#868E96")
    for k in (0, 1, 2):
        line([(ix + 10, iy + 56 + k * 5), (ix + 22, iy + 56 + k * 5)], "#A61E4D", 2)


def icon_globe(cx, cy):
    ell(cx, cy, 34, outline=WHITE, w=3)
    d.ellipse([sc(cx - 14), sc(cy - 34), sc(cx + 14), sc(cy + 34)], outline=WHITE, width=sc(2.5))
    line([(cx - 34, cy), (cx + 34, cy)], WHITE, 2.5)
    for dy in (-17, 17):
        hw = math.sqrt(34 ** 2 - dy ** 2)
        line([(cx - hw, cy + dy), (cx + hw, cy + dy)], WHITE, 2)


def icon_missile(cx, cy):
    for r, col in ((108, "#C2282D"), (78, "#D04A4F"), (50, "#E0777B")):
        ell(cx, cy, r, fill=col)
    ell(cx, cy, 24, fill=YELLOW)
    a = math.radians(-45)
    ca, sa = math.cos(a), math.sin(a)

    def tf(pts):  # local axis +x points to the tail; origin is the nose on the target
        return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]

    poly(tf([(8, 0), (38, -10), (125, -10), (125, 10), (38, 10)]), WHITE)
    poly(tf([(8, 0), (38, -10), (38, 10)]), "#7A0F13")
    poly(tf([(95, -10), (125, -28), (135, -28), (125, -10)]), "#CED4DA")
    poly(tf([(95, 10), (125, 28), (135, 28), (125, 10)]), "#CED4DA")
    poly(tf([(125, -6), (170, 0), (125, 6)]), "#F76707")
    poly(tf([(125, -3), (150, 0), (125, 3)]), YELLOW)


# ------------------------------------------------------------------ header
rect(0, 0, W, 108, NAVY)
f = font(BD, 27)
put(28, 14, ["WORLD NEWS IN ONE IMAGE"], f, 27, YELLOW, 0, "hdr-tag", clip=(0, 0, 880, 108), spacing=2.5)
f, lines, size = fit("FRIDAY 20 NOVEMBER 2026", XB, 74, 60, 860, 1)
put(28, 44, lines, f, size, WHITE, 0, "hdr-date", clip=(0, 0, 880, 106))
icon_globe(958, 54)

# ------------------------------------------------------------------ lead story
LEAD = (24, 118, 1000, 452)
rect(*LEAD, CRIMSON, r=18)
f = font(BD, 27)
put(48, 136, ["LEAD STORY  |  RUSSIA–NATO ESCALATION"], f, 27, YELLOW, 0, "lead-tag", clip=LEAD, spacing=2)
f, lines, size = fit("RUSSIAN MISSILES VIOLATE POLISH AIRSPACE", XB, 82, 60, 720, 2)
bottom = put(48, 176, lines, f, size, WHITE, size * 0.98, "lead-head", clip=LEAD)
bullets = ["Poland says 2 missiles + 1 drone entered its airspace",
           "Same night, Russian strikes kill 8 in Ukraine",
           "Putin rules out ceasefire after Crimea Bridge hit"]
y = bottom + 24
for b in bullets:
    f, ln, size = fit(b, SEMI, 28, 22, 700, 1)
    rect(48, y + 6, 58, y + 16, YELLOW)
    y = put(72, y, ln, f, size, WHITE, 0, "lead-bullet", clip=LEAD) + 18
icon_missile(880, 276)
f = font(XB, 34)
put(800, 396, ["POLAND | NATO"], f, 34, YELLOW, 0, "lead-label", clip=LEAD)

# ------------------------------------------------------------------ smaller stories
CARDS = [
    ("IRAN WAR | HORMUZ", "#C2410C", "#F76707", "SENATE REJECTS LIMITS ON IRAN WAR",
     "War cost tops $48B; tanker on fire", icon_tanker),
    ("MYANMAR | RULING 19 NOV", "#5B34C4", "#7048E8", "UN COURT: GENOCIDE AGAINST ROHINGYA",
     "ICJ vote 9–6; UK expels attaché", icon_scales),
    ("SHENZHEN | 19–20 NOV", "#1864AB", "#1C7ED6", "FIRST US–CHINA–RUSSIA SUMMIT",
     "Joint declaration on nuclear risks", icon_summit),
    ("CLIMATE | COP31, TURKEY", "#237032", "#2F9E44", "COP31 DRAFT DROPS FOSSIL FUELS",
     "Activists condemn slimmed-down text", icon_cop),
    ("BALTICS | ESTONIA", "#0B6B7A", "#1098AD", "ESTONIA SHUTS RUSSIA BORDER",
     "For 6+ months; Moscow vows response", icon_border),
    ("ITALY | LABOUR", "#A61E4D", "#D6336C", "NATIONWIDE GENERAL STRIKE IN ITALY",
     "Marches in cities across the country", icon_strike),
]
CW, CH, GX, GY, X0, Y0 = 480, 154, 16, 10, 24, 462
for i, (tag, tcol, bar, head, detail, icon) in enumerate(CARDS):
    x, y = X0 + (i % 2) * (CW + GX), Y0 + (i // 2) * (CH + GY)
    box = (x, y, x + CW, y + CH)
    rect(*box, WHITE, r=14, outline=EDGE)
    rect(x + 1, y + 14, x + 9, y + CH - 14, bar)
    f = font(BD, 21)
    put(x + 26, y + 14, [tag], f, 21, tcol, 0, f"card{i}-tag", clip=box, spacing=1.5)
    f, lines, size = fit(head, XB, 38, 30, 340, 2)
    put(x + 26, y + 40, lines, f, size, INK, size * 0.98, f"card{i}-head", clip=(x, y, x + CW - 112, y + CH))
    f, ln, size = fit(detail, MED, 23, 20, CW - 44, 1)
    put(x + 26, y + 121, ln, f, size, "#343A40", 0, f"card{i}-detail", clip=box)
    icon(x + CW - 104, y + 30)

# ------------------------------------------------------------------ footer
rect(0, 954, W, W, NAVY)
f = font(SEMI, 22)
put(28, 964, ["Sources: Democracy Now!, Just Security, Anadolu Agency, Wikipedia Current events"],
    f, 22, WHITE, 0, "foot1", clip=(0, 954, W - 20, W))
put(28, 994, ["News reported 20 Nov 2026 (UTC); some events occurred late on 19 Nov."],
    f, 22, "#CED4DA", 0, "foot2", clip=(0, 954, W - 20, W))

# ------------------------------------------------------------------ self-check: no overlapping text blocks
for i, a in enumerate(boxes):
    for b in boxes[i + 1:]:
        sep = a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2]
        assert sep, f"overlap: {a[0]} / {b[0]}"

out = img.resize((W, W), Image.LANCZOS)
out.save(HERE / "entry.png", optimize=True)
print("wrote", HERE / "entry.png")
