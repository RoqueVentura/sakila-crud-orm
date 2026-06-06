from datetime import datetime


class Film:
    """Copia de los campos de la tabla `film`."""

    def __init__(self, film_id=None, title='', description='',
                 release_year=None, language_id=1, original_language_id=None,
                 rental_duration=3, rental_rate=4.99, length=None,
                 replacement_cost=19.99, rating='G',
                 special_features=None, last_update=None):

        self.film_id:              int      = film_id
        self.title:                str      = title
        self.description:          str      = description
        self.release_year:         int      = release_year
        self.language_id:          int      = language_id
        self.original_language_id: int      = original_language_id
        self.rental_duration:      int      = rental_duration
        self.rental_rate:          float    = float(rental_rate)
        self.length:               int      = length
        self.replacement_cost:     float    = float(replacement_cost)
        self.rating:               str      = rating
        self.special_features:     str      = special_features
        self.last_update:          datetime = last_update or datetime.now()

    def __repr__(self):
        return f'Film(id={self.film_id}, title="{self.title}", rating={self.rating})'

    def to_dict(self):
        return {
            'film_id':              self.film_id,
            'title':                self.title,
            'description':          self.description,
            'release_year':         self.release_year,
            'language_id':          self.language_id,
            'original_language_id': self.original_language_id,
            'rental_duration':      self.rental_duration,
            'rental_rate':          self.rental_rate,
            'length':               self.length,
            'replacement_cost':     self.replacement_cost,
            'rating':               self.rating,
            'special_features':     self.special_features,
            'last_update':          str(self.last_update),
        }
