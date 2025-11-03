from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import get_db_connection # Importamos tu función de conexión

# 1. CREAMOS EL BLUEPRINT DE ADMIN
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- RUTA 2: DASHBOARD (GENERAL) ---
@admin_bp.route('/dashboard')
def admin_dashboard():
    total_prod = 0
    total_ped = 0
    total_usr = 0
    actividades = []

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""SELECT COUNT(*) 
                    FROM gestion_perfumance.perfume;""")
        total_prod = cur.fetchone()[0]

        cur.execute("""SELECT COUNT(*) 
                    FROM gestion_perfumance.venta;""")
        total_ped = cur.fetchone()[0]

        cur.execute("""SELECT COUNT(*) 
                    FROM gestion_perfumance.usuario;""")
        total_usr = cur.fetchone()[0]

        cur.execute("""SELECT a.descripcion, a.fecha, u.username, r.descripcion AS rol 
                    FROM gestion_perfumance.actividad a
                    JOIN gestion_perfumance.usuario u ON a.id_usuario = u.id_usuario
                    JOIN gestion_perfumance.rol r ON u.id_rol = r.id_rol
                    ORDER BY a.fecha DESC
                    LIMIT 8;""")
        rows = cur.fetchall()
        actividades = [{
            "descripcion": row[0],
            "fecha": row[1],
            "username": row[2],
            "rol": row[3]
        }for row in rows]

    except Exception as e:
        print(f"Error al cargar dashboard: {e}")
    finally:
        if conn:
            conn.close()
    print(f"Debug - Usuarios totales: {total_usr}")
    return render_template('admin_dashboard.html',
                           total_prod = total_prod,
                           total_ped = total_ped,
                           total_usr = total_usr, 
                           actividades = actividades)

# --- RUTA 3: GESTIÓN DE PRODUCTOS (TABLA) ---
@admin_bp.route('/productos')
def admin_productos():
    perfumes = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Consultamos los perfumes CON el nombre del género
        cur.execute("""
            SELECT p.id_perfume, p.marca, p.presentacion, p.talla, p.stock, g.descripcion AS genero_desc
            FROM gestion_perfumance.perfume p
            LEFT JOIN gestion_perfumance.genero g ON p.id_genero = g.id_genero
            ORDER BY p.id_perfume
        """)
        rows = cur.fetchall()
        
        # Convertimos las filas en una lista de diccionarios
        perfumes = [
            {
                "id_perfume": row[0],
                "marca": row[1],
                "presentacion": row[2],
                "talla": row[3],
                "stock": row[4],
                "genero_desc": row[5] or "Sin género" # 'or' para evitar Nulos
            } for row in rows
        ]
        
    except Exception as e:
        flash(f'Error al cargar productos: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return render_template('admin_productos.html', perfumes=perfumes)

# --- RUTA 4: GESTIÓN DE PEDIDOS ---
@admin_bp.route('/pedidos')
def admin_pedidos():
    return render_template('admin_pedidos.html')

# --- RUTA 5: GESTIÓN DE USUARIOS ---
@admin_bp.route('/usuarios')
def admin_usuarios():
    return render_template('admin_usuarios.html')

# ==========================================================
# ¡NUESTRAS NUEVAS RUTAS PARA AGREGAR PRODUCTOS!
# ==========================================================

# --- RUTA 6: MOSTRAR el formulario para crear un perfume (GET) ---
@admin_bp.route('/perfume/nuevo', methods=['GET'])
def vista_crear_perfume():
    generos = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Consultamos los géneros para llenar el <select>
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
            
    # Usamos el template que creaste en el paso anterior
    return render_template('admin_crear_perfume.html', generos=generos)


# --- RUTA 7: RECIBIR los datos del formulario (POST) ---
@admin_bp.route('/perfume/crear', methods=['POST'])
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
        
        # 2. Conectar y guardar en la base de datos
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

        usuario = session.get('usuario', {})
        id_usuario = usuario.get('id_usuario')
        descripcion = f"Agrego el perfume '{marca}' al catálogo."

        cur.execute("""INSER INTO gestion_perfumance.actividad (id_usuario, descripcion)
                    VALUES (%s, %s)""", 
                    (id_usuario, descripcion))
        conn.commit()
        flash('¡Perfume agregado exitosamente!', 'sucess')
    
    except Exception as e:
        if conn:
            conn.rollback() # Revertir si hay un error
        flash(f'Error al crear el perfume: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()

    # 4. Redirigir de vuelta a la lista de productos
    return redirect(url_for('admin.admin_productos'))