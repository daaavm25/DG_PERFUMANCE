from flask import Blueprint, jsonify, request
from config import get_db_connection

catalogo_bp = Blueprint('catalogo', __name__, url_prefix='/api')

@catalogo_bp.route('/catalogo/general', methods=['GET'])
def catalogo_general():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.id_genero, p.stock, p.fecha_caducidad, p.precio 
                    FROM gestion_perfumance.perfume p
                    JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
                    ORDER BY p.id_perfume """)
        perfumes = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "id_perfume": row[0],
                "marca": row[1], 
                "presentacion": row[2], 
                "talla": row[3], 
                "id_genero": row[4], 
                "stock": row[5], 
                "fecha_caducidad": row[6],
                "precio": float(row[7])
            } for row in perfumes
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el catálogo", "details": str(e)}), 500

@catalogo_bp.route('/catalogo/<genero>', methods=['GET'])
def catalogo_por_genero(genero):
    try:
        genero = genero.lower()
        conn = get_db_connection()
        cur = conn.cursor()

        if genero == 'hombre':
            cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.precio, g.descripcion AS genero
                        FROM gestion_perfumance.perfume p 
                        JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero 
                        WHERE LOWER(g.descripcion) = 'Hombre' 
                        ORDER BY p.id_perfume""") 
        elif genero == 'mujer':
            cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.precio, g.descripcion AS genero
                        FROM gestion_perfumance.perfume p 
                        JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero 
                        WHERE LOWER(g.descripcion) = 'Mujer' 
                        ORDER BY p.id_perfume""")
        else:
            cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.precio, g. descripcion AS genero
                        FROM gestion_perfumance.perfume p 
                        JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero 
                        ORDER BY p.id_perfume""")
            
        perfumes = cur.fetchall()     
        cur.close()
        conn.close()

        data = [
            {
                "id_perfume": row[0], 
                "marca": row[1], 
                "presentacion": row[2], 
                "talla": row[3], 
                "precio": float(row[4]),
                "genero": row[5]
            } for row in perfumes
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el catálogo por género", "details": str(e)}), 500

@catalogo_bp.route('/catalogo/buscar', methods=['GET'])
def buscar_perfume():
    termino = request.args.get('q', '').strip()
    if not termino:
        return jsonify({"error": "Falta el parámetro de búsqueda 'q'"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT id_perfume, marca, presentacion, talla, id_genero, stock, fecha_caducidad, precio 
                    FROM gestion_perfumance.perfume 
                    WHERE LOWER(marca) ILIKE %s""",
                    (f'%{termino}%',))
        perfumes = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "id_perfume": row[0],
                "marca": row[1], 
                "presentacion": row[2], 
                "talla": row[3], 
                "id_genero": row[4], 
                "stock": row[5], 
                "fecha_caducidad": row[6],
                "precio": float(row[7])
            } for row in perfumes
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Error al buscar perfumes", "details": str(e)}), 500

@catalogo_bp.route('/catalogo/perfume', methods=['GET'])
def obtener_perfumes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.stock, p.fecha_caducidad, p.precio g.descripcion AS genero
                    FROM gestion_perfumance.perfume p
                    JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
                    ORDER BY p.id_perfume;""")
        perfumes = cur.fetchall()
        cur.close()
        conn.close()

        data = [{
                "id": row[0],
                "nombre": row[1],
                "presentacion": row[2],
                "talla": row[3],
                "stock": row[4],
                "fecha_caducidad": row[5],
                "precio":float(row[6]),
                "genero": row[7],
                "imagen_url": f"/static/img/perfume_{row[0]}.jpg"            
        }for row in perfumes]
        return jsonify(data), 200
    except Exception as e:
        print(f"Error al obtener perfumes: {e}")
        return jsonify({"error": "No se pudieron obtener los perfumes"}), 500
    
@catalogo_bp.route('/catalogo/perfumes/<int:id_perfumes>', methods=['GET'])
def obtener_perfumes_porID(id_perfume):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.stock, p.fecha_caducidad, p.precio, g.descripcion AS genero 
                    FROM gestion_perfumace.perfume p
                    JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
                    WHERE p.id_perfume = %s;""")
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return jsonify({"error": "Perfume no encontrado"}), 404
        data = {
            "id": row[0],
            "nombre": row[1],
            "presentacion": row[2],
            "talla": row[3],
            "stock": row[4],
            "fecha_caducidad": row[5],
            "precio": float(row[6]),
            "genero": row[7],
            "imagen_url": f"/static/img/perfume_{row[0]}.jpg"
        }
        return jsonify(data), 200
    except Exception as e:
        print(f"Error al obtener perfume: {e}")
        return jsonify({"error": "No se pudo obtener el perfume"}), 500