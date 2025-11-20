from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from .vehicle import VehicleOut


class ClientBase(BaseModel):
    full_name: str
    phone: str
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    created_at: datetime
    vehicles: List[VehicleOut] = []
    model_config = ConfigDict(from_attributes=True)
