from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import Base


class UserRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    CLIENT = "client"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
