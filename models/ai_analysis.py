from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.base import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    employees = Column(Integer, nullable=False)
    security_concerns = Column(Text, nullable=False)
    risk_summary = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)