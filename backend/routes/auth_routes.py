import re
from flask import Blueprint, request, jsonify, session, current_app
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from config import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api')
ph = PasswordHasher()

def validar_datos_usuario(data):
    errores=[]

    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}$", data.get("nombres", "")):
        errores.append("Nombre inválido.")
    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}$", data.get("apellidos", "")):
        errores.append("Apellido inválido.")

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data.get("email", "")):
        errores.append("Correo electrónico inválido.")
    
    if not re.match(r"^[A-Za-z0-9_.-]{4,20}$", data.get("username", "")):
        errores.append("Usuario inválido. Solo letras, números y guiones.")
    
    if len(data.get("password", "")) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")
    
    return errores

@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json() or {}

    errores = validar_datos_usuario(data)
    if errores:
        return jsonify({"errores": errores}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""SELECT 1 
                    FROM gestion_perfumance.usuario 
                    WHERE username = %s OR email = %s""", 
                    (data['username'], data['email']))
        if cur.fetchone():
            return jsonify({"error": "El nombre de usuario o email ya existe"}), 400
        
        hashed_password = ph.hash(data['password'])    
    
        cur.execute("""INSERT INTO gestion_perfumance.cliente (nombres, apellidos, telefono, email) VALUES 
                    (%s, %s, %s, %s) RETURNING id_cliente""",
                    (data.get('nombres'), data.get('apellidos'), data.get('telefono'), data.get('email')))
        id_cliente = cur.fetchone()[0]

        cur.execute("""INSERT INTO gestion_perfumance.usuario (username, password, email, id_rol, activo, id_cliente) VALUES 
                    (%s, %s, %s, %s, TRUE, %s)""", 
                    (data.get('username'), hashed_password, data.get('email'), 3, id_cliente))
        conn.commit()
        return jsonify({"message": "Registro exitoso"}), 201
    
    except Exception as e:
        current_app.logger.error(f"Error en el registro: {e}")
        if conn:
            conn.rollback()  
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn:
            conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not (username and password):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT u.id_usuario, u.username, u.password, r.descripcion, u.activo 
                    FROM gestion_perfumance.usuario u
                    JOIN gestion_perfumance.rol r ON u.id_rol = r.id_rol
                    WHERE username = %s AND activo = TRUE;""", 
                    (username,))
        user = cur.fetchone()

        if  not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        if not user[4]:
            return jsonify({"error": "Cuenta inactiva"}), 403
    
        try:
            ph.verify(user[2], password)
        except VerifyMismatchError:
            return jsonify({"error": "Contraseña incorrecta"}), 401
        except (VerificationError, InvalidHash) as ve:
            current_app.logger.error(f"Error de verificación de contraseña: {ve}")
            return jsonify({"error": "Error interno del servidor"}), 500
    
        session['usuario'] ={
            'id_usuario': user[0],
            'username': user[1],
            'id_rol': user[3]
        }
        rol = user[3].strip().lower()

        if rol == 'gerente':
            destino = '/admin_dashboard'
        elif rol == 'empleado':
            destino = '/admin_pedidos'
        elif rol == 'cliente':
            destino = '/'
        else:
            destino = '/login'    

        return jsonify({
            "message": f"Bievenido {username}",
            "rol": user[3],
            "redirect": destino,
            'usuario': session['usuario']
            }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error en el login: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn:
            conn.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return jsonify({"message": "Sesión cerrada exitosamente"})
    
@auth_bp.route('/recuperar', methods=['POST'])
def recuperar():
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({"error": "El campo email es obligatorio"}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT username 
                    FROM gestion_perfumance.usuario 
                    WHERE email = %s""", 
                    (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "Email no encontrado"}), 404
        
        return jsonify({
            "message": f"Instrucciones de recuperación enviadas al {email}. Usuario:{row[0]}"
            }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error en la recuperación de contraseña: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn:
            conn.close()