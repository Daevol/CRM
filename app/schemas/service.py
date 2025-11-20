from typing import Optional
from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    category: Optional[str] = None
    duration_minutes: int = 60
    price: float
    materials: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
