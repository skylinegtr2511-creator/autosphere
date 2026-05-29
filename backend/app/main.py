from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import vehicle
from app.api import vehicles  # Import the new router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoSphere API",
    description="The backend engine for the AutoSphere community.",
    version="1.0.0"
)

# Include the vehicles router in our app
app.include_router(vehicles.router)

@app.get("/")
def read_root():
    return {"status": "success", "message": "The AutoSphere Engine is firing on all cylinders!"}