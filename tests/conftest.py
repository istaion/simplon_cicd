"""Configuration globale des tests et fixtures partagées."""

import os
from collections.abc import Generator

# IMPORTANT: Définir DATABASE_URL AVANT tout import de l'app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_db
from app.main import app


@pytest.fixture(name="session", scope="function")
def session_fixture() -> Generator[Session]:
    """Fixture qui fournit une session de base de données en mémoire pour les tests.

    Utilise SQLite en mémoire pour isoler chaque test.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient]:
    """Fixture qui fournit un client de test FastAPI avec la base de données mockée."""

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
