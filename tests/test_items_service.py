"""Tests pour le service ItemService."""

from sqlmodel import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService


class TestItemServiceGetAll:
    """Tests pour la méthode get_all du service."""

    def test_get_all_empty_database(self, session: Session):
        """Test que get_all retourne une liste vide si la base est vide."""
        items = ItemService.get_all(session)

        assert items == []
        assert isinstance(items, list)

    def test_get_all_with_items(self, session: Session):
        """Test que get_all retourne tous les items."""
        # Créer des items de test
        item1 = Item(nom="Item 1", prix=10.0)
        item2 = Item(nom="Item 2", prix=20.0)
        session.add(item1)
        session.add(item2)
        session.commit()

        items = ItemService.get_all(session)

        assert len(items) == 2
        assert items[0].nom == "Item 1"
        assert items[1].nom == "Item 2"

    def test_get_all_with_pagination_skip(self, session: Session):
        """Test que skip fonctionne correctement."""
        # Créer 5 items
        for i in range(5):
            item = Item(nom=f"Item {i}", prix=float(i * 10))
            session.add(item)
        session.commit()

        items = ItemService.get_all(session, skip=2)

        assert len(items) == 3
        assert items[0].nom == "Item 2"

    def test_get_all_with_pagination_limit(self, session: Session):
        """Test que limit fonctionne correctement."""
        # Créer 5 items
        for i in range(5):
            item = Item(nom=f"Item {i}", prix=float(i * 10))
            session.add(item)
        session.commit()

        items = ItemService.get_all(session, limit=3)

        assert len(items) == 3

    def test_get_all_with_skip_and_limit(self, session: Session):
        """Test que skip et limit fonctionnent ensemble."""
        # Créer 10 items
        for i in range(10):
            item = Item(nom=f"Item {i}", prix=float(i * 10))
            session.add(item)
        session.commit()

        items = ItemService.get_all(session, skip=2, limit=3)

        assert len(items) == 3
        assert items[0].nom == "Item 2"
        assert items[2].nom == "Item 4"


class TestItemServiceGetById:
    """Tests pour la méthode get_by_id du service."""

    def test_get_by_id_existing_item(self, session: Session):
        """Test que get_by_id retourne l'item correct."""
        item = Item(nom="Test Item", prix=99.99)
        session.add(item)
        session.commit()
        session.refresh(item)

        found_item = ItemService.get_by_id(session, item.id)

        assert found_item is not None
        assert found_item.id == item.id
        assert found_item.nom == "Test Item"
        assert found_item.prix == 99.99

    def test_get_by_id_non_existing_item(self, session: Session):
        """Test que get_by_id retourne None pour un ID inexistant."""
        found_item = ItemService.get_by_id(session, 9999)

        assert found_item is None


class TestItemServiceCreate:
    """Tests pour la méthode create du service."""

    def test_create_item_success(self, session: Session):
        """Test la création réussie d'un item."""
        item_data = ItemCreate(nom="Nouvel Item", prix=49.99)

        created_item = ItemService.create(session, item_data)

        assert created_item.id is not None
        assert created_item.nom == "Nouvel Item"
        assert created_item.prix == 49.99

    def test_create_item_persists_in_database(self, session: Session):
        """Test que l'item créé est bien persisté en base."""
        item_data = ItemCreate(nom="Item Persisté", prix=29.99)

        created_item = ItemService.create(session, item_data)

        # Vérifier que l'item existe en base
        found_item = session.get(Item, created_item.id)
        assert found_item is not None
        assert found_item.nom == "Item Persisté"

    def test_create_multiple_items(self, session: Session):
        """Test la création de plusieurs items."""
        item1_data = ItemCreate(nom="Item 1", prix=10.0)
        item2_data = ItemCreate(nom="Item 2", prix=20.0)

        item1 = ItemService.create(session, item1_data)
        item2 = ItemService.create(session, item2_data)

        assert item1.id != item2.id
        assert item1.nom == "Item 1"
        assert item2.nom == "Item 2"


class TestItemServiceUpdate:
    """Tests pour la méthode update du service."""

    def test_update_item_all_fields(self, session: Session):
        """Test la mise à jour de tous les champs d'un item."""
        # Créer un item
        item = Item(nom="Original", prix=10.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        # Mettre à jour
        update_data = ItemUpdate(nom="Modifié", prix=25.0)
        updated_item = ItemService.update(session, item.id, update_data)

        assert updated_item is not None
        assert updated_item.nom == "Modifié"
        assert updated_item.prix == 25.0

    def test_update_item_partial(self, session: Session):
        """Test la mise à jour partielle d'un item."""
        # Créer un item
        item = Item(nom="Original", prix=10.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        # Mettre à jour uniquement le prix
        update_data = ItemUpdate(prix=99.99)
        updated_item = ItemService.update(session, item.id, update_data)

        assert updated_item is not None
        assert updated_item.nom == "Original"  # Nom inchangé
        assert updated_item.prix == 99.99

    def test_update_non_existing_item(self, session: Session):
        """Test la mise à jour d'un item inexistant."""
        update_data = ItemUpdate(nom="Inexistant", prix=50.0)

        updated_item = ItemService.update(session, 9999, update_data)

        assert updated_item is None

    def test_update_item_persists(self, session: Session):
        """Test que les modifications sont bien persistées."""
        item = Item(nom="Original", prix=10.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        update_data = ItemUpdate(nom="Persisté")
        ItemService.update(session, item.id, update_data)

        # Vérifier en base
        found_item = session.get(Item, item.id)
        assert found_item.nom == "Persisté"


class TestItemServiceDelete:
    """Tests pour la méthode delete du service."""

    def test_delete_existing_item(self, session: Session):
        """Test la suppression d'un item existant."""
        item = Item(nom="À Supprimer", prix=15.0)
        session.add(item)
        session.commit()
        session.refresh(item)

        result = ItemService.delete(session, item.id)

        assert result is True

        # Vérifier que l'item n'existe plus
        found_item = session.get(Item, item.id)
        assert found_item is None

    def test_delete_non_existing_item(self, session: Session):
        """Test la suppression d'un item inexistant."""
        result = ItemService.delete(session, 9999)

        assert result is False

    def test_delete_item_removes_from_database(self, session: Session):
        """Test que l'item est bien supprimé de la base."""
        # Créer 2 items
        item1 = Item(nom="Item 1", prix=10.0)
        item2 = Item(nom="Item 2", prix=20.0)
        session.add(item1)
        session.add(item2)
        session.commit()
        session.refresh(item1)
        session.refresh(item2)

        # Supprimer le premier
        ItemService.delete(session, item1.id)

        # Vérifier qu'il ne reste qu'un item
        items = ItemService.get_all(session)
        assert len(items) == 1
        assert items[0].nom == "Item 2"
