from datetime import datetime
from entities.city import City
from db_context import DbContext


class CityModel:
    """Model ORM para City. Mantiene List[City] en memoria."""

    def __init__(self, context: DbContext):
        self._ctx = context
        self.items: list[City] = []

    def add(self, city: City) -> City:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, %s)',
            (city.city, city.country_id, datetime.now())
        )
        city.city_id = cur.lastrowid
        conn.commit()
        conn.close()
        self.items.append(city)
        print(f'[CityModel] Creada: {city}')
        return city

    def get_all(self, limit=20) -> list[City]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT city_id, city, country_id, last_update FROM city ORDER BY city LIMIT %s',
            (limit,)
        )
        self.items = [City(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]
        conn.close()
        return self.items

    def get_by_id(self, city_id: int) -> City | None:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT city_id, city, country_id, last_update FROM city WHERE city_id = %s',
            (city_id,)
        )
        row = cur.fetchone()
        conn.close()
        return City(row[0], row[1], row[2], row[3]) if row else None

    def get_by_country(self, country_id: int) -> list[City]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT city_id, city, country_id, last_update '
            'FROM city WHERE country_id = %s ORDER BY city',
            (country_id,)
        )
        rows = [City(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]
        conn.close()
        return rows

    def update(self, city: City) -> bool:
        # Actualiza tanto el nombre como el country_id del objeto
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE city SET city = %s, country_id = %s, last_update = %s WHERE city_id = %s',
            (city.city, city.country_id, datetime.now(), city.city_id)
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        print(f'[CityModel] Actualizada: {city}')
        return affected > 0

    def delete(self, city_id: int) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        # Verificar que no tenga direcciones asociadas
        cur.execute('SELECT COUNT(*) FROM address WHERE city_id = %s', (city_id,))
        if cur.fetchone()[0] > 0:
            conn.close()
            raise Exception('No se puede eliminar: la ciudad tiene direcciones asociadas.')
        cur.execute('DELETE FROM city WHERE city_id = %s', (city_id,))
        affected = cur.rowcount
        conn.commit()
        conn.close()
        self.items = [c for c in self.items if c.city_id != city_id]
        print(f'[CityModel] Eliminada city_id={city_id}')
        return affected > 0
