from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import BookingStatus
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking import BookingService
from .auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=BookingOut)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    return BookingService.create_booking(db, payload)


@router.get("", response_model=list[BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return BookingService.list_bookings(db)


@router.patch("/{booking_id}/status", response_model=BookingOut)
def update_status(booking_id: int, status: BookingStatus, db: Session = Depends(get_db)):
    return BookingService.update_status(db, booking_id, status)
