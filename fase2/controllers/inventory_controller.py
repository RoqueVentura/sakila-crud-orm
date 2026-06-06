from models.inventory_model import InventoryModel
from entities.inventory import Inventory
from db_context import DbContext


class InventoryController:
    """Controller MVC para Inventory."""

    def __init__(self, context: DbContext):
        self._model = InventoryModel(context)

    def create(self, film_id: int, store_id: int) -> Inventory:
        if store_id not in (1, 2):
            raise ValueError('store_id debe ser 1 o 2.')
        return self._model.add(Inventory(film_id=film_id, store_id=store_id))

    def get_all(self, limit=50) -> list[Inventory]:
        return self._model.get_all(limit)

    def get_by_id(self, inventory_id: int) -> Inventory | None:
        return self._model.get_by_id(inventory_id)

    def get_by_film(self, film_id: int) -> list[Inventory]:
        return self._model.get_by_film(film_id)

    def get_by_store(self, store_id: int) -> list[Inventory]:
        return self._model.get_by_store(store_id)

    def update(self, inventory_id: int, store_id: int) -> bool:
        if store_id not in (1, 2):
            raise ValueError('store_id debe ser 1 o 2.')
        entity = self._model.get_by_id(inventory_id)
        if not entity:
            return False
        entity.store_id = store_id
        return self._model.update(entity)

    def delete(self, inventory_id: int) -> bool:
        return self._model.delete(inventory_id)
