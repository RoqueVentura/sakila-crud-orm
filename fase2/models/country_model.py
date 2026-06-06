from datetime import datetime
from entities.country import Country
from db_context import DbContext


class CountryModel:
    """
    Model ORM para Country.
    Mantiene List[Country] en memoria y lo sincroniza con MySQL.
    """

    def __init__(self, context: DbContext):
        self._ctx = context
        self.items: list[Country] = []

    def add(self, country: Country) -> Country:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO country (country, last_update) VALUES (%s, %s)',
            (country.country, datetime.now())
        )
        country.country_id = cur.lastrowid
        conn.commit()
        conn.close()
        self.items.append(country)
        print(f'[CountryModel] Creado: {country}')
        return country

    def get_all(self, limit=20) -> list[Country]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT country_id, country, last_update FROM country ORDER BY country LIMIT %s',
            (limit,)
        )
        self.items = [Country(r[0], r[1], r[2]) for r in cur.fetchall()]
        conn.close()
        return self.items

    def get_by_id(self, country_id: int) -> Country | None:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT country_id, country, last_update FROM country WHERE country_id = %s',
            (country_id,)
        )
        row = cur.fetchone()
        conn.close()
        return Country(row[0], row[1], row[2]) if row else None

    def update(self, country: Country) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE country SET country = %s, last_update = %s WHERE country_id = %s',
            (country.country, datetime.now(), country.country_id)
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        print(f'[CountryModel] Actualizado: {country}')
        return affected > 0

    def delete(self, country_id: int) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        # Verificar que no tenga ciudades asociadas antes de eliminar
        cur.execute('SELECT COUNT(*) FROM city WHERE country_id = %s', (country_id,))
        if cur.fetchone()[0] > 0:
            conn.close()
            raise Exception('No se puede eliminar: el país tiene ciudades asociadas.')
        cur.execute('DELETE FROM country WHERE country_id = %s', (country_id,))
        affected = cur.rowcount
        conn.commit()
        conn.close()
        self.items = [c for c in self.items if c.country_id != country_id]
        print(f'[CountryModel] Eliminado country_id={country_id}')
        return affected > 0
