from sqlalchemy import create_engine
from .config import settings, logging
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the SQLAlchemy engine
engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare base for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    logging.info("✅ SQLAlchemy engine initialized successfully")