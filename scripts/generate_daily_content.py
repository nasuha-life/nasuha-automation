from pathlib import Path
from datetime import datetime, timezone
import json
import os
from openai import OpenAI

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

PROMPT = """You are the editorial content engine for Nasuha.life, an Indonesian Muslim spiritual reflection brand.
Create ONE original daily Instagram/Facebook content package in Indonesian, focused on taubat nasuha, muhasabah, istighfar, Qur'an reflection, authentic Sunnah, doa, or practical spiritual improvement.
Brand style: premium editorial, concise, emotionally resonant, calm, respectful, minimalist. Goal: qualified visits to https://nasuha.life.
Return only valid JSON with keys: theme, title, verse_reference, verse, reflection, caption, hashtags, cta, visual_prompt, reel_script, reel_scenes.
Rules:
- theme: a short editorial theme for the day, 2–6 words; vary topics and avoid repeating generic themes.
- Never invent Qur'an wording, hadith, source, or reference. Prefer a Qur'an verse only when confident; otherwise use verse_reference="Refleksi umum (tanpa kutipan ayat/hadis)" and verse="".
- If including a Qur'an translation, use concise Indonesian meaning/paraphrase and a correct surah/ayah reference; don't imply it is exact Arabic wording.
- Do not quote a hadith unless you can identify a reliable collection and reference confidently.
- title: 3–8 words, suitable for a poster.
- verse: no more than 25 words, or empty.
- reflection: no more than 22 words.
- caption: concise (25–50 Indonesian words), include https://nasuha.life near the beginning or middle, and end with a direct invitation to visit the site.
- hashtags: 5–8 relevant hashtags as one string, including #NasuhaLife; no spammy or unrelated tags.
- cta: a short action line mentioning https://nasuha.life.
- visual_prompt: detailed image-generation prompt for a premium editorial 4:5 Islamic reflection poster. Use cinematic atmosphere, refined composition, tasteful Islamic geometric/artisanal motifs only when appropriate, strong contrast, generous negative space, and no people/faces. Specify that only the exact title and short supplied poster copy may appear; no extra text, no logos beyond nasuha.life, no misspellings, no overlapping text.
- reel_script: Indonesian voiceover/script for a 12–20 second vertical Reel, 35–55 words maximum, with a natural website CTA.
- reel_scenes: array of exactly 3 short visual directions for a 9:16 Reel; no human faces.
- Keep poster wording short and readable on a phone. Do not put hashtags on the poster itself.
- Avoid reusing generic copy. Do not use date/day numbers as content.
"""

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required; refusing to silently repeat stale content.")
    client = OpenAI(api_key=api_key)
    today_wib = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=PROMPT + "\nGenerate the content for today. Today's date (UTC; use only for internal variety, never put the date/day number in content): " + today_wib + "."
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
    (OUTPUT_DIR / "output.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "theme.txt").write_text(data["theme"].strip(), encoding="utf-8")
    caption = data["caption"].strip() + "\n\n" + data["hashtags"].strip()
    (OUTPUT_DIR / "caption.txt").write_text(caption, encoding="utf-8")
    (OUTPUT_DIR / "hashtags.txt").write_text(data["hashtags"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "visual_prompt.txt").write_text(data["visual_prompt"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "reel_script.txt").write_text(data["reel_script"].strip(), encoding="utf-8")
    (OUTPUT_DIR / "reel_scenes.txt").write_text("\n".join(f"{i+1}. {scene}" for i, scene in enumerate(data["reel_scenes"])), encoding="utf-8")
    print("Daily content package generated and validated.")

if __name__ == "__main__":
    main()
