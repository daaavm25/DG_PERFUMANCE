from flask import Blueprint, jsonify, request
from app import db
from app.models.productos import Producto

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

@productos_bp.route('/', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    data = [
        {'id': p.id, 'nombre': p.nombre, 'genero': p.genero, 'precio': p.precio, 'imagen': p.imagen_url}
        for p in productos
    ]
    return jsonify(data)
