from datetime import datetime
from entities.inventory import Inventory
from db_context import DbContext


class InventoryModel:
    """Model ORM para Inventory. Mantiene List[Inventory] en memoria."""

    _SQL = '''
        SELECT
            i.inventory_id,
            i.film_id,
            i.store_id,
            i.last_update,
            f.title AS titulo,
            CASE WHEN r.return_date IS NULL AND r.rental_id IS NOT NULL
                 THEN 'RENTADO' ELSE 'DISPONIBLE' END AS estado
        FROM inventory i
        JOIN film  f ON i.film_id  = f.film_id
        JOIN store s ON i.store_id = s.store_id
        LEFT JOIN (
            SELECT inventory_id, MAX(rental_id) AS rental_id
            FROM rental GROUP BY inventory_id
        ) lr ON i.inventory_id = lr.inventory_id
        LEFT JOIN rental r ON lr.rental_id = r.rental_id
    '''

    def __init__(self, context: DbContext):
        self._ctx = context
        self.items: list[Inventory] = []

    def add(self, inventory: Inventory) -> Inventory:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO inventory (film_id, store_id, last_update) VALUES (%s, %s, %s)',
            (inventory.film_id, inventory.store_id, datetime.now())
        )
        inventory.inventory_id = cur.lastrowid
        conn.commit()
        conn.close()
        self.items.append(inventory)
        print(f'[InventoryModel] Creado: {inventory}')
        return inventory

    def get_all(self, limit=50) -> list[Inventory]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(self._SQL + f' ORDER BY f.title LIMIT {int(limit)}')
        self.items = [self._map(r) for r in cur.fetchall()]
        conn.close()
        return self.items

    def get_by_id(self, inventory_id: int) -> Inventory | None:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(self._SQL + ' WHERE i.inventory_id = %s', (inventory_id,))
        row = cur.fetchone()
        conn.close()
        return self._map(row) if row else None

    def get_by_film(self, film_id: int) -> list[Inventory]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(self._SQL + ' WHERE i.film_id = %s ORDER BY i.store_id', (film_id,))
        self.items = [self._map(r) for r in cur.fetchall()]
        conn.close()
        return self.items

    def get_by_store(self, store_id: int) -> list[Inventory]:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(self._SQL + ' WHERE i.store_id = %s ORDER BY f.title', (store_id,))
        self.items = [self._map(r) for r in cur.fetchall()]
        conn.close()
        return self.items

    def update(self, inventory: Inventory) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE inventory SET store_id = %s, last_update = %s WHERE inventory_id = %s',
            (inventory.store_id, datetime.now(), inventory.inventory_id)
        )
        affected = cur.rowcount
        conn.commit()
        conn.close()
        print(f'[InventoryModel] Actualizado: {inventory}')
        return affected > 0

    def delete(self, inventory_id: int) -> bool:
        conn = self._ctx.get_connection()
        cur = conn.cursor()
        try:
            # No eliminar si hay una renta activa
            cur.execute(
                'SELECT COUNT(*) FROM rental WHERE inventory_id = %s AND return_date IS NULL',
                (inventory_id,)
            )
            if cur.fetchone()[0] > 0:
                raise Exception('La copia está actualmente rentada; no se puede eliminar.')
            # Borrar rentas históricas (payment queda con rental_id=NULL por ON DELETE SET NULL)
            cur.execute('DELETE FROM rental WHERE inventory_id = %s', (inventory_id,))
            cur.execute('DELETE FROM inventory WHERE inventory_id = %s', (inventory_id,))
            affected = cur.rowcount
            conn.commit()
            self.items = [i for i in self.items if i.inventory_id != inventory_id]
            print(f'[InventoryModel] Eliminado inventory_id={inventory_id}')
            return affected > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def _map(row: tuple) -> Inventory:
        return Inventory(
            inventory_id=row[0], film_id=row[1], store_id=row[2],
            last_update=row[3],  titulo=row[4],  estado=row[5]
        )
