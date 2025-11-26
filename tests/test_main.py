"""Tests pour le module principal de l'application."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test que l'endpoint racine retourne le bon message."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Items CRUD API"}


def test_health_endpoint(client: TestClient):
    """Test que l'endpoint health retourne le statut healthy."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_app_metadata(client: TestClient):
    """Test que les métadonnées de l'application sont correctes."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    openapi = response.json()

    assert openapi["info"]["title"] == "Items CRUD API"
    assert openapi["info"]["version"] == "1.0.0"
    assert "API pour gérer une liste d'articles" in openapi["info"]["description"]
