from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Importar rutas
    from app.routes.usuarios import usuarios_bp
    from app.routes.productos import productos_bp
    from app.routes.carrito import carrito_bp
    from app.routes.busqueda import busqueda_bp

    # Registrar blueprints
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(carrito_bp)
    app.register_blueprint(busqueda_bp)

    # Crear la base de datos al iniciar
    with app.app_context():
        db.create_all()

    return app

