from pathlib import Path
from datetime import datetime, timezone
import json
import os
from openai import OpenAI

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Deterministic daily rotation keeps consecutive posters visually distinct.
VISUAL_DIRECTIONS = [
    "Moonlit midnight blue, antique-gold highlights, dramatic architectural shadows, contemplative and cinematic.",
    "Soft sunrise, warm ivory and sand, subtle olive botanicals, natural light, airy premium editorial.",
    "Restrained charcoal-and-cream monochrome, tactile paper grain, bold magazine composition, high contrast.",
    "Jade green and warm ivory, intricate cast shadows from abstract Islamic geometry, refined and quiet.",
    "Terracotta, muted clay and desert beige, sculptural arches and long shadows, grounded and contemplative.",
    "Deep teal and reflective water, a narrow beam of light, atmospheric depth, minimal and meditative.",
    "Muted lilac, misty dawn, delicate organic forms and soft gradients, gentle but sophisticated.",
    "Emerald-black with restrained copper accents, abstract geometric structure, dramatic premium finish.",
    "Bright ivory, delicate botanical silhouettes, sunlight through textured glass, spacious and hopeful.",
    "Obsidian, brushed bronze and layered geometric relief, tactile luxury materials, dramatic side lighting.",
    "Dusty blue-grey, rain-washed stone and soft window light, introspective photographic realism.",
    "Warm cream, muted burgundy and fine ornamental linework, heritage-inspired but contemporary.",
    "Sage, pale limestone and dappled light, quiet garden-inspired abstraction, fresh and restorative.",
    "Midnight plum and silver moonlight, flowing fabric-like abstract forms, spiritual and otherworldly without figures.",
]
THEME_FOCI = [
    "taubat nasuha dan keberanian memulai kembali",
    "muhasabah dan kejujuran terhadap diri sendiri",
    "istighfar dan membersihkan hati",
    "sabar saat diuji",
    "syukur dalam hal-hal kecil",
    "menjaga lisan dan prasangka",
    "ikhlas dan meluruskan niat",
    "tawakal setelah ikhtiar",
    "memperbaiki salat dan hubungan dengan Allah",
    "memaafkan dan melepaskan dendam",
    "waktu, kematian, dan amal yang tertinggal",
    "doa saat merasa lemah",
    "menjaga amanah dan akhlak",
    "harapan kepada rahmat Allah",
]

