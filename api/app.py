from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Conectar a la base de datos PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='db',
        port='5432'
    )
    return conn

# Ruta para agregar un libro
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    year = data['year']
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, year, is_available) VALUES (%s, %s, %s, %s)", (title, author, year, True))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Libro agregado con éxito!'}), 201

# Ruta para buscar libros por título exacto
@app.route('/books/search', methods=['GET'])
def search_book():
    query = request.args.get('query', '').lower()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE LOWER(title) = %s", (query,))
    books = cur.fetchall()
    cur.close()
    conn.close()
    if books:
        return jsonify(books), 200
    else:
        return jsonify({'message': 'No se encontró ningún libro con el título especificado'}), 404

# Ruta para obtener todos los libros disponibles
@app.route('/books/available', methods=['GET'])
def get_available_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE is_available = TRUE")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(books), 200

# Ruta para eliminar un libro por ID
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Libro eliminado con éxito'}), 200

# Ruta para obtener el último libro alquilado
@app.route('/last_rented', methods=['GET'])
def get_last_rented_book():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT title, cost FROM rented_books ORDER BY rented_at DESC LIMIT 1")
    book = cur.fetchone()
    cur.close()
    conn.close()
    if book:
        return jsonify({'title': book[0], 'cost': book[1]}), 200
    else:
        return jsonify({'message': 'No hay libros alquilados recientemente'}), 404

# Ruta para alquilar un libro
@app.route('/rent', methods=['POST'])
def rent_book():
    data = request.get_json()
    title = data['title']
    days = data['days']
    conn = connect_db()
    cur = conn.cursor()

    # Verificar si el libro está disponible
    cur.execute("SELECT * FROM books WHERE LOWER(title) = %s AND is_available = TRUE", (title.lower(),))
    book = cur.fetchone()
    if not book:
        return jsonify({'message': 'El libro no está disponible'}), 404

    # Marcar el libro como no disponible
    cur.execute("UPDATE books SET is_available = FALSE WHERE id = %s", (book[0],))
    conn.commit()

    # Calcular costo de alquiler
    cost = round(days * 0.25, 2)

    # Insertar el alquiler en la tabla rented_books
    cur.execute("INSERT INTO rented_books (title, author, year, days, cost) VALUES (%s, %s, %s, %s, %s)", (book[1], book[2], book[3], days, cost))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({'message': 'Libro alquilado con éxito', 'title': book[1], 'days': days, 'cost': cost}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
