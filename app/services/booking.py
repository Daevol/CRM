from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Booking, BookingStatus, Employee, Service, Vehicle, User
from app.schemas.booking import BookingCreate
from app.services.audit import AuditService
from app.services.notifications import NotificationService


class BookingService:
    @staticmethod
    def create_booking(db: Session, payload: BookingCreate, actor: User) -> Booking:
        if not db.query(Vehicle).filter_by(id=payload.vehicle_id, client_id=payload.client_id).first():
            raise HTTPException(status_code=400, detail="Автомобиль не найден у клиента")
        if not db.query(Service).filter_by(id=payload.service_id).first():
            raise HTTPException(status_code=400, detail="Услуга не найдена")
        if payload.employee_id:
            employee = db.query(Employee).filter_by(id=payload.employee_id).first()
            if not employee:
                raise HTTPException(status_code=400, detail="Сотрудник не найден")
        booking = Booking(**payload.dict())
        db.add(booking)
        db.commit()
        db.refresh(booking)
        AuditService.log_action(db, actor, "create_booking", "Booking", booking.id, payload.dict())
        NotificationService.queue_booking_confirmation(str(payload.client_id), str(payload.client_id), str(payload.service_id))
        return booking

    @staticmethod
    def list_bookings(db: Session):
        return db.query(Booking).order_by(Booking.scheduled_start.desc()).all()

    @staticmethod
    def update_status(db: Session, booking_id: int, status: BookingStatus, actor: User) -> Booking:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Бронь не найдена")
        booking.status = status
        db.commit()
        db.refresh(booking)
        AuditService.log_action(db, actor, "update_booking_status", "Booking", booking.id, {"status": status})
        NotificationService.queue_status_update(str(booking.client_id), status)
        return booking
