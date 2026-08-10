import json
import os
import re
import requests
from config import GEMINI_API_KEY

def generate_script(article_data, custom_topic=None):
    """
    Stage 2: Gemini Script Writer
    Uses Google Gemini API to write an engaging ~60 second video script based on news data.
    """
    title = article_data.get("title", custom_topic or "Breaking Tech News")
    summary = article_data.get("summary", "")
    source = article_data.get("source", "News Flash")

    prompt = f"""
You are a viral short-form video script writer for YouTube Shorts, TikTok, and Instagram Reels.
Write an engaging, fast-paced 60-second video script based on this news:
TITLE: {title}
SUMMARY: {summary}
SOURCE: {source}

REQUIREMENTS:
1. Total script narration length should be around 140-160 words (approx 60 seconds spoken pace).
2. Must have a high-retention HOOK in the first 3 seconds.
3. Deliver the core story with excitement and clarity.
4. End with a strong Call to Action (CTA).
5. Output MUST be valid JSON format only:
{{
  "title": "Short catchy title",
  "hook": "First attention grabbing sentence",
  "full_script": "Complete narration text from start to finish",
  "cta": "Closing sentence call to action"
}}
"""

    script_result = None

    # Try Gemini API if key is present
    if GEMINI_API_KEY:
        try:
            # Using standard REST endpoint for broad compatibility
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                text_out = data["candidates"][0]["content"]["parts"][0]["text"]
                script_result = json.loads(text_out)
        except Exception as e:
            print(f"[ScriptWriter] Gemini API call error: {e}")

    # Offline / Fallback Script Generator if API key missing or failed
    if not script_result:
        clean_title = re.sub(r'[^\w\s]', '', title)
        script_result = {
            "title": f"{title[:50]}...",
            "hook": f"Did you hear the latest breaking news about {clean_title[:30]}?",
            "full_script": (
                f"Did you hear the latest breaking news about {clean_title[:30]}? "
                f"In a major development reported by {source}, {summary[:120]}. "
                f"Industry analysts are calling this a game-changing moment that could reshape the industry forever. "
                f"Key experts point out that this innovation speeds up developments while opening entirely new possibilities. "
                f"As news continues to unfold, millions are watching closely to see what happens next. "
                f"What do you think about this breakthrough? Let us know in the comments below and subscribe for daily updates!"
            ),
            "cta": "What do you think about this breakthrough? Let us know in the comments below and subscribe for daily updates!"
        }

    return script_result

if __name__ == "__main__":
    test_article = {"title": "AI Breakthrough Announced", "summary": "Scientists launch new autonomous model.", "source": "TechDaily"}
    res = generate_script(test_article)
    print("Generated Script:", json.dumps(res, indent=2))
