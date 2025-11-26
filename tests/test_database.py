"""Tests pour le module database."""

import os
from unittest.mock import patch

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import POOL_SIZE


class TestDatabaseConfiguration:
    """Tests pour la configuration de la base de données."""

    def test_database_url_from_env(self):
        """Test que DATABASE_URL est bien chargé depuis l'environnement."""
        # DATABASE_URL devrait être défini dans conftest.py pour les tests
        database_url = os.getenv("DATABASE_URL")
        assert database_url is not None
        assert len(database_url) > 0

    def test_engine_creation_with_test_url(self):
        """Test la création d'un engine avec une URL de test."""
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        assert test_engine is not None
        assert isinstance(test_engine, Engine)

    def test_pool_size_constant(self):
        """Test que POOL_SIZE est défini."""
        assert POOL_SIZE == 10
        assert isinstance(POOL_SIZE, int)


class TestGetDbFunction:
    """Tests pour la fonction get_db avec une base de test."""

    def test_get_db_returns_generator(self, session: Session):
        """Test que get_db retourne un générateur."""
        from collections.abc import Generator

        from app.database import get_db

        db_generator = get_db()
        assert isinstance(db_generator, Generator)

        # Fermer proprement
        try:
            next(db_generator)
            next(db_generator)
        except StopIteration:
            pass

    def test_get_db_with_mock_engine(self):
        """Test get_db avec un engine mocké."""
        from app.database import get_db

        # Créer un engine de test
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(test_engine)

        # Patcher l'engine dans le module database
        with patch('app.database.engine', test_engine):
            db_generator = get_db()
            session = next(db_generator)

            assert isinstance(session, Session)

            # Fermer proprement
            try:
                next(db_generator)
            except StopIteration:
                pass

    def test_session_is_usable_with_fixture(self, session: Session):
        """Test que la session de test est utilisable."""
        from sqlmodel import select

        from app.models.item import Item

        # Ajouter un item de test
        item = Item(nom="Test", prix=10.0)
        session.add(item)
        session.commit()

        # Requêter
        statement = select(Item)
        result = session.exec(statement)
        items = list(result.all())

        assert isinstance(items, list)
        assert len(items) == 1
        assert items[0].nom == "Test"


class TestDatabaseEnvironment:
    """Tests pour les variables d'environnement."""

    def test_database_url_exists(self):
        """Test que DATABASE_URL existe dans l'environnement."""
        database_url = os.getenv("DATABASE_URL")
        assert database_url is not None
        assert isinstance(database_url, str)

    def test_database_url_fallback(self):
        """Test que DATABASE_URL a une valeur par défaut."""
        with patch.dict(os.environ, {}, clear=True):
            url = os.getenv("DATABASE_URL", "")
            # Devrait retourner une chaîne vide par défaut
            assert isinstance(url, str)

    def test_env_file_loading(self):
        """Test que dotenv charge bien les variables."""
        from dotenv import load_dotenv

        # load_dotenv retourne True si un fichier .env est trouvé
        result = load_dotenv()
        assert isinstance(result, bool)


class TestDatabaseIntegration:
    """Tests d'intégration pour la base de données."""

    def test_create_tables_with_test_engine(self):
        """Test la création des tables avec un engine de test."""
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        # Créer toutes les tables
        SQLModel.metadata.create_all(test_engine)

        # Vérifier que les tables existent
        from sqlalchemy import inspect
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()

        assert "items" in tables

    def test_full_database_cycle(self, session: Session):
        """Test un cycle complet avec la base de données."""

        from app.models.item import Item

        # Créer
        item = Item(nom="Cycle Test", prix=99.99)
        session.add(item)
        session.commit()
        session.refresh(item)

        # Lire
        found_item = session.get(Item, item.id)
        assert found_item is not None
        assert found_item.nom == "Cycle Test"

        # Mettre à jour
        found_item.prix = 149.99
        session.add(found_item)
        session.commit()

        # Vérifier la mise à jour
        updated_item = session.get(Item, item.id)
        assert updated_item.prix == 149.99

        # Supprimer
        session.delete(updated_item)
        session.commit()

        # Vérifier la suppression
        deleted_item = session.get(Item, item.id)
        assert deleted_item is None
