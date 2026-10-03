from app.database import Base, engine

# Import all models so SQLAlchemy knows
# which database tables to create.
from app import models


def initialize_database():
    """
    Create any database tables that do not exist.
    Existing tables and data are preserved.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully!")


if __name__ == "__main__":
    initialize_database()
    