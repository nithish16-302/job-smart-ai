from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class ResumeProfile(Base):
    __tablename__ = "resume_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    parsed_skills = Column(Text, nullable=True)
    parsed_roles = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
