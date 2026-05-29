from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)  # e.g., "Porsche"
    model = Column(String, index=True)  # e.g., "911 Carrera"
    year = Column(Integer, index=True)  # e.g., 2023

    # Specifications
    engine_type = Column(String)  # e.g., "3.0L Twin-Turbo Flat-6"
    horsepower = Column(Integer)
    torque_lbft = Column(Integer)
    drivetrain = Column(String)  # e.g., "RWD"

    # Financials
    msrp_usd = Column(Float)