# import_export.py
import pandas as pd
import json
import mysql.connector
from config import get_config
import os


def export_to_csv(table: str, filepath: str) -> None:
    """Exporta una tabla completa de MySQL a CSV."""
    conn = mysql.connector.connect(**get_config())
    df = pd.read_sql(f'SELECT * FROM {table}', conn)
    conn.close()
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f'[OK] {len(df)} filas exportadas a: {filepath}')


def import_from_csv(filepath: str, table: str) -> int:
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    conn = mysql.connector.connect(**get_config())
    cursor = conn.cursor()
    inserted = 0
    cols = ', '.join(df.columns[1:])
    placeholders = ', '.join(['%s'] * (len(df.columns) - 1))
    sql = f'INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})'
    for _, row in df.iterrows():
        cursor.execute(sql, tuple(row[1:]))
        inserted += cursor.rowcount
    conn.commit()
    conn.close()
    return inserted


def export_to_json(table: str, filepath: str) -> None:
    conn = mysql.connector.connect(**get_config())
    df = pd.read_sql(f'SELECT * FROM {table}', conn)
    conn.close()
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_json(filepath, orient='records', indent=2, force_ascii=False)
    print(f'[OK] {len(df)} filas exportadas a JSON: {filepath}')


def import_from_json(filepath: str, table: str) -> int:
    with open(filepath, 'r', encoding='utf-8') as f:
        records = json.load(f)
    df = pd.DataFrame(records)
    conn = mysql.connector.connect(**get_config())
    cursor = conn.cursor()
    inserted = 0
    cols = ', '.join(df.columns[1:])
    placeholders = ', '.join(['%s'] * (len(df.columns) - 1))
    sql = f'INSERT IGNORE INTO {table} ({cols}) VALUES ({placeholders})'
    for _, row in df.iterrows():
        cursor.execute(sql, tuple(row[1:]))
        inserted += cursor.rowcount
    conn.commit()
    conn.close()
    return inserted


if __name__ == '__main__':
    export_to_csv('city',    'output/city.csv')
    export_to_csv('country', 'output/country.csv')
    export_to_csv('film',    'output/film.csv')
    export_to_json('city',    'output/city.json')
    export_to_json('country', 'output/country.json')
    export_to_json('film',    'output/film.json')
