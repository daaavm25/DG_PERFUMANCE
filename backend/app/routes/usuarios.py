from flask import Blueprint, jsonify, request
from app import db
from app.models.usuarios import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo = Usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        contrasena=data['contrasena']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Cuenta creada con éxito'})

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'correo': u.correo} for u in usuarios])
