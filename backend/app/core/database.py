from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Using SQLite for easy local development.
# We can easily swap this to PostgreSQL later by changing this URL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./autosphere.db"

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # Only needed for SQLite
)

# Create a database session generator
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the base class all our future database models will inherit from
Base = declarative_base()