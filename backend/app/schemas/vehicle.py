from pydantic import BaseModel
from typing import Optional

# Data needed to CREATE a vehicle via the API
class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    engine_type: str
    horsepower: int
    torque_lbft: int
    drivetrain: str
    msrp_usd: float

# Data sent back to the client when READING a vehicle from the API
class VehicleResponse(VehicleCreate):
    id: int

    # Tells Pydantic to read data even if it's an ORM object (from SQLAlchemy)
    class Config:
        from_attributes = True