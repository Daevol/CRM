from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    client_id: int
    vehicle_id: int
    service_id: int
    employee_id: Optional[int] = None
    scheduled_start: datetime
    scheduled_end: datetime
    status: BookingStatus = BookingStatus.PENDING
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
