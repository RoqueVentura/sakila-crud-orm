from flask import Blueprint, request, jsonify
from controllers.film_controller import FilmController
from db_context import db

bp = Blueprint('films', __name__)
ctrl = FilmController(db)


@bp.get('/films')
def list_films():
    limit  = request.args.get('limit', 20, type=int)
    rating = request.args.get('rating')
    if rating:
        items = ctrl.get_by_rating(rating.upper())
    else:
        items = ctrl.get_all(limit)
    return jsonify([f.to_dict() for f in items])


@bp.get('/films/<int:film_id>')
def get_film(film_id):
    item = ctrl.get_by_id(film_id)
    if not item:
        return jsonify({'error': 'Película no encontrada'}), 404
    return jsonify(item.to_dict())


@bp.get('/films/<int:film_id>/inventory')
def get_film_inventory(film_id):
    items       = ctrl.get_inventory(film_id)
    disponibles = sum(1 for i in items if i.estado == 'DISPONIBLE')
    return jsonify({
        'film_id':     film_id,
        'total':       len(items),
        'disponibles': disponibles,
        'rentados':    len(items) - disponibles,
        'copias':      [i.to_dict() for i in items],
    })


@bp.post('/films')
def create_film():
    body = request.get_json(silent=True) or {}
    if not body.get('title', '').strip():
        return jsonify({'error': 'El campo "title" es requerido'}), 400
    try:
        item = ctrl.create(
            title            = body['title'],
            language_id      = body.get('language_id', 1),
            description      = body.get('description', ''),
            release_year     = body.get('release_year'),
            rental_duration  = body.get('rental_duration', 3),
            rental_rate      = body.get('rental_rate', 4.99),
            length           = body.get('length'),
            replacement_cost = body.get('replacement_cost', 19.99),
            rating           = body.get('rating', 'G'),
        )
        return jsonify({'ok': True, 'accion': 'creado', 'id': item.film_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.put('/films/<int:film_id>')
def update_film(film_id):
    body   = request.get_json(silent=True) or {}
    campos = {k: body[k] for k in ('title', 'rental_rate', 'length', 'rating') if k in body}
    if not campos:
        return jsonify({'error': 'Envía al menos un campo: title, rental_rate, length, rating'}), 400
    try:
        ok = ctrl.update(
            film_id,
            new_title   = campos.get('title'),
            rental_rate = campos.get('rental_rate'),
            length      = campos.get('length'),
            rating      = campos.get('rating'),
        )
        if not ok:
            return jsonify({'error': 'Película no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'actualizado', 'id': film_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.delete('/films/<int:film_id>')
def delete_film(film_id):
    try:
        ok = ctrl.delete(film_id)
        if not ok:
            return jsonify({'error': 'Película no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'eliminado', 'id': film_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
