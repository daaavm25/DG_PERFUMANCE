# Contenido para 'proyecto/routes/admin_routes.py' (Archivo NUEVO)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import get_db_connection # Importamos tu función de conexión

# 1. CREAMOS EL BLUEPRINT DE ADMIN
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# --- RUTA 2: DASHBOARD (GENERAL) ---
@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    # (Aquí irá la lógica para contar productos, pedidos, etc.)
    return render_template('admin_dashboard.html')

# --- RUTA 3: GESTIÓN DE PRODUCTOS (TABLA) ---
@admin_bp.route('/admin/productos')
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
@admin_bp.route('/admin/pedidos')
def admin_pedidos():
    return render_template('admin_pedidos.html')

# --- RUTA 5: GESTIÓN DE USUARIOS ---
@admin_bp.route('/admin/usuarios')
def admin_usuarios():
    return render_template('admin_usuarios.html')

# ==========================================================
# ¡NUESTRAS NUEVAS RUTAS PARA AGREGAR PRODUCTOS!
# ==========================================================

# --- RUTA 6: MOSTRAR el formulario para crear un perfume (GET) ---
@admin_bp.route('/admin/perfume/nuevo', methods=['GET'])
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
@admin_bp.route('/admin/perfume/crear', methods=['POST'])
def crear_perfume():
    conn = None
    try:
        # 1. Recibir todos los datos del formulario
        marca = request.form.get('marca')
        presentacion = request.form.get('presentacion')
        talla = request.form.get('talla')
        id_genero = request.form.get('id_genero')
        stock = request.form.get('stock')
        fecha_caducidad = request.form.get('fecha_caducidad')
        
        # Pequeña conversión por si la fecha viene vacía
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
    
    except Exception as e:
        if conn:
            conn.rollback() # Revertir si hay un error
        flash(f'Error al crear el perfume: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()

    # 4. Redirigir de vuelta a la lista de productos
    return redirect(url_for('admin.admin_productos'))