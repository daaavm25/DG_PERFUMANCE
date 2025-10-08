from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from argon2 import PasswordHasher
from config import get_db_connection

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()

@auth_bp.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor()

    if not (nombres and apellidos and telefono and email and username and  password ):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    cur.execute("INSERT INTO gestion_perfumance.cliente (nombres, apellidos, telefono, email) VALUES (%s, %s, %s, %s) RETURNING id_cliente", (nombres, apellidos, telefono, email))
    id_cliente = cur.fetchone()[0]
    hashed_password = ph.hash(password)
    cur.execute("INSERT INTO gestion_perfumance.usuario (username, password, email, id_rol, activo, id_cliente) VALUES (%s, %s, %s, 3, %s, %s)", (username, hashed_password, email, id_cliente))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Registro exitoso"}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get['username']
    password = data.get['password']

    if not (username and password):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, username, password, id_rol, activo FROM gestion_perfumance.usuario WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if  not row:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    try:
        ph.verify(row[2], password)
    except:
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    if not row[4]:
        return jsonify({"error": "Usuario inactivo"}), 403
    return jsonify({"message": "Login exitoso", "user": {"id_usuario": row[0], "username": row[1], "id_rol": row[3]}}), 200 

    
@auth_bp.route('/recuperar', methods=['POST'])
def recuperar():
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({"error": "El campo email es obligatorio"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM gestion_perfumance.usuario WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Email no encontrado"}), 404

    return jsonify({"message": f"Instrucciones de recuperación enviadas al {email} (usuario:[username])"}), 200