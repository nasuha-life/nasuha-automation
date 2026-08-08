from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import textwrap

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

DATA_FILE = OUTPUT_DIR / "output.json"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Content file not found: {DATA_FILE}")

with open(DATA_FILE, encoding="utf-8") as f:
    data = json.load(f)

W, H = 1080, 1350
img = Image.new("RGB", (W, H), color=(244, 248, 240))
draw = ImageDraw.Draw(img)

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

title_font = load_font(60, bold=True)
verse_font = load_font(42)
body_font = load_font(34)
brand_font = load_font(28)

margin = 80
y = 100

title = textwrap.fill(data.get("title", "Nasuha"), width=20)
draw.text((margin, y), title, fill=(34, 85, 34), font=title_font)
y += 170

verse = textwrap.fill(data.get("verse", ""), width=34)
draw.text((margin, y), verse, fill=(55, 65, 81), font=verse_font)
y += 360

ref = data.get("verse_reference", "")
draw.text((margin, y), ref, fill=(107, 114, 128), font=body_font)
y += 90

reflection = textwrap.fill(data.get("reflection", ""), width=36)
draw.text((margin, y), reflection, fill=(31, 41, 55), font=body_font)

draw.text((margin, H - 80), "nasuha.life", fill=(34, 85, 34), font=brand_font)

poster_path = OUTPUT_DIR / "poster.png"
img.save(poster_path)

print(f"Poster saved to {poster_path}")
