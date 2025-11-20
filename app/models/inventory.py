from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True)
    unit = Column(String, default="pcs")
    quantity = Column(Numeric(10, 2), default=0)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    movements = relationship("StockMovement", back_populates="item")


class StockMovementType(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    ADJUSTMENT = "adjustment"


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("stock_items.id"), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    movement_type = Column(String, default=StockMovementType.ADJUSTMENT)
    reference = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("StockItem", back_populates="movements")
