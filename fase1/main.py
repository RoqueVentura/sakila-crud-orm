# main.py
from crud_basic    import (create_country, read_countries,
                            update_country, delete_country,
                            create_city,    read_cities,
                            update_city,    delete_city,
                            create_film,    read_films,
                            update_film,    delete_film)
from metrics       import run_all_metrics
from import_export import (export_to_csv,  import_from_csv,
                            export_to_json, import_from_json)


def demo_crud():
    print('\n========== DEMO CRUD ==========')

    print('\n[COUNTRY]')
    cid = create_country('Wakanda')
    print('  READ:', read_countries(3))
    print('  UPDATE:', update_country(cid, 'Wakanda Forever'))
    print('  DELETE:', delete_country(cid))

    print('\n[CITY]')
    pid = create_country('TempPais')
    city_id = create_city('Ciudad Demo', pid)
    print('  READ:', read_cities(pid))
    print('  UPDATE:', update_city(city_id, 'Ciudad Demo v2'))
    print('  DELETE:', delete_city(city_id))
    delete_country(pid)

    print('\n[FILM]')
    fid = create_film('DEMO FILM', language_id=1,
                      rental_rate=3.99, length=120, rating='PG')
    print('  READ:', read_films(3))
    print('  UPDATE:', update_film(fid, 'DEMO FILM v2', rental_rate=4.99))
    print('  DELETE:', delete_film(fid))


def demo_io():
    print('\n========== EXPORT / IMPORT ==========')
    export_to_csv('city',    'output/city.csv')
    export_to_csv('country', 'output/country.csv')
    export_to_csv('film',    'output/film.csv')
    export_to_json('city',    'output/city.json')
    export_to_json('country', 'output/country.json')
    export_to_json('film',    'output/film.json')
    print('\n[Reimport CSV -> city]')
    n = import_from_csv('output/city.csv', 'city')
    print(f'  {n} filas procesadas')
    print('[Reimport JSON -> country]')
    n = import_from_json('output/country.json', 'country')
    print(f'  {n} filas procesadas')


def demo_metricas():
    run_all_metrics()


def menu():
    opciones = {
        '1': ('Demo CRUD completo',  demo_crud),
        '2': ('Export / Import  CSV  y  JSON',      demo_io),
        '3': ('Métricas descriptivas (film)',        demo_metricas),
        '0': ('Salir', None),
    }
    while True:
        print('\n' + '=' * 45)
        print('  FASE I  |  Sakila CRUD  |  MACDIA C-2')
        print('=' * 45)
        for k, (desc, _) in opciones.items():
            print(f'  [{k}]  {desc}')
        sel = input('  Seleccione opción: ').strip()
        if sel == '0':
            print('  Hasta luego.')
            break
        if sel in opciones and opciones[sel][1]:
            opciones[sel][1]()
        else:
            print('  Opción no válida.')


if __name__ == '__main__':
    menu()
