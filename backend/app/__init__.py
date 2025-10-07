from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración opcional
    app.config['SECRET_KEY'] = 'mi_clave_secreta'

    # Si no tienes rutas aún, no necesitas importar nada
    # from .routes import main
    # app.register_blueprint(main)

    return app

