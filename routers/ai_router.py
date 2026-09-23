import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from models.ai_analysis import AIAnalysis
from schemas.ai_schema import AIAnalysisRequest
from services.ai_service import generate_ai_analysis


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/analyze")
def analyze_customer(
    request: AIAnalysisRequest,
    db: Session = Depends(get_db)
):
    result = generate_ai_analysis(
        company_name=request.company_name,
        industry=request.industry,
        employees=request.employees,
        security_concerns=request.security_concerns
    )

    ai_response = result["response"]

    if ai_response is None:
        return {
            "message": "AI analysis could not be generated"
        }

    # Convert recommendations to JSON string
    recommendations_json = json.dumps(
        [
            recommendation.model_dump()
            for recommendation in ai_response.recommendations
        ]
    )

    ai_analysis = AIAnalysis(
        company_name=request.company_name,
        industry=request.industry,
        employees=request.employees,
        security_concerns=", ".join(request.security_concerns),

        # Store actual string
        risk_summary=ai_response.risk_summary,

        # Store recommendations as JSON text
        recommendations=recommendations_json
    )

    db.add(ai_analysis)
    db.commit()
    db.refresh(ai_analysis)

    return {
        "id": ai_analysis.id,
        "company_name": ai_analysis.company_name,
        "industry": ai_analysis.industry,
        "employees": ai_analysis.employees,
        "security_concerns": request.security_concerns,
        "risk_summary": ai_response.risk_summary,
        "recommendations": [
            recommendation.model_dump()
            for recommendation in ai_response.recommendations
        ],
        "created_at": ai_analysis.created_at
    }

@router.get("/analyses")
def get_ai_analyses(
    db: Session = Depends(get_db)
):
    analyses = db.query(AIAnalysis).order_by(
        AIAnalysis.created_at.desc()
    ).all()

    return [
        {
            "id": analysis.id,
            "company_name": analysis.company_name,
            "industry": analysis.industry,
            "employees": analysis.employees,
            "security_concerns": analysis.security_concerns.split(", "),
            "risk_summary": analysis.risk_summary,
            "recommendations": json.loads(analysis.recommendations),
            "created_at": analysis.created_at
        }
        for analysis in analyses
    ]