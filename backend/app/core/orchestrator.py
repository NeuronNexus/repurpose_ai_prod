from app.agents.master import master_plan, master_synthesis
from app.agents.clinical import run_clinical_agent
from app.agents.patent import run_patent_agent


async def run_analysis(query: str):
    plan = await master_plan(query)

    clinical = await run_clinical_agent(plan)
    patent = await run_patent_agent(plan)

    synthesis = await master_synthesis(plan, clinical, patent)

    return {
        "master": plan,
        "clinical": clinical,
        "patent": patent,
        "synthesis": synthesis
    }
