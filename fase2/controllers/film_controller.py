from models.film_model import FilmModel
from models.inventory_model import InventoryModel
from entities.film import Film
from db_context import DbContext


class FilmController:
    """Controller MVC para Film e Inventory."""

    def __init__(self, context: DbContext):
        self._model     = FilmModel(context)
        self._inventory = InventoryModel(context)

    def create(self, title: str, language_id=1, description='',
               release_year=None, rental_duration=3, rental_rate=4.99,
               length=None, replacement_cost=19.99, rating='G') -> Film:
        if not title or not title.strip():
            raise ValueError('El título no puede estar vacío.')
        entity = Film(
            title=title.strip(), language_id=language_id,
            description=description, release_year=release_year,
            rental_duration=rental_duration, rental_rate=rental_rate,
            length=length, replacement_cost=replacement_cost, rating=rating,
        )
        return self._model.add(entity)

    def get_all(self, limit=20) -> list[Film]:
        return self._model.get_all(limit)

    def get_by_id(self, film_id: int) -> Film | None:
        return self._model.get_by_id(film_id)

    def get_by_rating(self, rating: str) -> list[Film]:
        return self._model.get_by_rating(rating)

    def update(self, film_id: int, new_title: str = None,
               rental_rate: float = None, length: int = None,
               rating: str = None) -> bool:
        entity = self._model.get_by_id(film_id)
        if not entity:
            print(f'[FilmController] film_id={film_id} no encontrado.')
            return False
        if new_title  is not None: entity.title       = new_title.strip()
        if rental_rate is not None: entity.rental_rate  = rental_rate
        if length      is not None: entity.length        = length
        if rating      is not None: entity.rating        = rating
        return self._model.update(entity)

    def delete(self, film_id: int) -> bool:
        return self._model.delete(film_id)

    def get_inventory(self, film_id: int) -> list:
        return self._inventory.get_by_film(film_id)
