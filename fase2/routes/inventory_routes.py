from flask import Blueprint, request, jsonify
from controllers.inventory_controller import InventoryController
from db_context import db

bp = Blueprint('inventory', __name__)
ctrl = InventoryController(db)


@bp.get('/inventory')
def list_inventory():
    film_id  = request.args.get('film_id',  type=int)
    store_id = request.args.get('store_id', type=int)
    limit    = request.args.get('limit', 50, type=int)
    if film_id:
        items = ctrl.get_by_film(film_id)
    elif store_id:
        items = ctrl.get_by_store(store_id)
    else:
        items = ctrl.get_all(limit)
    return jsonify([i.to_dict() for i in items])


@bp.get('/inventory/<int:inventory_id>')
def get_inventory(inventory_id):
    item = ctrl.get_by_id(inventory_id)
    if not item:
        return jsonify({'error': 'Copia no encontrada'}), 404
    return jsonify(item.to_dict())


@bp.post('/inventory')
def create_inventory():
    body     = request.get_json(silent=True) or {}
    film_id  = body.get('film_id')
    store_id = body.get('store_id')
    if not film_id:
        return jsonify({'error': 'El campo "film_id" es requerido'}), 400
    if not store_id:
        return jsonify({'error': 'El campo "store_id" es requerido (1 o 2)'}), 400
    try:
        item = ctrl.create(film_id, store_id)
        return jsonify({'ok': True, 'accion': 'creado', 'id': item.inventory_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.put('/inventory/<int:inventory_id>')
def update_inventory(inventory_id):
    body     = request.get_json(silent=True) or {}
    store_id = body.get('store_id')
    if not store_id:
        return jsonify({'error': 'El campo "store_id" es requerido (1 o 2)'}), 400
    try:
        ok = ctrl.update(inventory_id, store_id)
        if not ok:
            return jsonify({'error': 'Copia no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'actualizado', 'id': inventory_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.delete('/inventory/<int:inventory_id>')
def delete_inventory(inventory_id):
    try:
        ok = ctrl.delete(inventory_id)
        if not ok:
            return jsonify({'error': 'Copia no encontrada'}), 404
        return jsonify({'ok': True, 'accion': 'eliminado', 'id': inventory_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
