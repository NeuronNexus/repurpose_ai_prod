from fastapi import APIRouter
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.core.orchestrator import run_analysis

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    return await run_analysis(request.query)
