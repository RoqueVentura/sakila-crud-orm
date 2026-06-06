import requests

BASE = 'http://127.0.0.1:8000'


def sep(titulo):
    print(f'\n{"="*55}')
    print(f'  {titulo}')
    print('='*55)


def mostrar(metodo, url, r):
    try:
        data = r.json()
    except Exception:
        data = None

    estado = '✓' if r.status_code < 400 else '✗'
    print(f'  {estado} {metodo} {url}  [{r.status_code}]')

    if data is None:
        print('    Respuesta: (vacía — reinicia Flask y vuelve a intentar)')
        return

    if isinstance(data, list):
        print(f'    Registros : {len(data)}')
        if data:
            primer = {k: v for k, v in list(data[0].items())[:3]}
            print(f'    Primero   : {primer}...')
    elif 'error' in data:
        print(f'    Error     : {data["error"]}')
    else:
        print(f'    Respuesta : {data}')


def safe_id(response, key):
    try:
        return response.json().get(key)
    except Exception:
        return None


# ══════════════════════════════════════════════════════
# COUNTRY  (GET · POST · PUT · DELETE)
# ══════════════════════════════════════════════════════
sep('COUNTRY')

r = requests.get(f'{BASE}/countries', params={'limit': 5})
mostrar('GET', '/countries?limit=5', r)

r = requests.post(f'{BASE}/countries', json={'country': 'Pais Demo Test'})
mostrar('POST', '/countries', r)
country_id = safe_id(r, 'id')

if country_id:
    r = requests.put(f'{BASE}/countries/{country_id}', json={'country': 'Pais Demo Actualizado'})
    mostrar('PUT', f'/countries/{country_id}', r)

    r = requests.delete(f'{BASE}/countries/{country_id}')
    mostrar('DELETE', f'/countries/{country_id}', r)


# ══════════════════════════════════════════════════════
# CITY  (GET · POST · PUT · DELETE)
# ══════════════════════════════════════════════════════
sep('CITY')

r = requests.get(f'{BASE}/cities', params={'limit': 5})
mostrar('GET', '/cities?limit=5', r)

tmp = requests.post(f'{BASE}/countries', json={'country': 'PaisTempCity'})
tmp_country_id = safe_id(tmp, 'id')

if tmp_country_id:
    r = requests.post(f'{BASE}/cities', json={'city': 'Ciudad Demo', 'country_id': tmp_country_id})
    mostrar('POST', '/cities', r)
    city_id = safe_id(r, 'id')

    if city_id:
        r = requests.put(f'{BASE}/cities/{city_id}', json={'city': 'Ciudad Demo Actualizada'})
        mostrar('PUT', f'/cities/{city_id}', r)

        r = requests.delete(f'{BASE}/cities/{city_id}')
        mostrar('DELETE', f'/cities/{city_id}', r)

    requests.delete(f'{BASE}/countries/{tmp_country_id}')


# ══════════════════════════════════════════════════════
# FILM  (GET · POST · PUT · DELETE)
# ══════════════════════════════════════════════════════
sep('FILM')

r = requests.get(f'{BASE}/films', params={'limit': 5})
mostrar('GET', '/films?limit=5', r)

r = requests.post(f'{BASE}/films', json={
    'title':        'Film Demo Test',
    'description':  'Pelicula de prueba',
    'release_year': 2024,
    'rental_rate':  3.99,
    'length':       105,
    'rating':       'PG',
})
mostrar('POST', '/films', r)
film_id = safe_id(r, 'id')

if film_id:
    r = requests.put(f'{BASE}/films/{film_id}', json={'rental_rate': 1.99, 'length': 115})
    mostrar('PUT', f'/films/{film_id}', r)

    r = requests.delete(f'{BASE}/films/{film_id}')
    mostrar('DELETE', f'/films/{film_id}', r)


# ══════════════════════════════════════════════════════
# INVENTORY  (GET · POST · PUT · DELETE)
# ══════════════════════════════════════════════════════
sep('INVENTORY')

r = requests.get(f'{BASE}/inventory', params={'limit': 5})
mostrar('GET', '/inventory?limit=5', r)

r = requests.post(f'{BASE}/inventory', json={'film_id': 1, 'store_id': 2})
mostrar('POST', '/inventory', r)
inventory_id = safe_id(r, 'id')

if inventory_id:
    r = requests.put(f'{BASE}/inventory/{inventory_id}', json={'store_id': 1})
    mostrar('PUT', f'/inventory/{inventory_id}', r)

    r = requests.delete(f'{BASE}/inventory/{inventory_id}')
    mostrar('DELETE', f'/inventory/{inventory_id}', r)


print('\n' + '='*55)
print('  16 pruebas completadas  (4 por entidad).')
print('='*55)
