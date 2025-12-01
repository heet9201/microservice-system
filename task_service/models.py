from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
