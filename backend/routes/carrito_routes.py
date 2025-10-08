from flask import Blueprint, request, jsonify
from config import get_db_connection
from datetime import date

carrito_bp = Blueprint('carrito', __name__) 

@carrito_bp.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    id_cliente = data.get('id_cliente')
    id_empleado = data.get('id_empleado')
    productos = data.get('productos')

    if not (id_cliente and productos):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()

    monto_total = sum(p['cantidad'] * p['precio_unitario'] for p in productos)

    cur.execute("INSERT INTO gestion_perfumance.venta (fecha_venta, monto_total, id_cliente, id_empleado) VALUES (%s, %s, %s, %s) RETURNING id_venta", (date.today(), monto_total, id_cliente, id_empleado))
    id_venta = cur.fetchone()[0]

    for p in productos:
        cur.execute("INSERT INTO gestion_perfumance.detalle_venta (id_venta, id_perfume, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", (id_venta, p['id_perfume'], p['cantidad'], p['precio_unitario']))
        cur.execute("UPDATE gestion_perfumance.perfume SET stock = stock - %s WHERE id_perfume = %s", (p['cantidad'], p['id_perfume']))
    
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Compra realizada con éxito", "id_venta": id_venta, "monto_total": monto_total}), 201

@carrito_bp.route('/api/ventas/<int:id_cliente>', methods=['GET'])
def ver_historial_ventas(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT v.id_venta, v.fecha_venta, v.monto_total FROM gestion_perfumance.ventas v WHERE v.id_cliente = %s ORDER BY v.fecha_venta DESC", (id_cliente,))
    ventas = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"id_venta": row[0], "fecha_venta": row[1], "monto_total": row[2]} for row in ventas]
    return jsonify(data)

@carrito_bp.route('/api/venta/<int:id_venta>', methods=['GET'])
def ver_detalle_venta(id_venta):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT dv.id_detalle_venta, p.marca, dv.cantidad, dv.precio_unitario FROM gestion_perfumance.detalle_venta dv JOIN gestion_perfumance.perfume p ON dv.id_perfume = p.id_perfume WHERE dv.id_venta = %s", (id_venta,))
    detalles = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"id_detalle": row[0], "marca": row[1], "cantidad": row[2], "precio_unitario": row[3]} for row in detalles]
    return jsonify(data)