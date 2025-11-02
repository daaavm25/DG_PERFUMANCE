from flask import Flask, render_template
from flask_cors import CORS
from flask_talisman import Talisman
from config import SECRET_KEY

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

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin_pedidos')
def admin_pedidos():
    return render_template('admin_pedidos.html')

@app.route('/admin_productos')
def admin_productos():
    return render_template('admin_productos.html')

@app.route('/admin_usuarios')
def admin_usuarios():
    return render_template('admin_usuarios.html')

@app.route('/catalogo_general')
def catalogo_general():
    from config import get_db_connection
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
    from config import get_db_connection
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
    from config import get_db_connection
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

@app.route('/pago')
def pago():
    return render_template('pago.html')

@app.route('/producto_detalle')
def producto_detalle():
    return render_template('producto_detalle.html')

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')


if __name__ == '__main__':
    app.run(debug=True)
