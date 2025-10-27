from flask import Blueprint, request, jsonify, session, current_app
from config import get_db_connection
from datetime import datetime
import psycopg2

venta_bp = Blueprint('venta', __name__, url_prefix="/api/ventas")

@venta_bp.route('/historial', methods=['GET'])
def historial_ventas():
    try:
        if 'usuario' not in session:
            return jsonify({"error": "Necesita iniciar sesion para continuar"}), 401
        
        id_cliente = session['usuario']['id_usuario']
        conn = get_db_connection
        cur = conn.cursor()
        cur.execute("""SELECT v.id_venta, v.fecha_venta, v.monto_total, p.estado, p.metododepago 
                    FROM gestion_perfumance.venta v
                    LEFT JOIN gestion_perfumance.pago p ON v.id_cliente = p.id_cliente
                    WHERE v.id_cliente = %s
                    ORDER BY v.fecha_venta DESC""", 
                    (id_cliente,))
        ventas = cur.fetchall()
        cur.close()
        conn.close()

        data = [{
            "id_venta": row[0],
            "fecha_venta": row[1],
            "monto_total": float(row[2]),
            "estado": row[3],
            "metodo_pago": row[4]
        }for row in ventas]
        return jsonify (data), 200
    except (psycopg2.Error, Exception) as e:
        return jsonify({"error": "Error al obtener historial de ventas"}), 500

@venta_bp.route('/<int:id__venta>', methods=['GEt'])
def detalle_venta(id_venta):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT p.marca, dv.cantidad, dv.precio_unitario, (dv.cantidad * dv.precio_unitario) AS subtotal
            FROM gestion_perfumance.detalle_venta dv
            JOIN gestion_perfumance.perfume p ON dv.id_perfume = p.id_perfume
            WHERE dv.id_venta = %s""", 
            (id_venta,))
        detalles = cur.fetchall()
        cur.close()
        conn.close()

        data = [{
                "marca": row[0],
                "cantidad": row[1],
                "precio_unitario": float(row[2]),
                "subtotal": float(row[3])
        } for row in detalles]
        return jsonify(data), 200

    except (psycopg2.Error, Exception) as e:
        return jsonify({"error": "Error al obtener detalle de venta"}), 500
    
@venta_bp.route('/pagos', methods=['GET'])
def ver_pagos():
    try:
        if 'usuario' not in session:
            return jsonify({"error": "Debe iniciar sesión para ver sus pagos"}), 401

        id_cliente = session['usuario']['id_usuario']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT id_pago, fecha_pago, total, estado, metododepago
            FROM gestion_perfumance.pago
            WHERE id_cliente = %s
            ORDER BY fecha_pago DESC""", 
        (id_cliente,))
        pagos = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "id_pago": row[0],
                "fecha_pago": row[1],
                "total": float(row[2]),
                "estado": row[3],
                "metododepago": row[4]
            } for row in pagos
        ]
        return jsonify(data), 200
    except (psycopg2.Error, Exception) as e:
        return jsonify({"error": "Error al obtener pagos"}), 500