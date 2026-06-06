from datetime import datetime


class City:
    """Copia de los campos de la tabla `city`."""

    def __init__(self, city_id=None, city='', country_id=None, last_update=None):
        self.city_id:     int      = city_id
        self.city:        str      = city
        self.country_id:  int      = country_id
        self.last_update: datetime = last_update or datetime.now()

    def __repr__(self):
        return f'City(id={self.city_id}, city="{self.city}", country_id={self.country_id})'

    def to_dict(self):
        return {
            'city_id':    self.city_id,
            'city':       self.city,
            'country_id': self.country_id,
            'last_update': str(self.last_update),
        }
