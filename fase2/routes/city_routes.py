from flask import Blueprint, request, jsonify
from controllers.city_controller import CityController
from db_context import db

bp = Blueprint('cities', __name__)
ctrl = CityController(db)


@bp.get('/cities')
def list_cities():
    limit      = request.args.get('limit', 20, type=int)
    country_id = request.args.get('country_id', type=int)
    if country_id:
        items = ctrl.get_by_country(country_id)
    else:
        items = ctrl.get_all(limit)
    return jsonify([c.to_dict() for c in items])


@bp.get('/cities/<int:city_id>')
def get_city(city_id):
    item = ctrl.get_by_id(city_id)
    if not item:
        return jsonify({'error': 'Ciudad no encontrada'}), 404
    return jsonify(item.to_dict())


@bp.post('/cities')
def create_city():
    body       = request.get_json(silent=True) or {}
    name       = body.get('city', '').strip()
    country_id = body.get('country_id')
    if not name:
        return jsonify({'error': 'El campo "city" es requerido'}), 400
    if not country_id:
        return jsonify({'error': 'El campo "country_id" es requerido'}), 400
    try:
        item = ctrl.create(name, country_id)
        return jsonify({'ok': True, 'accion': 'creado', 'id': item.city_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.put('/cities/<int:city_id>')
def update_city(city_id):
    body           = request.get_json(silent=True) or {}
    new_name       = body.get('city', '').strip() or None
    new_country_id = body.get('country_id')
    if not new_name and not new_country_id:
        return jsonify({'error': 'Debe enviar "city" y/o "country_id"'}), 400
    try:
        ok = ctrl.update(city_id, new_name=new_name, new_country_id=new_country_id)
        if not ok:
            return jsonify({'error': 'Ciudad no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'actualizado', 'id': city_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.delete('/cities/<int:city_id>')
def delete_city(city_id):
    try:
        ok = ctrl.delete(city_id)
        if not ok:
            return jsonify({'error': 'Ciudad no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'eliminado', 'id': city_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
