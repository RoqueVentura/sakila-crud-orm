from flask import Flask, jsonify
from db_context import db
from routes.country_routes   import bp as country_bp
from routes.city_routes      import bp as city_bp
from routes.film_routes      import bp as film_bp
from routes.inventory_routes import bp as inventory_bp

app = Flask(__name__)

app.register_blueprint(country_bp)
app.register_blueprint(city_bp)
app.register_blueprint(film_bp)
app.register_blueprint(inventory_bp)


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Ruta o recurso no encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Método HTTP no permitido en esta ruta'}), 405

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': f'Error interno: {e}'}), 500


@app.get('/')
def index():
    return jsonify({
        'api':    'Sakila ORM — Fase II',
        'routes': [
            'GET    /countries',
            'GET    /countries/<id>',
            'POST   /countries',
            'PUT    /countries/<id>',
            'DELETE /countries/<id>',

            'GET    /cities',
            'GET    /cities?country_id=<id>',
            'GET    /cities/<id>',
            'POST   /cities',
            'PUT    /cities/<id>',
            'DELETE /cities/<id>',

            'GET    /films',
            'GET    /films?rating=<G|PG|PG-13|R|NC-17>',
            'GET    /films/<id>',
            'GET    /films/<id>/inventory',
            'POST   /films',
            'PUT    /films/<id>',
            'DELETE /films/<id>',

            'GET    /inventory',
            'GET    /inventory?film_id=<id>',
            'GET    /inventory?store_id=<1|2>',
            'GET    /inventory/<id>',
            'POST   /inventory',
            'PUT    /inventory/<id>',
            'DELETE /inventory/<id>',
        ]
    })


if __name__ == '__main__':
    if db.test_connection():
        app.run(debug=True, port=8000)
