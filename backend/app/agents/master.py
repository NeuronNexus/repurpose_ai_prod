import json
from app.core.gemini_client import call_gemini
from app.trm.refiner import refine_with_trm
from app.utils.json_sanitizer import safe_json_load
from app.utils.normalizer import normalize_list


async def master_plan(query: str):
    system_prompt = """
You are a pharmaceutical AI research planner.
Convert the user query into a structured investigation plan.
Return STRICT JSON following this schema:

{
  "drug": "",
  "indication": "",
  "objectives": [],
  "tasks": [
    {
      "task_id": "",
      "agent": "clinical | patent",
      "description": "",
      "priority": "high | medium | low"
    }
  ],
  "assumptions": [],
  "constraints": [],
  "required_sources": []
}
"""

    raw = call_gemini(system_prompt, f"Query: {query}", temperature=0.3)

    refined = refine_with_trm(
        raw,
        checklist=[
            "At least one clinical task exists",
            "At least one patent task exists",
            "Tasks are answerable using public data",
            "No market or financial analysis"
        ]
    )

    plan = safe_json_load(refined)

    # 🔒 NORMALIZATION (CRITICAL FOR FASTAPI SCHEMA)
    plan["objectives"] = normalize_list(plan.get("objectives", []))
    plan["assumptions"] = normalize_list(plan.get("assumptions", []))
    plan["constraints"] = normalize_list(plan.get("constraints", []))
    plan["required_sources"] = normalize_list(plan.get("required_sources", []))

    return plan


async def master_synthesis(plan, clinical, patent):
    system_prompt = """
You are a senior pharmaceutical strategy analyst.
Synthesize clinical and patent reports into a final decision-ready assessment.

Return STRICT JSON following this schema:

{
  "hypothesis_strength_score": {
    "value": 0,
    "rationale": []
  },
  "aligned_signals": [],
  "contradictions": [],
  "key_risks": [],
  "opportunity_summary": "",
  "recommended_next_steps": [],
  "explicit_limitations": []
}
"""

    user_prompt = json.dumps(
        {
            "plan": plan,
            "clinical": clinical,
            "patent": patent
        },
        ensure_ascii=False
    )

    raw = call_gemini(system_prompt, user_prompt, temperature=0.25)

    try:
        synthesis = safe_json_load(raw)
    except Exception:
        strict_prompt = system_prompt + "\n\nIMPORTANT: Output ONLY raw JSON. No text."
        raw_retry = call_gemini(strict_prompt, user_prompt, temperature=0.1)
        synthesis = safe_json_load(raw_retry)

    # 🔒 NORMALIZATION (CRITICAL)
    synthesis["aligned_signals"] = normalize_list(
        synthesis.get("aligned_signals", [])
    )
    synthesis["key_risks"] = normalize_list(
        synthesis.get("key_risks", [])
    )
    synthesis["recommended_next_steps"] = normalize_list(
        synthesis.get("recommended_next_steps", [])
    )
    synthesis["explicit_limitations"] = normalize_list(
        synthesis.get("explicit_limitations", [])
    )
    synthesis["contradictions"] = normalize_list(
        synthesis.get("contradictions", [])
    )

    # Ensure score value is int (LLMs sometimes return strings)
    synthesis["hypothesis_strength_score"]["value"] = int(
        synthesis["hypothesis_strength_score"]["value"]
    )

    synthesis["hypothesis_strength_score"]["rationale"] = normalize_list(
        synthesis["hypothesis_strength_score"].get("rationale", [])
    )

    return synthesis
