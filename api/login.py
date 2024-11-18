from flask import Blueprint, request, redirect, url_for, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
 
# Crear el Blueprint para el login
auth = Blueprint('auth', __name__)
 
# Configuración de conexión a la base de datos
def get_db_connection():
    connection = psycopg2.connect(
        host='db',  # Nombre del servicio definido en docker-compose
        database='biblioteca',
        user='user',
        password='password'
    )
    return connection
 
# Ruta para el login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        # Consultar el usuario en la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
 
        # Verificar las credenciales
        if user and check_password_hash(user[2], password):  # user[2] es el campo de la contraseña
            session['username'] = username
            return redirect(url_for('biblioteca'))
        return "Credenciales incorrectas", 401
    # Mostrar formulario de login si es una solicitud GET
    return render_template('login.html')
 
# Ruta para el registro (opcional, en caso de que quieras permitir el registro de nuevos usuarios)
@auth.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
 
    # Insertar el usuario en la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                   (username, password))
    connection.commit()
    cursor.close()
    connection.close()
 
    return "Usuario registrado correctamente", 201
