from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import textwrap

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

with open("output.json", encoding="utf-8") as f:
    data = json.load(f)

W, H = 1080, 1350
img = Image.new("RGB", (W, H), color=(244, 248, 240))
draw = ImageDraw.Draw(img)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 60)
    verse_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 42)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
    brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except Exception:
    title_font = ImageFont.load_default()
    verse_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    brand_font = ImageFont.load_default()

margin = 80
y = 100

title = textwrap.fill(data.get("title", "Nasuha"), width=20)
draw.text((margin, y), title, fill=(34, 85, 34), font=title_font)
y += 180

verse = textwrap.fill(data.get("verse", ""), width=34)
draw.text((margin, y), verse, fill=(55, 65, 81), font=verse_font)
y += 360

ref = data.get("verse_reference", "")
draw.text((margin, y), ref, fill=(107, 114, 128), font=body_font)
y += 90

reflection = textwrap.fill(data.get("reflection", ""), width=36)
draw.text((margin, y), reflection, fill=(31, 41, 55), font=body_font)

draw.text((margin, H - 80), "nasuha.life", fill=(34, 85, 34), font=brand_font)

img.save(OUTPUT_DIR / "poster.png")
print("Poster saved to output/poster.png")
