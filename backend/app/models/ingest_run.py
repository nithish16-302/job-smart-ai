from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class IngestRun(Base):
    __tablename__ = "ingest_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    fetched = Column(Integer, nullable=False, default=0)
    inserted = Column(Integer, nullable=False, default=0)
    status = Column(String(30), nullable=False, default="success")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
