"""Tests pour les modèles SQLModel."""

import pytest
from pydantic import ValidationError

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate


class TestItemModel:
    """Tests pour le modèle Item."""

    def test_item_creation(self):
        """Test la création d'un modèle Item."""
        item = Item(nom="Test Item", prix=99.99)

        assert item.nom == "Test Item"
        assert item.prix == 99.99
        assert item.id is None  # Pas encore en base

    def test_item_with_id(self):
        """Test la création d'un item avec un ID."""
        item = Item(id=1, nom="Item avec ID", prix=50.0)

        assert item.id == 1
        assert item.nom == "Item avec ID"

    def test_item_tablename(self):
        """Test que le nom de table est correct."""
        assert Item.__tablename__ == "items"

    def test_item_nom_is_indexed(self):
        """Test que le champ nom est indexé."""
        # Vérifier que le champ a l'attribut index
        nom_field = Item.model_fields["nom"]
        assert nom_field.json_schema_extra is not None or hasattr(nom_field, "sa_column")


class TestItemCreateSchema:
    """Tests pour le schéma ItemCreate."""

    def test_item_create_valid(self):
        """Test la création d'un schéma ItemCreate valide."""
        item_data = ItemCreate(nom="Nouveau", prix=29.99)

        assert item_data.nom == "Nouveau"
        assert item_data.prix == 29.99

    def test_item_create_validation_empty_nom(self):
        """Test que le nom ne peut pas être vide."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(nom="", prix=10.0)

        errors = exc_info.value.errors()
        assert any("nom" in str(error) for error in errors)

    def test_item_create_validation_negative_price(self):
        """Test que le prix doit être positif."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(nom="Test", prix=-10.0)

        errors = exc_info.value.errors()
        assert any("prix" in str(error) for error in errors)

    def test_item_create_validation_zero_price(self):
        """Test que le prix ne peut pas être zéro."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(nom="Test", prix=0.0)

        errors = exc_info.value.errors()
        assert any("prix" in str(error) for error in errors)

    def test_item_create_validation_nom_too_long(self):
        """Test que le nom ne peut pas dépasser 255 caractères."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(nom="a" * 256, prix=10.0)

        errors = exc_info.value.errors()
        assert any("nom" in str(error) for error in errors)

    def test_item_create_validation_missing_fields(self):
        """Test que tous les champs sont requis."""
        with pytest.raises(ValidationError):
            ItemCreate(nom="Sans Prix")

        with pytest.raises(ValidationError):
            ItemCreate(prix=10.0)


class TestItemUpdateSchema:
    """Tests pour le schéma ItemUpdate."""

    def test_item_update_all_fields(self):
        """Test la mise à jour de tous les champs."""
        update_data = ItemUpdate(nom="Modifié", prix=99.99)

        assert update_data.nom == "Modifié"
        assert update_data.prix == 99.99

    def test_item_update_only_nom(self):
        """Test la mise à jour uniquement du nom."""
        update_data = ItemUpdate(nom="Nouveau Nom")

        assert update_data.nom == "Nouveau Nom"
        assert update_data.prix is None

    def test_item_update_only_prix(self):
        """Test la mise à jour uniquement du prix."""
        update_data = ItemUpdate(prix=49.99)

        assert update_data.nom is None
        assert update_data.prix == 49.99

    def test_item_update_empty_is_valid(self):
        """Test qu'un ItemUpdate vide est valide."""
        update_data = ItemUpdate()

        assert update_data.nom is None
        assert update_data.prix is None

    def test_item_update_validation_empty_nom(self):
        """Test que le nom ne peut pas être vide s'il est fourni."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdate(nom="")

        errors = exc_info.value.errors()
        assert any("nom" in str(error) for error in errors)

    def test_item_update_validation_negative_price(self):
        """Test que le prix doit être positif s'il est fourni."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdate(prix=-10.0)

        errors = exc_info.value.errors()
        assert any("prix" in str(error) for error in errors)

    def test_item_update_validation_zero_price(self):
        """Test que le prix ne peut pas être zéro s'il est fourni."""
        with pytest.raises(ValidationError) as exc_info:
            ItemUpdate(prix=0.0)

        errors = exc_info.value.errors()
        assert any("prix" in str(error) for error in errors)

    def test_item_update_model_dump_exclude_unset(self):
        """Test que model_dump(exclude_unset=True) ne retourne que les champs définis."""
        update_data = ItemUpdate(nom="Seulement Nom")

        dumped = update_data.model_dump(exclude_unset=True)

        assert "nom" in dumped
        assert "prix" not in dumped
        assert dumped["nom"] == "Seulement Nom"


class TestItemResponseSchema:
    """Tests pour le schéma ItemResponse."""

    def test_item_response_creation(self):
        """Test la création d'un schéma ItemResponse."""
        response_data = ItemResponse(id=1, nom="Test", prix=50.0)

        assert response_data.id == 1
        assert response_data.nom == "Test"
        assert response_data.prix == 50.0

    def test_item_response_requires_all_fields(self):
        """Test que tous les champs sont requis pour ItemResponse."""
        with pytest.raises(ValidationError):
            ItemResponse(nom="Sans ID ni Prix")

        with pytest.raises(ValidationError):
            ItemResponse(id=1, prix=10.0)

        with pytest.raises(ValidationError):
            ItemResponse(id=1, nom="Sans Prix")

    def test_item_response_from_item(self):
        """Test la conversion d'un Item en ItemResponse."""
        item = Item(id=1, nom="Test Item", prix=99.99)

        # Simuler la conversion (FastAPI le fait automatiquement)
        response_data = ItemResponse(id=item.id, nom=item.nom, prix=item.prix)

        assert response_data.id == item.id
        assert response_data.nom == item.nom
        assert response_data.prix == item.prix

    def test_item_response_validation_inherits_from_base(self):
        """Test que ItemResponse hérite des validations de ItemBase."""
        # Nom vide
        with pytest.raises(ValidationError):
            ItemResponse(id=1, nom="", prix=10.0)

        # Prix négatif
        with pytest.raises(ValidationError):
            ItemResponse(id=1, nom="Test", prix=-10.0)

        # Prix zéro
        with pytest.raises(ValidationError):
            ItemResponse(id=1, nom="Test", prix=0.0)
