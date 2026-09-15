from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# connect to PostgreSQL running on my mac using incident monitor databases
DATABASE_URL = "postgresql://aronmezretab@localhost:5432/incident_monitor"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()