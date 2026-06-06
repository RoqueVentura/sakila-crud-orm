# crud_basic.py
import mysql.connector
from config import get_config

def get_conn():
    """Abre y retorna una conexión a MySQL."""
    return mysql.connector.connect(**get_config())


# ======================================================================
# CRUD - COUNTRY
# ======================================================================

def create_country(name: str) -> int:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO country (country) VALUES (%s)',
        (name,)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f'[OK] País creado con ID: {new_id}')
    return new_id

def read_countries(limit: int = 20) -> list:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT country_id, country FROM country ORDER BY country LIMIT %s',
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_country(country_id: int, new_name: str) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE country SET country = %s WHERE country_id = %s',
        (new_name, country_id)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_country(country_id: int) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM country WHERE country_id = %s',
        (country_id,)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


# ======================================================================
# CRUD - CITY
# ======================================================================

def create_city(city_name: str, country_id: int) -> int:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO city (city, country_id) VALUES (%s, %s)',
        (city_name, country_id)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f'[OK] Ciudad creada con ID: {new_id}')
    return new_id

def read_cities(country_id: int = None) -> list:
    conn = get_conn()
    cursor = conn.cursor()
    if country_id:
        cursor.execute(
            'SELECT city_id, city, country_id FROM city '
            'WHERE country_id = %s ORDER BY city',
            (country_id,)
        )
    else:
        cursor.execute(
            'SELECT city_id, city, country_id FROM city ORDER BY city LIMIT 30'
        )
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_city(city_id: int, new_name: str) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE city SET city = %s WHERE city_id = %s',
        (new_name, city_id)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_city(city_id: int) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM city WHERE city_id = %s',
        (city_id,)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


# ======================================================================
# CRUD - FILM
# ======================================================================

def create_film(title: str, language_id: int,
                rental_rate: float, length: int,
                rating: str = 'G') -> int:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO film (title, language_id, rental_rate, length, rating) '
        'VALUES (%s, %s, %s, %s, %s)',
        (title, language_id, rental_rate, length, rating)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f'[OK] Película creada con ID: {new_id}')
    return new_id

def read_films(limit: int = 20, rating: str = None) -> list:
    conn = get_conn()
    cursor = conn.cursor()
    if rating:
        cursor.execute(
            'SELECT film_id, title, rental_rate, length, rating '
            'FROM film WHERE rating = %s ORDER BY title LIMIT %s',
            (rating, limit)
        )
    else:
        cursor.execute(
            'SELECT film_id, title, rental_rate, length, rating '
            'FROM film ORDER BY title LIMIT %s',
            (limit,)
        )
    return cursor.fetchall()

def update_film(film_id: int, new_title: str,
                rental_rate: float = None) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    if rental_rate is not None:
        cursor.execute(
            'UPDATE film SET title = %s, rental_rate = %s WHERE film_id = %s',
            (new_title, rental_rate, film_id)
        )
    else:
        cursor.execute(
            'UPDATE film SET title = %s WHERE film_id = %s',
            (new_title, film_id)
        )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_film(film_id: int) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM film WHERE film_id = %s',
        (film_id,)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


# ======================================================================
# BLOQUE DE PRUEBA
# ======================================================================

if __name__ == '__main__':
    print('\n── Países (primeros 5) ──')
    for row in read_countries(5):
        print(row)
    print('\n── Películas (primeras 5) ──')
    for row in read_films(5):
        print(row)
