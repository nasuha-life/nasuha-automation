from pathlib import Path
import base64
import os
from openai import OpenAI

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
PROMPT_FILE = OUTPUT_DIR / "visual_prompt.txt"
BACKGROUND_FILE = OUTPUT_DIR / "ai_background.png"

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for AI image generation.")
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Visual prompt not found: {PROMPT_FILE}")

    visual_prompt = PROMPT_FILE.read_text(encoding="utf-8").strip()
    prompt = (
        "Create ONLY the visual background artwork for a premium Indonesian Islamic spiritual-reflection "
        "social media poster. Portrait 4:5 composition. Do not render any text, letters, numerals, typography, "
        "calligraphy, watermark, logo, or signature. Leave a calm, uncluttered negative-space area in the "
        "central and lower portions so crisp text can be typeset later. No people or faces. "
        "Use sophisticated cinematic lighting, realistic material detail, subtle atmospheric depth, "
        "luxury editorial art direction, restrained color, and tasteful non-figurative Islamic geometric "
        "craft details only if suitable for the theme. Avoid clichés, visual clutter, and garbled pseudo-writing.\n\n"
        "Creative direction from the content editor:\n" + visual_prompt
    )
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"),
        prompt=prompt,
        size="1024x1536",
        quality="high",
        n=1,
    )
    image_b64 = getattr(response.data[0], "b64_json", None)
    if not image_b64:
        raise RuntimeError("Image API returned no base64 image data; check model access and API response.")
    BACKGROUND_FILE.write_bytes(base64.b64decode(image_b64))
    print(f"AI background generated: {BACKGROUND_FILE}")

if __name__ == "__main__":
    main()
