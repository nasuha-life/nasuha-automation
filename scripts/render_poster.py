#!/usr/bin/env python3
"""
Render a 1080×1350 PNG poster from generated content.
Uses Pillow for image generation with professional typography and layout.
"""

import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap


def load_content(input_file: str = "output/content.json") -> dict:
    """
    Load generated content from JSON file.
    
    Args:
        input_file: Path to content JSON file
        
    Returns:
        dict: Content with title, verse, reflection, caption
    """
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Content file not found: {input_file}")
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    
    return content


def create_poster(content: dict, output_dir: str = "output", output_file: str = "poster.png") -> None:
    """
    Generate a 1080×1350 PNG poster with Islamic content.
    
    Args:
        content: Content dictionary with title, verse, reflection, caption
        output_dir: Output directory
        output_file: Name of output poster image
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    poster_path = output_path / output_file
    
    # Poster dimensions
    width, height = 1080, 1350
    
    # Colors
    bg_color = (15, 32, 62)  # Dark blue background
    accent_color = (34, 177, 76)  # Islamic green
    text_color = (255, 255, 255)  # White text
    verse_color = (220, 220, 220)  # Light gray for verse
    
    # Create image
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fall back to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except OSError:
        # Fall back to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # Draw decorative top bar
    draw.rectangle([(0, 0), (width, 120)], fill=accent_color)
    
    # Draw title
    y_offset = 140
    title = content.get("title", "Nasuha Daily Post")
    title_lines = wrap(title, width=20)
    
    for line in title_lines:
        draw.text(
            (40, y_offset),
            line,
            fill=text_color,
            font=font_large
        )
        y_offset += 60
    
    # Draw verse reference
    y_offset += 20
    verse_ref = content.get("verse_reference", "")
    draw.text(
        (40, y_offset),
        verse_ref,
        fill=accent_color,
        font=font_medium
    )
    
    # Draw verse text
    y_offset += 60
    verse_text = content.get("verse", "")
    verse_lines = wrap(verse_text, width=28)
    
    for line in verse_lines:
        draw.text(
            (40, y_offset),
            line,
            fill=verse_color,
            font=font_small
        )
        y_offset += 45
    
    # Draw reflection section
    y_offset += 30
    reflection = content.get("reflection", "")
    reflection_lines = wrap(reflection, width=28)
    
    for line in reflection_lines[:4]:  # Limit to 4 lines for space
        draw.text(
            (40, y_offset),
            line,
            fill=text_color,
            font=font_small
        )
        y_offset += 45
    
    # Draw branding at bottom
    y_offset = height - 120
    draw.rectangle([(0, y_offset - 20), (width, height)], fill=accent_color)
    
    draw.text(
        (width // 2 - 100, y_offset + 20),
        "nasuha.life",
        fill=text_color,
        font=font_large
    )
    
    # Draw caption at the very bottom (smaller)
    caption = content.get("caption", "")
    caption_lines = wrap(caption, width=35)
    
    if caption_lines:
        caption_text = " ".join(caption_lines[:2])
        draw.text(
            (40, y_offset + 80),
            caption_text[:70] + ("..." if len(caption_text) > 70 else ""),
            fill=(200, 200, 200),
            font=font_tiny
        )
    
    # Save poster
    img.save(poster_path, "PNG", quality=95)
    print(f"[+] Poster saved to {poster_path}")


def main() -> None:
    """Main entry point."""
    try:
        print("[*] Loading content...")
        content = load_content()
        
        print("[*] Rendering poster...")
        create_poster(content)
        
        print("[+] Poster rendered successfully (1080×1350)")
    except Exception as e:
        print(f"[!] Error rendering poster: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
