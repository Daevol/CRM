from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import BookingStatus
from app.models import UserRole, User
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking import BookingService
from .auth import get_current_user, require_roles

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(require_roles(UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER, UserRole.EMPLOYEE))],
)


@router.post("", response_model=BookingOut)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BookingService.create_booking(db, payload, current_user)


@router.get("", response_model=list[BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return BookingService.list_bookings(db)


@router.patch("/{booking_id}/status", response_model=BookingOut)
def update_status(booking_id: int, status: BookingStatus, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BookingService.update_status(db, booking_id, status, current_user)
