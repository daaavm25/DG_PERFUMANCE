from app import create_app  # Importa la función create_app desde app

app = create_app()  # Crea la aplicación Flask


if __name__ == "__main__":
    app.run(debug=True, port=5001)
