"""Pytest fixtures and test database setup for Civic Engine."""

import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Set test environment variables before importing app
TEST_DB_PATH = os.path.abspath("test_civic.db")
os.environ["AI_PROVIDER"] = "mock"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

import app.core.config
app.core.config.settings.DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
app.core.config.settings.AI_PROVIDER = "mock"

from app.core.database import Base, engine, SessionLocal, get_db, init_db
from app.main import app
from app.stakeholders.service import StakeholderService


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provide a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    # Seed stakeholders
    StakeholderService(session)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    if os.path.exists("test_civic.db"):
        try:
            os.remove("test_civic.db")
        except Exception:
            pass
