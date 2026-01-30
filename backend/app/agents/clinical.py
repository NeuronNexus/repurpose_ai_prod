import json
from app.core.gemini_client import call_gemini
from app.trm.refiner import refine_with_trm
from app.utils.json_sanitizer import safe_json_load
from app.utils.normalizer import normalize_list


async def run_clinical_agent(plan):
    system_prompt = """
You are a clinical evidence analysis agent.
Summarize known clinical evidence from public biomedical literature.
Do NOT fabricate citations.

Return STRICT JSON:

{
  "drug": "",
  "indication": "",
  "evidence": [
    {
      "source_id": "",
      "study_type": "",
      "sample_size": null,
      "outcome_summary": "",
      "statistical_signal": "positive | mixed | negative | inconclusive",
      "limitations": []
    }
  ],
  "overall_signal": "strong | moderate | weak | insufficient",
  "confidence_notes": []
}
"""

    user_prompt = json.dumps(plan, ensure_ascii=False)

    raw = call_gemini(system_prompt, user_prompt, temperature=0.2)

    refined = refine_with_trm(
        raw,
        checklist=[
            "Every evidence item has a source_id",
            "Claims are conservative",
            "Limitations are explicitly stated",
            "No overstated conclusions"
        ]
    )

    report = safe_json_load(refined)

    # 🔒 NORMALIZATION (CRITICAL)
    report["confidence_notes"] = normalize_list(
        report.get("confidence_notes", [])
    )

    # Normalize limitations inside evidence
    for ev in report.get("evidence", []):
        ev["limitations"] = normalize_list(ev.get("limitations", []))

    return report
