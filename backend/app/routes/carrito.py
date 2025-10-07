from flask import Blueprint, jsonify, request
from app import db
from app.models.carrito import Carrito

carrito_bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@carrito_bp.route('/', methods=['POST'])
def agregar_al_carrito():
    data = request.json
    nuevo = Carrito(
        usuario_id=data['usuario_id'],
        producto_id=data['producto_id'],
        cantidad=data.get('cantidad', 1)
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Producto agregado al carrito'})
