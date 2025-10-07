from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(10))  # 'Hombre' o 'Mujer'
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float)
    imagen_url = db.Column(db.String(255))
