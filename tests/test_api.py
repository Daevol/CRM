from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import os
import sys

sys.path.append(os.path.abspath("."))

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_full_flow():
    register_payload = {"full_name": "Admin", "phone": "+70000000000", "password": "secret", "role": "owner"}
    resp = client.post("/auth/register", json=register_payload)
    assert resp.status_code == 200

    token_resp = client.post("/auth/login", data={"username": register_payload["phone"], "password": register_payload["password"]})
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client_payload = {"full_name": "Иван Иванов", "phone": "+79998887766", "notes": "VIP"}
    c_resp = client.post("/clients", json=client_payload, headers=headers)
    assert c_resp.status_code == 200
    client_id = c_resp.json()["id"]

    vehicle_payload = {"client_id": client_id, "vin": "1", "plate_number": "A000AA", "make": "BMW", "model": "X5"}
    v_resp = client.post("/vehicles", json=vehicle_payload, headers=headers)
    assert v_resp.status_code == 200
    vehicle_id = v_resp.json()["id"]

    service_payload = {"name": "Мойка", "category": "wash", "duration_minutes": 60, "price": 1000}
    s_resp = client.post("/services", json=service_payload, headers=headers)
    assert s_resp.status_code == 200
    service_id = s_resp.json()["id"]

    start_time = datetime.utcnow()
    booking_payload = {
        "client_id": client_id,
        "vehicle_id": vehicle_id,
        "service_id": service_id,
        "scheduled_start": start_time.isoformat(),
        "scheduled_end": (start_time + timedelta(minutes=60)).isoformat(),
        "status": "confirmed",
    }
    b_resp = client.post("/bookings", json=booking_payload, headers=headers)
    assert b_resp.status_code == 200

    item_payload = {"name": "Шампунь", "sku": "SH-1", "unit": "l", "quantity": 10}
    i_resp = client.post("/inventory/items", json=item_payload, headers=headers)
    assert i_resp.status_code == 200
    item_id = i_resp.json()["id"]

    movement_payload = {"item_id": item_id, "quantity": 2, "movement_type": "outbound", "reference": "booking"}
    m_resp = client.post("/inventory/movements", json=movement_payload, headers=headers)
    assert m_resp.status_code == 200

    finance_payload = {"direction": "income", "category": "wash", "amount": 1200, "description": "Мойка"}
    f_resp = client.post("/finance/transactions", json=finance_payload, headers=headers)
    assert f_resp.status_code == 200

    summary_resp = client.get("/finance/summary", headers=headers)
    assert summary_resp.status_code == 200
    assert summary_resp.json()["income"] == 1200
