import json
from app.core.gemini_client import call_gemini
from app.trm.refiner import refine_with_trm
from app.utils.json_sanitizer import safe_json_load
from app.utils.normalizer import normalize_list


async def run_patent_agent(plan):
    system_prompt = """
You are a patent landscape analysis agent.
Analyze high-level patent feasibility using public patent metadata.
Do NOT provide legal advice.

Return STRICT JSON:

{
  "drug": "",
  "indication": "",
  "key_patents": [
    {
      "patent_id": "",
      "jurisdiction": "",
      "filing_year": null,
      "expiry_year": null,
      "coverage_type": "",
      "relevance": "high | medium | low"
    }
  ],
  "freedom_to_operate": "high | moderate | low | unclear",
  "risks": [],
  "whitespace_opportunities": []
}
"""

    user_prompt = json.dumps(plan, ensure_ascii=False)

    raw = call_gemini(system_prompt, user_prompt, temperature=0.2)

    refined = refine_with_trm(
        raw,
        checklist=[
            "No legal claims made",
            "Freedom to operate matches evidence",
            "Expiry logic not overstated",
            "Risks clearly articulated"
        ]
    )

    report = safe_json_load(refined)

    # 🔒 NORMALIZATION (CRITICAL)
    report["risks"] = normalize_list(report.get("risks", []))
    report["whitespace_opportunities"] = normalize_list(
        report.get("whitespace_opportunities", [])
    )

    # 🔒 FIX freedom_to_operate
    fto = report.get("freedom_to_operate")
    if isinstance(fto, dict) and "status" in fto:
        report["freedom_to_operate"] = fto["status"]

    return report
