from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import get_settings
from app.core.database import get_db
from app.models import User, UserRole
from app.schemas.user import Token, UserCreate, UserOut
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
settings = get_settings()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = security.decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


def require_roles(*roles: UserRole):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if roles and current_user.role not in {role.value for role in roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )
        return current_user

    return dependency


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, payload)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.authenticate(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = security.create_access_token({"sub": str(user.id), "role": user.role}, expires_delta=access_token_expires)
    return Token(access_token=token)
