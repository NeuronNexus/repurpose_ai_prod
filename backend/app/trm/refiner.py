from app.core.gemini_client import call_gemini


def refine_with_trm(content_json: str, checklist: list[str]) -> str:
    system_prompt = """
You are a reasoning validator.
Your job is to critically review the provided JSON output against a checklist.
If issues exist, revise the JSON to fix them.
Return ONLY valid JSON. No explanations.
"""

    user_prompt = f"""
CHECKLIST:
{checklist}

JSON OUTPUT:
{content_json}
"""

    # One critique + one revision pass (MVP-safe)
    revised = call_gemini(system_prompt, user_prompt, temperature=0.1)
    return revised
