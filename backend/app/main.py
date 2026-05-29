from fastapi import FastAPI
from app.core.database import engine, Base
# We must import the models here so SQLAlchemy knows they exist before creating tables
from app.models import vehicle

# This single line creates your database file (autosphere.db)
# and builds all the tables defined in your models.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoSphere API",
    description="The backend engine for the AutoSphere community.",
    version="1.0.0"
)

# A simple health-check route to ensure the server is running
@app.get("/")
def read_root():
    return {"status": "success", "message": "The AutoSphere Engine is firing on all cylinders!"}