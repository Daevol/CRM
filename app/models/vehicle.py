from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    vin = Column(String, index=True, nullable=True)
    plate_number = Column(String, index=True, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    client = relationship("Client", back_populates="vehicles")
    bookings = relationship("Booking", back_populates="vehicle")
