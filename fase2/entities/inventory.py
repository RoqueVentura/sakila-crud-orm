from datetime import datetime


class Inventory:
    """
    Copia de los campos de la tabla `inventory`.
    estado es un campo calculado (no está en la tabla) que indica
    si la copia está disponible o actualmente rentada.
    """

    def __init__(self, inventory_id=None, film_id=None, store_id=None,
                 last_update=None, titulo=None, estado=None):
        self.inventory_id: int      = inventory_id
        self.film_id:      int      = film_id
        self.store_id:     int      = store_id
        self.last_update:  datetime = last_update or datetime.now()
        # campos calculados con JOIN
        self.titulo: str = titulo
        self.estado: str = estado   # 'DISPONIBLE' | 'RENTADO'

    def __repr__(self):
        return (f'Inventory(id={self.inventory_id}, film_id={self.film_id}, '
                f'store={self.store_id}, estado={self.estado})')

    def to_dict(self):
        return {
            'inventory_id': self.inventory_id,
            'film_id':      self.film_id,
            'store_id':     self.store_id,
            'last_update':  str(self.last_update),
            'titulo':       self.titulo,
            'estado':       self.estado,
        }
