from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
 
app = Flask(__name__)
CORS(app)
 
# Configuración para conectarse a la base de datos PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'biblioteca'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'db'),  # Nombre del servicio de la base de datos en Docker Compose
        port=os.getenv('POSTGRES_PORT', '5432')
    )
 
# Ruta para registrar un nuevo usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
 
    if not username or not password:
        return jsonify({'message': 'El username y password son requeridos.'}), 400
 
    conn = connect_db()
    cur = conn.cursor()
 
    try:
        # Verificar si el usuario ya existe
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({'message': 'El usuario ya existe.'}), 409
 
        # Registrar nuevo usuario
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return jsonify({'message': 'Usuario registrado exitosamente.'}), 201
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'message': f'Error al registrar usuario: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
 
    if not username or not password:
        return jsonify({'message': 'El username y password son requeridos.'}), 400
 
    conn = connect_db()
    cur = conn.cursor()
 
    try:
        # Verificar credenciales
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        if user:
            return jsonify({'message': 'Inicio de sesión exitoso.'}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas.'}), 401
    except psycopg2.Error as e:
        return jsonify({'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para obtener la lista de usuarios (opcional, solo para pruebas)
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cur = conn.cursor()
 
    try:
        cur.execute("SELECT id, username FROM users")
        users = cur.fetchall()
        user_list = [{'id': u[0], 'username': u[1]} for u in users]
        return jsonify(user_list), 200
    except psycopg2.Error as e:
        return jsonify({'message': f'Error al obtener usuarios: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Iniciar el servicio Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
