from flask import Blueprint, request, jsonify, session, current_app, redirect, render_template, url_for
from config import get_db_connection
from datetime import date, datetime
import psycopg2

carrito_bp = Blueprint('carrito', __name__, url_prefix='/api') 

@carrito_bp.route('/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    if 'usuario' not in session:
        return jsonify({"error": "Necesita iniciar sesion para continuar"}), 401
    
    data = request.get_json()
    id_perfume = data.get('id_perfume')
    cantidad = int(data.get('cantidad', 1))

    if not id_perfume or  cantidad <= 0:
            return jsonify({"error": "Datos invalidos."}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT marca, stock, precio 
                    FROM gestion_perfumance.perfume 
                    WHERE id_perfume = %s""", 
                    (id_perfume,))
        perfume = cur.fetchone()

        cur.close()
        conn.close()

        if not perfume:
            return jsonify({"error": "Producto no encontrado."}), 404

        marca = perfume[0]
        stock = perfume[1]
        precio = float(perfume[2])

        if stock < cantidad:
            return jsonify({"error": "Stock insuficiente"}), 400
                
        carrito = session.get('carrito', [])
        existente = next((item for item in carrito if item['id_perfume'] == id_perfume), None)

        if existente:
            existente ['cantidad'] += cantidad
            existente ['subtotal'] = existente['cantidad'] * existente['precio']
        else:
            carrito.append({
                "id_perfume": id_perfume, 
                "nombre": marca,
                "precio": precio,
                "cantidad": cantidad,
                "subtotal": precio * cantidad,
                "imagen_url": f"/static/img/perfume_{id_perfume}.jpg"
            })
        
        session['carrito'] = carrito
        session.modified = True

        return jsonify({"message": "Producto agregado al carrito.", "carrito": carrito}), 200
    except (psycopg2.Error,Exception) as e:
        current_app.logger.error(f"Error al agregar al carrito: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@carrito_bp.route('/carrito/ver', methods=['GET'])
def ver_carrito():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('carrito.html')

@carrito_bp.route('/carrito_api', methods=['GET'])
def ver_carrito_api():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 400
    
    carrito = session.get('carrito', [])
    return jsonify({"carrito": carrito}), 200

@carrito_bp.route('/carrito/vaciar', methods=['POST'])
def vaciar_carrito():
    session.pop('carrito', None)
    return jsonify({"message": "Carrito vaciado exitosamente."}), 200

@carrito_bp.route('/checkout', methods=['POST'])
def checkout():
    if 'usuario' not in session:
        return jsonify({"error": "Necesita iniciar sesion para continuar"}), 401
    
    usuario = session['usuario']

    id_cliente = usuario.get('id_usuario')
    id_empleado = None
    productos = session.get('carrito', [])  

    if not productos:
        return jsonify({"error": "El carrito está vacío"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        monto_total = sum(item['cantidad'] * item['precio_unitario'] for item in productos)
        #registro de venta 
        cur.execute("""INSERT INTO gestion_perfumance.venta (fecha_venta, monto_total, id_cliente, id_empleado)
                    VALUES (%s, %s, %s, %s) 
                    RETURNING id_venta""",
                    (datetime.now(), monto_total, id_cliente, id_empleado))
        id_venta = cur.fetchone()[0]
        #registro de pago
        cur.execute("""INSERT INTO gestion_perfumance.pago(id_cliente, total, estado, metododepago)
                    VALUES (%s, %s, %s, %s) RETURNING id_pago""", 
                    (id_cliente, monto_total, 'Completado', usuario.get('metododepago', 'Tarjeta')))
        id_pago = cur.fetchone()[0]
        #registro de detalle_pago
        for item in productos:
            cur.execute("""INSERT INTO gestion_perfumance.detalle_pago (id_pago, id_venta, id_cliente, id_perfume, cantidad, costo_unitario)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (id_pago,id_venta, id_cliente, item['id_perfume'], item['cantidad'], item['precio_unitario']))

            cur.execute("""UPDATE gestion_perfumance.perfume 
                        SET stock = stock - %s 
                        WHERE id_perfume = %s""",
                        (item['cantidad'], item['id_perfume']))

        conn.commit()
        cur.close()
        conn.close()

        session.pop('carrito', None)  

        return jsonify({"message": "Compra realizada con éxito", "id_venta": id_venta,"id_pago": id_pago , "monto_total": monto_total}), 201
    except (psycopg2.Error, Exception) as e:
        if 'conn' in locals:
            conn.rollback()
            current_app.logger.error(f"Error en el checkout: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@carrito_bp.route('/ventas/<int:id_cliente>', methods=['GET'])
def ver_historial_ventas(id_cliente):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT v.id_venta, v.fecha_venta, v.monto_total 
                    FROM gestion_perfumance.venta v 
                    WHERE v.id_cliente = %s 
                    ORDER BY v.fecha_venta DESC""", 
                    (id_cliente,))
        ventas = cur.fetchall()
        cur.close()
        conn.close()

        data = [{
            "id_venta": row[0], 
            "fecha_venta": row[1], 
            "monto_total": row[2]
            }for row in ventas]
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception("Error al obtener historial de ventas")
        return jsonify({"error": "Error al consultar historial de ventas"}), 500

@carrito_bp.route('/venta/<int:id_venta>', methods=['GET'])
def ver_detalle_venta(id_venta):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT dv.id_detalle_venta, p.marca, dv.cantidad, dv.precio_unitario 
                    FROM gestion_perfumance.detalle_venta dv 
                    JOIN gestion_perfumance.perfume p ON dv.id_perfume = p.id_perfume 
                    WHERE dv.id_venta = %s""", 
                    (id_venta,))
        detalles = cur.fetchall()
        cur.close()
        conn.close()

        data = [{
            "id_detalle": row[0], 
            "marca": row[1], 
            "cantidad": row[2], 
            "precio_unitario": row[3]
            } for row in detalles]
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception("Error al obtener detalle de venta")
        return jsonify({"error": "Error al obtener detalle de venta"}), 500