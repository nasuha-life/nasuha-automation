#!/usr/bin/env python3
"""
Generate daily Islamic content using OpenAI API.
Outputs structured JSON with title, verse, reflection, and caption.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI


def generate_content() -> dict:
    """
    Generate daily Islamic dakwah content using OpenAI.
    
    Returns:
        dict: Content with title, verse_reference, verse, reflection, and caption
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    prompt = """Buat satu konten dakwah Instagram untuk Nasuha.

Format JSON:
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
- Tema berganti setiap hari
- Caption 120-180 kata
- Maksimal 3 hashtag di caption
- Tidak boleh menggunakan caption default
- Jangan mengulang konten yang sudah ada sebelumnya
- Verse harus dari Al-Quran atau Hadits yang autentik"""

    print("[*] Generating daily content with OpenAI...")
    
    response = client.messages.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    response_text = response.content[0].text
    
    # Parse JSON response
    try:
        # Extract JSON from response (may contain markdown code blocks)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text
        
        content = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"[!] Failed to parse JSON response: {e}")
        print(f"[!] Response text: {response_text}")
        sys.exit(1)
    
    # Validate required fields
    required_fields = ["title", "verse_reference", "verse", "reflection", "caption"]
    for field in required_fields:
        if field not in content:
            raise ValueError(f"Missing required field: {field}")
    
    # Add metadata
    content["generated_at"] = datetime.utcnow().isoformat()
    
    return content


def save_content(content: dict, output_dir: str = "output") -> None:
    """
    Save generated content to JSON and text files.
    
    Args:
        content: Generated content dictionary
        output_dir: Directory to save files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save full content as JSON
    json_file = output_path / "content.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"[+] Content saved to {json_file}")
    
    # Save caption as separate text file
    caption_file = output_path / "caption.txt"
    with open(caption_file, "w", encoding="utf-8") as f:
        f.write(content["caption"])
    
    print(f"[+] Caption saved to {caption_file}")


def main() -> None:
    """Main entry point."""
    try:
        content = generate_content()
        save_content(content)
        print("[+] Daily content generated successfully")
        print(f"[+] Title: {content['title']}")
        print(f"[+] Verse: {content['verse_reference']}")
    except Exception as e:
        print(f"[!] Error generating content: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
