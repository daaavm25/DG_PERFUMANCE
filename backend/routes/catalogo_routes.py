from flask import Blueprint, jsonify, request
from config import get_db_connection

catalogo_bp = Blueprint('catalogo', __name__)

@catalogo_bp.route('/catalogo/general', methods=['GET'])
def catalogo_general():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT marca, presentacion, talla, id_genero, stock, fecha_caducidad FROM gestion_perfumance.perfume")
    perfume = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"marca": row[0], "presentacion": row[1], "talla": row[2], "id_genero": row[3], "stock": row[4], "fecha_caducidad": row[5]} for row in perfume]
    return jsonify(data), 200

@catalogo_bp.route('/catalogo/<genero>', methods=['GET'])
def catalogo_por_genero(genero):
    conn = get_db_connection()
    cur = conn.cursor()

    if genero.lowe() == 'hombre':
        cur.execute("SELECT p.id_perfume, p.marca, p.presentacion, p.talla AS genero" \
        "FROM gestion_perfumance.perfume p JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero WHERE LOWER(g.descripcion) = 'Hombre'") 
    elif genero.lower() == 'mujer':
        cur.execute("SELECT p.id_perfume, p.marca, p.presentacion, p.talla AS genero " \
        "FROM gestion_perfumance.perfume p JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero WHERE LOWER(g.descripcion) = 'Mujer'")
    else:
        cur.execute("SELECT p.id_perfume, p.marca, p.presentacion, p.talla AS genero " \
        "FROM gestion_perfumance.perfume p JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero")   

    perfume = cur.fetchall()     
    cur.close()
    conn.close()

    data = [{"id_perfume": row[0], "marca": row[1], "presentacion": row[2], "talla": row[3], "genero": row[4]} for row in perfume]
    return jsonify(data), 200

@catalogo_bp.route('/buscar', methods=['GET'])
def buscar_perfume():
    termino = request.args.get('q', '').strip().lower()
    if not termino:
        return jsonify({"error": "Falta el parámetro de búsqueda 'q'"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT marca, presentacion, talla, id_genero, stock, fecha_caducidad FROM gestion_perfumance.perfume WHERE LOWER(marca) ILIKE %s", (f'%{termino}%',))
    perfume = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"marca": row[0], "presentacion": row[1], "talla": row[2], "id_genero": row[3], "stock": row[4], "fecha_caducidad": row[5]} for row in perfume]
    return jsonify(data), 200