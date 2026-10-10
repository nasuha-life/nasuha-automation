from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import json
import textwrap

OUTPUT_DIR = Path("output")
DATA_FILE = OUTPUT_DIR / "output.json"
BACKGROUND_FILE = OUTPUT_DIR / "ai_background.png"

W, H = 1080, 1350
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Content file not found: {DATA_FILE}")
if not BACKGROUND_FILE.exists():
    raise FileNotFoundError(
        f"AI background not found: {BACKGROUND_FILE}. Run scripts/generate_ai_background.py first."
    )

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

def wrap_pixels(draw, text, font, max_width):
    words = str(text or "").split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_lines(draw, lines, x, y, font, fill, spacing=14):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill, stroke_width=0)
        y += draw.textbbox((x, y), line, font=font)[3] - draw.textbbox((x, y), line, font=font)[1] + spacing
    return y

# Crop generated art to a 4:5 canvas without stretching.
background = Image.open(BACKGROUND_FILE).convert("RGB")
source_ratio = background.width / background.height
target_ratio = W / H
if source_ratio > target_ratio:
    new_width = int(background.height * target_ratio)
    left = (background.width - new_width) // 2
    background = background.crop((left, 0, left + new_width, background.height))
else:
    new_height = int(background.width / target_ratio)
    top = (background.height - new_height) // 2
    background = background.crop((0, top, background.width, top + new_height))
img = background.resize((W, H), Image.Resampling.LANCZOS)
img = ImageEnhance.Color(img).enhance(0.82)
img = ImageEnhance.Brightness(img).enhance(0.72).convert("RGBA")

# A subtle dark gradient improves readability while retaining the AI artwork.
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pixels = overlay.load()
for y in range(H):
    alpha = int(52 + 112 * (y / (H - 1)))
    for x in range(W):
        pixels[x, y] = (8, 13, 19, alpha)
img = Image.alpha_composite(img, overlay)
draw = ImageDraw.Draw(img)

margin = 88
title_font = load_font(72, bold=True)
verse_font = load_font(39)
ref_font = load_font(25)
reflection_font = load_font(34)
brand_font = load_font(31, bold=True)
cta_font = load_font(23)

title_lines = wrap_pixels(draw, data.get("title", "Kembali kepada Allah"), title_font, W - margin * 2)
y = 145
y = draw_lines(draw, title_lines[:3], margin, y, title_font, (255, 252, 244, 255), spacing=15)
y += 38

verse = data.get("verse", "").strip()
if verse:
    verse_lines = wrap_pixels(draw, "“" + verse + "”", verse_font, W - margin * 2)
    y = draw_lines(draw, verse_lines[:4], margin, y, verse_font, (248, 246, 239, 255), spacing=12)
    y += 16

reference = data.get("verse_reference", "").strip()
if reference:
    ref_lines = wrap_pixels(draw, reference, ref_font, W - margin * 2)
    y = draw_lines(draw, ref_lines[:2], margin, y, ref_font, (224, 211, 174, 255), spacing=8)
    y += 38

reflection = data.get("reflection", "").strip()
if reflection:
    reflection_lines = wrap_pixels(draw, reflection, reflection_font, W - margin * 2)
    y = draw_lines(draw, reflection_lines[:4], margin, y, reflection_font, (255, 255, 255, 255), spacing=13)

# Restrained footer branding and website CTA.
footer_y = H - 165
draw.line((margin, footer_y - 24, margin + 95, footer_y - 24), fill=(224, 211, 174, 220), width=3)
draw.text((margin, footer_y), "nasuha.life", font=brand_font, fill=(255, 252, 244, 255))
draw.text((margin, footer_y + 48), "Mulai langkah kembali kepada Allah", font=cta_font, fill=(236, 232, 220, 255))

poster_path = OUTPUT_DIR / "poster.png"
img.convert("RGB").save(poster_path, quality=95)
print(f"Premium AI poster rendered: {poster_path} ({W}x{H})")
