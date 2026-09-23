from pydantic import BaseModel
from typing import List


class AIAnalysisRequest(BaseModel):
    company_name: str
    industry: str
    employees: int
    security_concerns: List[str]


class Recommendation(BaseModel):
    recommendation: str
    priority: str


class AIAnalysisResponse(BaseModel):
    risk_summary: str
    recommendations: List[Recommendation]