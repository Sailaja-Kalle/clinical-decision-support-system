from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.connection import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=True)
    oxygen = Column(Float, nullable=True)
    blood_pressure = Column(String, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    symptoms = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())