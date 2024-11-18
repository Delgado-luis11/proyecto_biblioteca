from flask import Flask, request, jsonify, redirect, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import jwt
import datetime
import os
from dotenv import load_dotenv
 
load_dotenv()
 
app = Flask(__name__)
# Clave secreta: es mejor almacenarla en una variable de entorno para seguridad.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_secreto')  # Cambia a una clave segura
 
# Configuración de conexión a la base de datos
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="login_db",
            user="login_user",
            password="login_password",
            host="login_db",  # Nombre del servicio en Docker
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
 
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')
 
# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Faltan datos (username y password)"}), 400
    # Hashear la contraseña
    hashed_password = generate_password_hash(password, method='sha256')
    # Conectar a la base de datos
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Error en la conexión a la base de datos"}), 500
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()
        return jsonify({"message": "Usuario registrado con éxito"}), 201
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return jsonify({"message": "Error al registrar el usuario"}), 500
    finally:
        conn.close()
 
# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Faltan datos (username y password)"}), 400
    # Conectar a la base de datos
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Error en la conexión a la base de datos"}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
    except Exception as e:
        print(f"Error al consultar usuario: {e}")
        return jsonify({"message": "Error al validar credenciales"}), 500
    finally:
        conn.close()
    # Verificar si el usuario existe y si la contraseña es correcta
    if user and check_password_hash(user[0], password):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"message": "Login exitoso", "token": token, "redirect_url": "http://api:5000"}), 200
    return jsonify({"message": "Credenciales inválidas"}), 401
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
