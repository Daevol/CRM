from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.core.config import get_settings
from app.routers import auth, bookings, clients, finance, inventory, services, vehicles

Base.metadata.create_all(bind=engine)
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(vehicles.router)
app.include_router(services.router)
app.include_router(bookings.router)
app.include_router(inventory.router)
app.include_router(finance.router)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
