import os
import requests
import json
import re
import time

GEMINI_MODEL = "gemini-flash-latest"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # seconds


def _build_url() -> str:
    gemini_base = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
    return f"{gemini_base}/models/{GEMINI_MODEL}:generateContent"


def call_gemini(system_prompt: str, user_prompt: str, temperature: float = 0.3, max_output_tokens: int = 2048) -> str:
    """
    Call Google Generative AI (Gemini) REST endpoint using an API key.

    Requires environment variable `GEMINI_API_KEY` to be set.
    Implements exponential backoff for rate limiting (429 errors).
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in environment")

    prompt_text = (system_prompt or "") + "\n\n" + (user_prompt or "")

    url = _build_url()
    params = {"key": gemini_api_key}

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": float(temperature),
            "maxOutputTokens": int(max_output_tokens)
        }
    }

    print("\n[GEMINI] Sending request...")
    print(f"[GEMINI] Model: {GEMINI_MODEL}")
    print(f"[GEMINI] Prompt length: {len(prompt_text)}")

    # Retry with exponential backoff for rate limits
    for attempt in range(MAX_RETRIES):
        start = time.time()

        try:
            res = requests.post(url, params=params, json=payload, timeout=600)
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if res.status_code == 429:  # Too Many Requests
                if attempt < MAX_RETRIES - 1:
                    backoff = INITIAL_BACKOFF * (2 ** attempt)
                    print(f"[GEMINI] Rate limited (429). Retrying in {backoff}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(backoff)
                    continue
            print(f"[GEMINI] Request failed: {e}")
            raise
        except Exception as e:
            print(f"[GEMINI] Request failed: {e}")
            raise

        elapsed = round(time.time() - start, 2)
        print(f"[GEMINI] Response received in {elapsed}s")

        data = res.json()

        # Parse Gemini generateContent response
        # Format: {"candidates": [{"content": {"parts": [{"text": "..."}]}}]}
        if "candidates" in data and isinstance(data["candidates"], list) and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if isinstance(parts, list) and len(parts) > 0:
                    text = parts[0].get("text", "")
                    if text:
                        # Strip markdown code blocks if present
                        text = re.sub(r"```(?:json)?\s*\n?", "", text)
                        return text.strip()

        # Fallback: try to extract any string in top-level
        for key in ("text", "content"):
            if key in data and isinstance(data[key], str):
                return data[key]

        # If we didn't find any expected field, raise for visibility
        print("[GEMINI] Unexpected response format:")
        print(json.dumps(data, indent=2))
        raise ValueError("Unexpected Gemini response format")

    raise RuntimeError(f"Failed after {MAX_RETRIES} retries due to rate limiting")