PROMPT = """You are the editorial content engine for Nasuha.life, an Indonesian Muslim spiritual reflection brand.
Create ONE original daily Instagram/Facebook content package in Indonesian, focused on taubat nasuha, muhasabah, istighfar, Qur'an reflection, authentic Sunnah, doa, or practical spiritual improvement.
Brand style: premium editorial, concise, emotionally resonant, calm, respectful, minimalist. Goal: qualified visits to https://nasuha.life.
Return only valid JSON with keys: theme, title, verse_reference, verse, reflection, caption, hashtags, cta, visual_prompt, reel_script, reel_scenes.
Rules:
- theme: a short editorial theme for the day, 2–6 words; vary topics and avoid repeating generic themes.
- Make the topic and core message specific, fresh, and distinct; do not fall back to generic “jangan menyerah” or “kembali kepada Allah” unless genuinely relevant to the day's focus.
- Never invent Qur'an wording, hadith, source, or reference. Prefer a Qur'an verse only when confident; otherwise use verse_reference="Refleksi umum (tanpa kutipan ayat/hadis)" and verse="".
- If including a Qur'an translation, use concise Indonesian meaning/paraphrase and a correct surah/ayah reference; don't imply it is exact Arabic wording.
- Do not quote a hadith unless you can identify a reliable collection and reference confidently.
- title: 3–8 words, suitable for a poster.
- verse: no more than 25 words, or empty.
- reflection: no more than 22 words.
- caption: concise (25–50 Indonesian words), include https://nasuha.life near the beginning or middle, and end with a direct invitation to visit the site.
- hashtags: 5–8 relevant hashtags as one string, including #NasuhaLife; no spammy or unrelated tags.
- cta: a short action line mentioning https://nasuha.life.
- visual_prompt: write a precise image-generation brief for today's visual, not a generic reusable template. It must specify subject/metaphor, setting, materials/textures, lighting, palette, camera/composition, and where negative space must remain. Tie the visual metaphor to today's theme. Rotate composition and imagery across days; do not repeat the same arches, lanterns, mosque silhouettes, crescent moons, prayer beads, or open Qur'an by default. Use the supplied daily art direction.
- The image itself must contain NO text, letters, numerals, typography, calligraphy, watermark, logo, people, or faces. Text will be typeset separately by the renderer.
- Avoid cliché stock imagery, clutter, pseudo-Arabic writing, and any elements that compete with legibility.
- reel_script: Indonesian voiceover/script for a 12–20 second vertical Reel, 35–55 words maximum, with a natural website CTA.
- reel_scenes: array of exactly 3 short visual directions for a 9:16 Reel; no human faces.
- Keep poster wording short and readable on a phone. Do not put hashtags on the poster itself.
- Never print the date, day number, or a “Hari #” label as content.
"""

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required; refusing to silently repeat stale content.")
    client = OpenAI(api_key=api_key)
    today = datetime.now(timezone.utc).date()
    today_text = today.isoformat()
    visual_direction = VISUAL_DIRECTIONS[(today.timetuple().tm_yday - 1) % len(VISUAL_DIRECTIONS)]
    theme_focus = THEME_FOCI[(today.timetuple().tm_yday - 1) % len(THEME_FOCI)]
    daily_instruction = (
        f"\nTODAY'S INTERNAL VARIATION INPUT (never print the date or rotation index):"
        f"\nDate key: {today_text}."
        f"\nToday's theme focus: {theme_focus}."
        f"\nToday's mandatory visual art direction: {visual_direction}."
        "\nFollow this art direction closely, while choosing a fresh visual metaphor and composition."
        "\nDo not use the same subject, palette, and composition as the previous generic template; "
        "make today's concept clearly recognizable as a new design."
    )
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=PROMPT + daily_instruction
    )
    raw = response.output_text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    data = json.loads(raw)
    required = ["theme", "title", "verse_reference", "verse", "reflection", "caption",
                "hashtags", "cta", "visual_prompt", "reel_script", "reel_scenes"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing content fields: {missing}")
    if not all(isinstance(data[k], str) for k in required if k != "reel_scenes"):
        raise ValueError("All text fields must be strings.")
    if "https://nasuha.life" not in data["caption"] or "https://nasuha.life" not in data["cta"]:
        raise ValueError("CTA URL missing from caption/CTA.")
    if not isinstance(data["reel_scenes"], list) or len(data["reel_scenes"]) != 3:
        raise ValueError("reel_scenes must contain exactly 3 scenes.")
    data["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    data["daily_visual_direction"] = visual_direction
    data["daily_theme_focus"] = theme_focus
    (OUTPUT_DIR / "output.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "theme.txt").write_text(data["theme"].strip(), encoding="utf-8")
    caption = data["caption"].strip() + "\n\n" + data["hashtags"].strip()
    (OUTPUT_DIR / "caption.txt").write_text(caption, encoding="utf-8")
    (OUTPUT_DIR / "hashtags.txt").write_text(data["hashtags"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "visual_prompt.txt").write_text(data["visual_prompt"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "reel_script.txt").write_text(data["reel_script"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "reel_scenes.txt").write_text("\n".join(f"{i+1}. {scene}" for i, scene in enumerate(data["reel_scenes"])), encoding="utf-8")
    (OUTPUT_DIR / "daily_image_prompt.txt").write_text(
        "Create ONLY the visual background artwork for a premium Indonesian Islamic spiritual-reflection social media poster. "
        "Portrait 4:5 composition. Do not render any text, letters, numerals, typography, calligraphy, watermark, logo, or signature. "
        "Leave a calm, uncluttered negative-space area in the central and lower portions so crisp text can be typeset later. "
        "No people or faces. Use sophisticated cinematic lighting, realistic material detail, subtle atmospheric depth, "
        "luxury editorial art direction, restrained color, and tasteful non-figurative Islamic geometric craft details only if suitable. "
        "Avoid clichés, visual clutter, and garbled pseudo-writing.\n\n"
        "Today's specific visual prompt:\n" + data["visual_prompt"].strip(),
        encoding="utf-8"
    )
    print(f"Daily content package generated and validated. Theme focus: {theme_focus}")
    print(f"Visual direction: {visual_direction}")

if __name__ == "__main__":
    main()
