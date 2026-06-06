# metrics.py
import pandas as pd
import mysql.connector
from config import get_config


def load_df(query: str) -> pd.DataFrame:
    conn = mysql.connector.connect(**get_config())
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def print_metrics(df: pd.DataFrame, cols: list, cov_pair: tuple) -> None:
    print(f'  {"Columna":<22} {"Media":>10} {"Rango":>10} {"Desv.":>10} {"Varianza":>12}')
    print(f'  {"-"*22} {"-"*10} {"-"*10} {"-"*10} {"-"*12}')
    for col in cols:
        s = df[col].dropna()
        print(f'  {col:<22} '
              f'{round(float(s.mean()),4):>10} '
              f'{round(float(s.max()-s.min()),4):>10} '
              f'{round(float(s.std()),4):>10} '
              f'{round(float(s.var()),4):>12}')
    c1, c2 = cov_pair
    cov = round(float(df[[c1, c2]].cov().loc[c1, c2]), 4)
    print(f'\n  Covarianza ({c1}, {c2}): {cov}')


def run_all_metrics() -> None:

    # ── COUNTRY ──────────────────────────────────────────────
    df = load_df('SELECT country_id, country FROM country')
    df['name_len'] = df['country'].str.len()
    print('\n══ MÉTRICAS — country ══')
    print_metrics(df, ['country_id', 'name_len'], ('country_id', 'name_len'))

    # ── CITY ─────────────────────────────────────────────────
    df = load_df('SELECT city_id, country_id FROM city')
    print('\n══ MÉTRICAS — city ══')
    print_metrics(df, ['city_id', 'country_id'], ('city_id', 'country_id'))

    # ── FILM ─────────────────────────────────────────────────
    df = load_df('SELECT rental_rate, length, rental_duration, replacement_cost FROM film')
    print('\n══ MÉTRICAS — film ══')
    print_metrics(df, ['rental_rate', 'length', 'rental_duration', 'replacement_cost'],
                  ('rental_rate', 'length'))

    # ── INVENTORY ────────────────────────────────────────────
    df = load_df('SELECT inventory_id, film_id, store_id FROM inventory')
    print('\n══ MÉTRICAS — inventory ══')
    print_metrics(df, ['inventory_id', 'film_id', 'store_id'],
                  ('inventory_id', 'film_id'))


if __name__ == '__main__':
    run_all_metrics()
