from models.city_model import CityModel
from entities.city import City
from db_context import DbContext


class CityController:
    """Controller MVC para City."""

    def __init__(self, context: DbContext):
        self._model = CityModel(context)

    def create(self, city_name: str, country_id: int) -> City:
        if not city_name or not city_name.strip():
            raise ValueError('El nombre de la ciudad no puede estar vacío.')
        return self._model.add(City(city=city_name.strip(), country_id=country_id))

    def get_all(self, limit=20) -> list[City]:
        return self._model.get_all(limit)

    def get_by_id(self, city_id: int) -> City | None:
        return self._model.get_by_id(city_id)

    def get_by_country(self, country_id: int) -> list[City]:
        return self._model.get_by_country(country_id)

    def update(self, city_id: int, new_name: str = None, new_country_id: int = None) -> bool:
        entity = self._model.get_by_id(city_id)
        if not entity:
            print(f'[CityController] city_id={city_id} no encontrado.')
            return False
        if new_name:
            entity.city = new_name.strip()
        if new_country_id:
            entity.country_id = new_country_id
        return self._model.update(entity)

    def delete(self, city_id: int) -> bool:
        return self._model.delete(city_id)
