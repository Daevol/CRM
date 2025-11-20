from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.models.inventory import StockMovementType


class StockItemBase(BaseModel):
    name: str
    sku: Optional[str] = None
    unit: str = "pcs"
    quantity: float = 0
    location: Optional[str] = None


class StockItemCreate(StockItemBase):
    pass


class StockItemOut(StockItemBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StockMovementBase(BaseModel):
    item_id: int
    quantity: float
    movement_type: StockMovementType = StockMovementType.ADJUSTMENT
    reference: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementOut(StockMovementBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
