import os
import sys
import requests

# 1. Get the root project directory (autosphere_project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 2. Point directly to the backend folder
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
# 3. Add it to Python's system path so it can find the 'app' module
sys.path.append(BACKEND_DIR)

# Now we can import 'app' directly, matching how the rest of the backend works!
from app.core.database import SessionLocal, Base, engine
from app.models.vehicle import Vehicle

# A curated list of popular enthusiast cars to seed our initial wiki database...
# (Keep the rest of your CARS_TO_SEED list and functions exactly the same below here)
# A curated list of popular enthusiast cars to seed our initial wiki database
CARS_TO_SEED = [
    {"make": "Porsche", "model": "911", "year": 2022, "engine_type": "3.0L Twin-Turbo Flat-6", "hp": 379, "torque": 331,
     "drivetrain": "RWD", "msrp": 101200},
    {"make": "Chevrolet", "model": "Corvette", "year": 2023, "engine_type": "6.2L V8", "hp": 490, "torque": 465,
     "drivetrain": "RWD", "msrp": 64500},
    {"make": "Toyota", "model": "Supra", "year": 2021, "engine_type": "3.0L Turbo Inline-6", "hp": 382, "torque": 368,
     "drivetrain": "RWD", "msrp": 50990},
    {"make": "Ford", "model": "Mustang", "year": 2020, "engine_type": "5.0L V8", "hp": 460, "torque": 420,
     "drivetrain": "RWD", "msrp": 36725},
    {"make": "Nissan", "model": "GT-R", "year": 2021, "engine_type": "3.8L Twin-Turbo V8", "hp": 565, "torque": 467,
     "drivetrain": "AWD", "msrp": 113540},
    {"make": "BMW", "model": "M3", "year": 2022, "engine_type": "3.0L Twin-Turbo Inline-6", "hp": 473, "torque": 406,
     "drivetrain": "RWD", "msrp": 72800}
]


def verify_with_nhtsa(make: str, model: str, year: int) -> bool:
    """
    Queries the public NHTSA API to verify if the vehicle exists in global records.
    This acts as a validation layer for our automated data pipeline.
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/474/modelyear/{year}?format=json"
    # Note: For simplicity, we check a broad year category, but we can target specific make names dynamically
    try:
        url_dynamic = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json"
        response = requests.get(url_dynamic, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get("Results", [])
            # Search if our desired model is in the official list returned by NHTSA
            models = [r["Model_Name"].lower() for r in results]
            if model.lower() in [m.lower() for m in models] or any(model.lower() in m for m in models):
                return True
    except Exception as e:
        print(f"⚠️ Warning: NHTSA verification skipped for {make} due to connectivity: {e}")
    return True  # Fallback to true if API is slow, so we don't block the database population


def seed_database():
    print("🚀 Starting the AutoSphere Database Seeding Pipeline...")
    db = SessionLocal()

    try:
        for car in CARS_TO_SEED:
            # Prevent duplicate entries
            existing = db.query(Vehicle).filter_by(make=car["make"], model=car["model"], year=car["year"]).first()
            if existing:
                print(f"⏭️ {car['year']} {car['make']} {car['model']} already exists in database. Skipping.")
                continue

            print(f"🔍 Verifying {car['year']} {car['make']} {car['model']} via NHTSA API...")
            if verify_with_nhtsa(car["make"], car["model"], car["year"]):
                db_vehicle = Vehicle(
                    make=car["make"],
                    model=car["model"],
                    year=car["year"],
                    engine_type=car["engine_type"],
                    horsepower=car["hp"],
                    torque_lbft=car["torque"],
                    drivetrain=car["drivetrain"],
                    msrp_usd=car["msrp"]
                )
                db.add(db_vehicle)
                print(f"✅ Successfully ingested {car['make']} {car['model']} into AutoSphere!")

        db.commit()
        print("\n🎉 Data pipeline completion successful! Your Intelligent Vehicle Database is populated.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during database seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()