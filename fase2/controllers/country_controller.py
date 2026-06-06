from models.country_model import CountryModel
from entities.country import Country
from db_context import DbContext


class CountryController:
    """Controller MVC para Country. Coordina View ↔ Model."""

    def __init__(self, context: DbContext):
        self._model = CountryModel(context)

    def create(self, name: str) -> Country:
        if not name or not name.strip():
            raise ValueError('El nombre del país no puede estar vacío.')
        return self._model.add(Country(country=name.strip()))

    def get_all(self, limit=20) -> list[Country]:
        return self._model.get_all(limit)

    def get_by_id(self, country_id: int) -> Country | None:
        return self._model.get_by_id(country_id)

    def update(self, country_id: int, new_name: str) -> bool:
        entity = self._model.get_by_id(country_id)
        if not entity:
            print(f'[CountryController] country_id={country_id} no encontrado.')
            return False
        entity.country = new_name.strip()
        return self._model.update(entity)

    def delete(self, country_id: int) -> bool:
        return self._model.delete(country_id)
