from datetime import datetime


class Country:
    """Copia de los campos de la tabla `country`."""

    def __init__(self, country_id=None, country='', last_update=None):
        self.country_id:  int      = country_id
        self.country:     str      = country
        self.last_update: datetime = last_update or datetime.now()

    def __repr__(self):
        return f'Country(id={self.country_id}, country="{self.country}")'

    def to_dict(self):
        return {
            'country_id':  self.country_id,
            'country':     self.country,
            'last_update': str(self.last_update),
        }
