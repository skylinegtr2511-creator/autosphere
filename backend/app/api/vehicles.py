from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])

# Dependency to get a fresh database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Endpoint to ADD a new vehicle to the database
@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**vehicle_in.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# 2. Endpoint to FETCH all vehicles in the database
@router.get("/", response_model=List[VehicleResponse])
def read_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return vehicles