import os
from flask import Flask, send_from_directory, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.routes.covid import covid_bp # Importa el blueprint de rutas de COVID

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__, static_folder='static')

# --- Configuración de la Base de Datos ---
# Obtener la URL de la base de datos de las variables de entorno de Vercel
# Si no está definida (ej. en desarrollo local sin .env), puedes poner un valor por defecto o lanzar un error.
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    # IMPORTANTE: Si estás desarrollando localmente sin una variable de entorno,
    # puedes poner aquí tu URI de DB local para pruebas.
    raise ValueError("DATABASE_URL environment variable not set. Cannot connect to database.")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Pasar el engine a la configuración de la aplicación para que otros módulos puedan acceder a él
app.config['DB_ENGINE'] = engine
app.config['DB_SESSION'] = sessionmaker(bind=engine) # Opcional: para manejar sesiones de forma más directa


# --- Registro de Blueprints (Módulos de Rutas) ---
# Registra el blueprint de COVID con su prefijo de URL
app.register_blueprint(covid_bp, url_prefix='/api/covid')

# --- Rutas Adicionales ---
# Ruta para servir el archivo HTML principal (el dashboard frontend)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Ruta para servir otros archivos estáticos (CSS, JS, imágenes)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# --- Manejo Global de Errores ---
@app.errorhandler(500)
def internal_server_error(e):
    # Esto capturará cualquier 500 no manejado en las rutas
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"error": "Not Found", "message": "La ruta solicitada no existe."}), 404


# --- Inicio de la Aplicación (para desarrollo local) ---
if __name__ == '__main__':
    # Esto solo se ejecuta si corres main.py directamente (ej. python main.py)
    # En Vercel, Gunicorn u otro servidor WSGI iniciará la app, no este bloque.
    print(f"Flask app running on http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)
