import os
from pathlib import Path
import requests

TOKEN = os.environ["META_ACCESS_TOKEN"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]

POSTER = Path("output/poster.png")
CAPTION = Path("output/caption.txt")

if not POSTER.exists():
    raise FileNotFoundError("output/poster.png not found")

caption = CAPTION.read_text(encoding="utf-8") if CAPTION.exists() else "https://nasuha.life"

url = f"https://graph.facebook.com/v25.0/{FB_PAGE_ID}/photos"

with open(POSTER, "rb") as f:
    r = requests.post(
        url,
        files={"source": f},
        data={
            "caption": caption,
            "access_token": TOKEN
        },
        timeout=60
    )

print(r.status_code)
print(r.text)
r.raise_for_status()
print("Facebook upload success")
