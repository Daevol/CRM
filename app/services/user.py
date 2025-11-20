from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.models import User, UserRole
from app.schemas.user import UserCreate
from app.services.audit import AuditService


class UserService:
    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> User:
        if db.query(User).filter(User.phone == payload.phone).first():
            raise HTTPException(status_code=400, detail="Пользователь с таким телефоном уже существует")
        user = User(
            full_name=payload.full_name,
            phone=payload.phone,
            role=payload.role,
            hashed_password=security.get_password_hash(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        AuditService.log_action(db, None, "create_user", "User", user.id, {"role": user.role})
        return user

    @staticmethod
    def authenticate(db: Session, phone: str, password: str) -> User:
        user = db.query(User).filter(User.phone == phone).first()
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь деактивирован")
        return user
