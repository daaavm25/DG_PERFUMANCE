import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.catalogo_routes import catalogo_bp
from routes.carrito_routes import carrito_bp

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(catalogo_bp)
app.register_blueprint(carrito_bp)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'app': 'DG_PERFUMANCE'})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'inicio.html')

if __name__ == '__main__':
    app.run(debug=True)
