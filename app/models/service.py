from sqlalchemy import Column, Integer, Numeric, String

from app.core.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    duration_minutes = Column(Integer, default=60)
    price = Column(Numeric(10, 2), nullable=False)
    materials = Column(String, nullable=True)
