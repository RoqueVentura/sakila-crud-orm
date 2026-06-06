from flask import Blueprint, request, jsonify
from controllers.country_controller import CountryController
from db_context import db

bp = Blueprint('countries', __name__)
ctrl = CountryController(db)


@bp.get('/countries')
def list_countries():
    limit = request.args.get('limit', 20, type=int)
    items = ctrl.get_all(limit)
    return jsonify([c.to_dict() for c in items])


@bp.get('/countries/<int:country_id>')
def get_country(country_id):
    item = ctrl.get_by_id(country_id)
    if not item:
        return jsonify({'error': 'País no encontrado'}), 404
    return jsonify(item.to_dict())


@bp.post('/countries')
def create_country():
    body = request.get_json(silent=True) or {}
    name = body.get('country', '').strip()
    if not name:
        return jsonify({'error': 'El campo "country" es requerido'}), 400
    try:
        item = ctrl.create(name)
        return jsonify({'ok': True, 'accion': 'creado', 'id': item.country_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.put('/countries/<int:country_id>')
def update_country(country_id):
    body = request.get_json(silent=True) or {}
    name = body.get('country', '').strip()
    if not name:
        return jsonify({'error': 'El campo "country" es requerido'}), 400
    try:
        ok = ctrl.update(country_id, name)
        if not ok:
            return jsonify({'error': 'País no encontrado'}), 404
        return jsonify({'ok': True, 'accion': 'actualizado', 'id': country_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.delete('/countries/<int:country_id>')
def delete_country(country_id):
    try:
        ok = ctrl.delete(country_id)
        if not ok:
            return jsonify({'error': 'País no encontrado'}), 404
        return jsonify({'ok': True, 'accion': 'eliminado', 'id': country_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
