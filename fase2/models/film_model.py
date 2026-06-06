from datetime import datetime
from entities.film import Film
from db_context import DbContext


class FilmModel:
    """Model ORM para Film. Mantiene List[Film] en memoria."""

    def __init__(self, context: DbContext):
        self._ctx = context
        self.items: list[Film] = []

    def add(self, film: Film) -> Film:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO film
               (title, description, release_year, language_id,
                rental_duration, rental_rate, length, replacement_cost,
                rating, last_update)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (film.title, film.description, film.release_year, film.language_id,
             film.rental_duration, film.rental_rate, film.length,
             film.replacement_cost, film.rating, datetime.now())
        )
        film.film_id = cur.lastrowid
        conn.commit()
        conn.close()
        self.items.append(film)
        print(f'[FilmModel] Creada: {film}')
        return film

    def get_all(self, limit=20) -> list[Film]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            '''SELECT film_id, title, description, release_year, language_id,
                      original_language_id, rental_duration, rental_rate, length,
                      replacement_cost, rating, special_features, last_update
               FROM film ORDER BY title LIMIT %s''',
            (limit,)
        )
        self.items = [self._map(r) for r in cur.fetchall()]
        conn.close()
        return self.items

    def get_by_id(self, film_id: int) -> Film | None:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            '''SELECT film_id, title, description, release_year, language_id,
                      original_language_id, rental_duration, rental_rate, length,
                      replacement_cost, rating, special_features, last_update
               FROM film WHERE film_id = %s''',
            (film_id,)
        )
        row = cur.fetchone()
        conn.close()
        return self._map(row) if row else None

    def get_by_rating(self, rating: str, limit=20) -> list[Film]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            '''SELECT film_id, title, description, release_year, language_id,
                      original_language_id, rental_duration, rental_rate, length,
                      replacement_cost, rating, special_features, last_update
               FROM film WHERE rating = %s ORDER BY title LIMIT %s''',
            (rating, limit)
        )
        self.items = [self._map(r) for r in cur.fetchall()]
        conn.close()
        return self.items

    def update(self, film: Film) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            '''UPDATE film SET title=%s, rental_rate=%s, length=%s,
               rating=%s, last_update=%s WHERE film_id=%s''',
            (film.title, film.rental_rate, film.length,
             film.rating, datetime.now(), film.film_id)
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        print(f'[FilmModel] Actualizada: {film}')
        return affected > 0

    def delete(self, film_id: int) -> bool:
        """
        Elimina la película respetando el orden de FK de Sakila.
        payment.rental_id tiene ON DELETE SET NULL, por eso no hace falta
        borrar payments manualmente.
        """
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        try:
            # Rentas activas — no se puede eliminar si hay alguna sin devolver
            cur.execute(
                '''SELECT COUNT(*) FROM rental r
                   JOIN inventory i ON r.inventory_id = i.inventory_id
                   WHERE i.film_id = %s AND r.return_date IS NULL''',
                (film_id,)
            )
            if cur.fetchone()[0] > 0:
                raise Exception('La película tiene rentas activas; devuélvanlas primero.')

            # Rentas históricas (payments quedan con rental_id=NULL por el trigger de sakila)
            cur.execute(
                '''DELETE r FROM rental r
                   JOIN inventory i ON r.inventory_id = i.inventory_id
                   WHERE i.film_id = %s''',
                (film_id,)
            )
            cur.execute('DELETE FROM inventory     WHERE film_id = %s', (film_id,))
            cur.execute('DELETE FROM film_actor    WHERE film_id = %s', (film_id,))
            cur.execute('DELETE FROM film_category WHERE film_id = %s', (film_id,))
            # film_text lo maneja automáticamente el trigger de Sakila
            cur.execute('DELETE FROM film          WHERE film_id = %s', (film_id,))
            affected = cur.rowcount
            conn.commit()
            self.items = [f for f in self.items if f.film_id != film_id]
            print(f'[FilmModel] Eliminada film_id={film_id}')
            return affected > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _map(row: tuple) -> Film:
        # special_features es SET en MySQL; mysql-connector lo devuelve como set de Python
        sf = row[11]
        if isinstance(sf, set):
            sf = ','.join(sorted(sf))
        return Film(
            film_id=row[0],              title=row[1],
            description=row[2],          release_year=row[3],
            language_id=row[4],          original_language_id=row[5],
            rental_duration=row[6],      rental_rate=row[7],
            length=row[8],               replacement_cost=row[9],
            rating=row[10],              special_features=sf,
            last_update=row[12]
        )
