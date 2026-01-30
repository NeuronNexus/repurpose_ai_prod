from pydantic import BaseModel
from typing import List, Optional, Literal


class MasterTask(BaseModel):
    task_id: str
    agent: Literal["clinical", "patent"]
    description: str
    priority: Literal["high", "medium", "low"]


class MasterPlan(BaseModel):
    drug: str
    indication: str
    objectives: List[str]
    tasks: List[MasterTask]
    assumptions: List[str]
    constraints: List[str]
    required_sources: List[str]


class ClinicalEvidence(BaseModel):
    source_id: str
    study_type: str
    sample_size: Optional[int]
    outcome_summary: str
    statistical_signal: Literal["positive", "mixed", "negative", "inconclusive"]
    limitations: List[str]


class ClinicalReport(BaseModel):
    drug: str
    indication: str
    evidence: List[ClinicalEvidence]
    overall_signal: Literal["strong", "moderate", "weak", "insufficient"]
    confidence_notes: List[str]


class PatentItem(BaseModel):
    patent_id: str
    jurisdiction: str
    filing_year: Optional[int]
    expiry_year: Optional[int]
    coverage_type: str
    relevance: Literal["high", "medium", "low"]


class PatentReport(BaseModel):
    drug: str
    indication: str
    key_patents: List[PatentItem]
    freedom_to_operate: Literal["high", "moderate", "low", "unclear"]
    risks: List[str]
    whitespace_opportunities: List[str]


class HypothesisScore(BaseModel):
    value: int
    rationale: List[str]


class FinalSynthesis(BaseModel):
    hypothesis_strength_score: HypothesisScore
    aligned_signals: List[str]
    contradictions: List[str]
    key_risks: List[str]
    opportunity_summary: str
    recommended_next_steps: List[str]
    explicit_limitations: List[str]


class AnalyzeResponse(BaseModel):
    master: MasterPlan
    clinical: ClinicalReport
    patent: PatentReport
    synthesis: FinalSynthesis
