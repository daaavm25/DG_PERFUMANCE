<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash, session
=======
# Contenido COMPLETO para tu app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
>>>>>>> origin/main
from flask_cors import CORS
from flask_talisman import Talisman
from config import SECRET_KEY, get_db_connection

from routes.auth_routes import auth_bp
from routes.catalogo_routes import catalogo_bp
from routes.carrito_routes import carrito_bp
from routes.venta_routes import venta_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True, origins="http://localhost:5000")
Talisman(app, content_security_policy=None)

app.register_blueprint(auth_bp)
app.register_blueprint(catalogo_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(venta_bp)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

# --- RUTAS DE ADMIN ---

@app.route('/admin_dashboard')
def admin_dashboard():
<<<<<<< HEAD
    conn = None
    total_productos = 0
    total_usuarios = 0
    total_pedidos = 0
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""SELECT COUNT(*)
                    FROM gestion_perfumance.perfume""")
        total_productos = cur.fetchone()[0]

        cur.execute("""SELECT COUNT(*)
                    FROM gestion_perfumance.usuario""")
        total_usuarios = cur.fetchone()[0]

        cur.execute("""SELECT COUNT(*)
                    FROM gestion_perfumance.venta""")
        total_usuarios = cur.fetchone()[0]
=======
    
    conn = None
    total_productos = 0
    total_usuarios = 0
    total_pedidos = 0 

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM gestion_perfumance.perfume")
        total_productos = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM gestion_perfumance.usuario")
        total_usuarios = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM gestion_perfumance.venta")
        total_pedidos = cur.fetchone()[0]

>>>>>>> origin/main
    except Exception as e:
        print(f"Error al cargar el dashboard: {e}")
    finally:
        if conn:
            conn.close()
<<<<<<< HEAD
    
    return render_template('admin_dashboard.html', 
                           total_prod = total_productos, 
=======

    return render_template('admin_dashboard.html', 
                           total_prod = total_productos,
>>>>>>> origin/main
                           total_usr = total_usuarios,
                           total_ped = total_pedidos)

@app.route('/admin_pedidos')
def admin_pedidos():
    pedidos = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT v.id_venta, c.nombres AS cliente_nombre, v.fecha_venta, v.monto_total
            FROM gestion_perfumance.venta v
            LEFT JOIN gestion_perfumance.cliente c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha_venta DESC
        """)
        
        rows = cur.fetchall()
        
        pedidos = [
            {
                "id_pedido": row[0],
                "cliente": row[1] or "Cliente Desconocido",
                "fecha": row[2].strftime('%Y-%m-%d %H:%M'),
                "total": "${:,.2f}".format(row[3])
            } for row in rows
        ]
        
    except Exception as e:
        print(f"Error al cargar pedidos: {e}")
        flash(f'Error al cargar pedidos: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return render_template('admin_pedidos.html', pedidos=pedidos)

@app.route('/admin_productos')
def admin_productos():
    perfumes = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.stock, g.descripcion AS genero_desc
            FROM gestion_perfumance.perfume p
            LEFT JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
            ORDER BY p.id_perfume
        """)
        rows = cur.fetchall()
        
        perfumes = [
            {
                "id_perfume": row[0],
                "marca": row[1],
                "presentacion": row[2],
                "talla": row[3],
                "stock": row[4],
                "genero_desc": row[5] or "Sin género"
            } for row in rows
        ]
        
    except Exception as e:
        flash(f'Error al cargar productos: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return render_template('admin_productos.html', perfumes=perfumes)

@app.route('/admin_usuarios')
def admin_usuarios():
    usuarios = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id_usuario, u.username, u.email, r.descripcion AS rol_desc
            FROM gestion_perfumance.usuario u
            LEFT JOIN gestion_perfumance.rol r ON u.id_rol = r.id_rol
            ORDER BY u.id_usuario
        """)
        rows = cur.fetchall()
        usuarios = [
            {
                "id_usuario": row[0],
                "username": row[1],
                "email": row[2],
                "rol": row[3] or "Sin Rol"
            } for row in rows
        ]
    except Exception as e:
        flash(f'Error al cargar usuarios: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return render_template('admin_usuarios.html', usuarios=usuarios)


# --- RUTAS PARA CREAR PERFUME ---
@app.route('/admin/perfume/nuevo', methods=['GET'])
def vista_crear_perfume():
    generos = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_genero, descripcion FROM gestion_perfumance.genero ORDER BY descripcion")
        rows = cur.fetchall()
        generos = [
            {"id_genero": row[0], "nombre": row[1]} for row in rows
        ]
    except Exception as e:
        flash(f'Error al cargar géneros: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return render_template('admin_crear_perfume.html', generos=generos)

@app.route('/admin/perfume/crear', methods=['POST'])
def crear_perfume():
    conn = None
    try:
        marca = request.form.get('marca')
        presentacion = request.form.get('presentacion')
        talla = request.form.get('talla')
        id_genero = request.form.get('id_genero')
        stock = request.form.get('stock')
        fecha_caducidad = request.form.get('fecha_caducidad')
        if not fecha_caducidad:
            fecha_caducidad = None
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO gestion_perfumance.perfume 
            (marca, presentacion, talla, id_genero, stock, fecha_caducidad) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (marca, presentacion, talla, int(id_genero), int(stock), fecha_caducidad))
        conn.commit()
        flash('¡Perfume agregado exitosamente!', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error al crear el perfume: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_productos'))

# --- RUTAS PARA EDITAR/ELIMINAR PERFUME ---
@app.route('/admin/perfume/eliminar/<int:id_perfume>')
def eliminar_perfume(id_perfume):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM gestion_perfumance.perfume WHERE id_perfume = %s", (id_perfume,))
        conn.commit()
        flash('Perfume eliminado exitosamente.', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        if 'foreign key constraint' in str(e).lower():
            flash('Error: No se puede eliminar un perfume que ya está en un pedido.', 'danger')
        else:
            flash(f'Error al eliminar el perfume: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_productos'))

@app.route('/admin/perfume/editar/<int:id_perfume>', methods=['GET'])
def vista_editar_perfume(id_perfume):
    perfume = None
    generos = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM gestion_perfumance.perfume WHERE id_perfume = %s", (id_perfume,))
        row = cur.fetchone()
        if row:
            perfume = {
                "id_perfume": row[0], "marca": row[1], "presentacion": row[2],
                "talla": row[3], "id_genero": row[4], "stock": row[5],
                "fecha_caducidad": str(row[6]) if row[6] else '' 
            }
        cur.execute("SELECT id_genero, descripcion FROM gestion_perfumance.genero ORDER BY descripcion")
        rows_generos = cur.fetchall()
        generos = [{"id_genero": g[0], "nombre": g[1]} for g in rows_generos]
    except Exception as e:
        flash(f'Error al cargar datos para editar: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    if perfume:
        return render_template('admin_editar_perfume.html', perfume=perfume, generos=generos)
    else:
        flash('No se encontró el perfume para editar.', 'danger')
        return redirect(url_for('admin_productos'))

@app.route('/admin/perfume/actualizar/<int:id_perfume>', methods=['POST'])
def actualizar_perfume(id_perfume):
    conn = None
    try:
        marca = request.form.get('marca')
        presentacion = request.form.get('presentacion')
        talla = request.form.get('talla')
        id_genero = request.form.get('id_genero')
        stock = request.form.get('stock')
        fecha_caducidad = request.form.get('fecha_caducidad')
        if not fecha_caducidad:
            fecha_caducidad = None
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            UPDATE gestion_perfumance.perfume
            SET marca = %s, presentacion = %s, talla = %s, id_genero = %s, stock = %s, fecha_caducidad = %s
            WHERE id_perfume = %s
        """
        cur.execute(sql, (marca, presentacion, talla, int(id_genero), int(stock), fecha_caducidad, id_perfume))
        conn.commit()
        flash('Perfume actualizado exitosamente.', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error al actualizar el perfume: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_productos'))


# --- RUTAS DE USUARIO ---
@app.route('/admin/usuario/nuevo', methods=['GET'])
def vista_crear_usuario():
    roles = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_rol, descripcion FROM gestion_perfumance.rol ORDER BY descripcion")
        rows = cur.fetchall()
        roles = [
            {"id_rol": row[0], "nombre": row[1]} for row in rows
        ]
    except Exception as e:
        flash(f'Error al cargar roles: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return render_template('admin_crear_usuario.html', roles=roles)

@app.route('/admin/usuario/crear', methods=['POST'])
def crear_usuario():
    conn = None
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        id_rol = request.form.get('id_rol')
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            INSERT INTO gestion_perfumance.usuario (username, password, email, id_rol, activo) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (username, hashed_password, email, int(id_rol), True))
        conn.commit()
        flash('¡Usuario creado exitosamente!', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        if 'unique constraint' in str(e).lower():
             flash('Error: El nombre de usuario o el email ya existen.', 'danger')
        else:
            flash(f'Error al crear el usuario: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuario/eliminar/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM gestion_perfumance.usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        flash('Usuario eliminado exitosamente.', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        if 'foreign key constraint' in str(e).lower():
            flash('Error: No se puede eliminar un usuario que ya ha realizado pedidos.', 'danger')
        else:
            flash(f'Error al eliminar el usuario: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuario/editar/<int:id_usuario>', methods=['GET'])
def vista_editar_usuario(id_usuario):
    usuario = None
    roles = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, username, email, id_rol, activo FROM gestion_perfumance.usuario WHERE id_usuario = %s", (id_usuario,))
        row = cur.fetchone()
        if row:
            usuario = {
                "id_usuario": row[0], "username": row[1], "email": row[2],
                "id_rol": row[3], "activo": row[4]
            }
        cur.execute("SELECT id_rol, descripcion FROM gestion_perfumance.rol ORDER BY descripcion")
        rows_roles = cur.fetchall()
        roles = [{"id_rol": r[0], "nombre": r[1]} for r in rows_roles]
    except Exception as e:
        flash(f'Error al cargar datos del usuario: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    if usuario:
        return render_template('admin_editar_usuario.html', usuario=usuario, roles=roles)
    else:
        flash('No se encontró el usuario para editar.', 'danger')
        return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuario/actualizar/<int:id_usuario>', methods=['POST'])
def actualizar_usuario(id_usuario):
    conn = None
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') 
        id_rol = request.form.get('id_rol')
        activo = 'activo' in request.form 
        conn = get_db_connection()
        cur = conn.cursor()
        if password:
            hashed_password = generate_password_hash(password)
            sql = """
                UPDATE gestion_perfumance.usuario
                SET username = %s, email = %s, password = %s, id_rol = %s, activo = %s
                WHERE id_usuario = %s
            """
            cur.execute(sql, (username, email, hashed_password, int(id_rol), activo, id_usuario))
        else:
            sql = """
                UPDATE gestion_perfumance.usuario
                SET username = %s, email = %s, id_rol = %s, activo = %s
                WHERE id_usuario = %s
            """
            cur.execute(sql, (username, email, int(id_rol), activo, id_usuario))
        conn.commit()
        flash('Usuario actualizado exitosamente.', 'success')
    except Exception as e:
        if conn:
            conn.rollback()
        if 'unique constraint' in str(e).lower():
             flash('Error: El nombre de usuario o el email ya existen.', 'danger')
        else:
            flash(f'Error al actualizar el usuario: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('admin_usuarios'))


# --- FIN DE RUTAS DE USUARIO ---


@app.route('/catalogo_general')
def catalogo_general():
    conn = get_db_connection() 
    cur = conn.cursor()
    cur.execute(""" SELECT id_perfume, marca
                FROM gestion_perfumance.perfume
                ORDER BY id_perfume;""")
    perfumes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('catalogo_general.html', perfumes=perfumes)

@app.route('/catalogo_hombre')
def catalogo_hombre():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(""" SELECT p.id_perfume, p.marca
                FROM gestion_perfumance.perfume p
                JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
                WHERE LOWER(g.descripcion) = 'hombre'
                ORDER BY p.id_perfume;""")
    perfumes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('catalogo_hombre.html', perfumes=perfumes)

@app.route('/catalogo_mujer')
def catalogo_mujer():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(""" SELECT p.id_perfume, p.marca
                FROM gestion_perfumance.perfume p
                JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
                WHERE LOWER(g.descripcion) = 'mujer'
                ORDER BY p.id_perfume;""")
    perfumes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('catalogo_mujer.html', perfumes=perfumes)

@app.route('/crear_cuenta')
def crear_cuenta():
    return render_template('crear_cuenta.html')

# --- ↓↓↓ ¡CAMBIO AQUÍ! (Bloque de datos falsos eliminado) ↓↓↓ ---
@app.route('/pago')
def pago():
    
    # --- TAREA PARA EL BACKEND ---
    # 1. Obtener los productos reales del carrito (ej: desde session['carrito'])
    # 2. Calcular los totales reales.
    # 3. Reemplazar 'items_reales' y 'resumen_real' con los datos correctos.
    #    Asegúrate de que 'resumen_real' sea un diccionario y 'items_reales' una lista.
    
    # (Valores por defecto para que la plantilla no se rompa)
    items_reales = [] 
    resumen_real = {
        "subtotal": 0.00,
        "envio": 0.00,
        "total": 0.00
    }
    
    # EJEMPLO DE LÓGICA DE BACKEND (COMENTADO):
    # try:
    #   (Aquí iría la lógica del backend para obtener el carrito de la sesión)
    #   items_reales = obtener_productos_del_carrito_de_la_sesion(session)
    #   resumen_real = calcular_totales_reales(items_reales)
    # except Exception as e:
    #   print(f"Error al cargar el carrito: {e}")
    #   flash('Error al cargar tu carrito.', 'danger')
    #   return redirect(url_for('carrito'))
    
    # El backend debe pasar las variables reales aquí
    return render_template('pago.html', resumen=resumen_real, items=items_reales)
# --- ↑↑↑ FIN DEL CAMBIO ↑↑↑ ---

@app.route('/producto_detalle')
def producto_detalle():
    return render_template('producto_detalle.html')

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

