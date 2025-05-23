import pytest
from app.main import app
from app.core.database import Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.core.config import settings
from app.core.database import get_db
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


# Create test engine
engine = create_engine(settings.database_url)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Apply schema before test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Provide a clean DB session for each test using rollbacks
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Override get_db dependency in FastAPI
@pytest.fixture(scope="function", autouse=True)
def override_get_db(db: Session):
    def _get_db_override():
        yield db

    app.dependency_overrides[get_db] = _get_db_override

# Test client fixture
@pytest.fixture(scope="function")
def client():
    return TestClient(app)