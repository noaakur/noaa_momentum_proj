from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class User(Base):
    """User model representing a team member."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    status = Column(Integer, nullable=False, default=0)  # 0=Working, 1=Working Remotely, 2=On Vacation, 3=Business Trip
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

