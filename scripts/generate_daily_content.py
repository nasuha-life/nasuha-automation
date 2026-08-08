import os
import json
from pathlib import Path
from openai import OpenAI

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

prompt = """
Buat satu konten dakwah Instagram untuk Nasuha.

Kembalikan HANYA JSON valid dengan format berikut:

{
  "title": "...",
  "verse_reference": "...",
  "verse": "...",
  "reflection": "...",
  "caption": "..."
}

Syarat:
- Bahasa Indonesia
- Lembut, menyentuh, dan reflektif
- Tema berbeda setiap hari
- Caption sekitar 120-180 kata
- Maksimal 3 hashtag
- Sertakan ajakan memulai perjalanan taubat bersama https://nasuha.life
- Jangan gunakan emoji berlebihan
- Jangan menambahkan markdown atau penjelasan apa pun
"""

response = client.responses.create(
    model="gpt-5",
    input=prompt,
)

text = response.output_text.strip()

data = json.loads(text)

with open(OUTPUT_DIR / "output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(OUTPUT_DIR / "caption.txt", "w", encoding="utf-8") as f:
    f.write(data["caption"])

print("Daily content generated successfully.")
