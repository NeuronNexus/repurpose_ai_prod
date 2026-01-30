import json
import re

def safe_json_load(text: str) -> dict:
    """
    Extracts and parses the first valid JSON object from LLM output.
    Handles markdown code blocks and nested structures.
    Raises ValueError if impossible.
    """
    if not text or not text.strip():
        raise ValueError("Empty LLM response")

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to strip markdown code blocks (```json ... ```)
    markdown_match = re.search(r"```(?:json)?\s*\n([\s\S]*?)\n```", text)
    if markdown_match:
        try:
            return json.loads(markdown_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to extract JSON with proper brace matching
    # Find the first { and match its closing }
    start_idx = text.find("{")
    if start_idx == -1:
        raise ValueError("No JSON object found in LLM response")
    
    # Count braces to find the matching closing brace
    depth = 0
    for i in range(start_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                json_str = text[start_idx:i+1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid extracted JSON: {e}")
    
    raise ValueError("No valid JSON object found in LLM response")
