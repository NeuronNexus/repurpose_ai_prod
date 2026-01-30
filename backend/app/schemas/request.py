from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Drug repurposing query")
