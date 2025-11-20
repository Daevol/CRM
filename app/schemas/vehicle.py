from typing import Optional
from pydantic import BaseModel, ConfigDict


class VehicleBase(BaseModel):
    vin: Optional[str] = None
    plate_number: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    notes: Optional[str] = None


class VehicleCreate(VehicleBase):
    client_id: int


class VehicleOut(VehicleBase):
    id: int
    client_id: int
    model_config = ConfigDict(from_attributes=True)
