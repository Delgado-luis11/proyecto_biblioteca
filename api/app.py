from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
 
app = Flask(__name__)
CORS(app)
 
# Conectar a la base de datos PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'biblioteca'),
        user=os.getenv('POSTGRES_USER', 'user'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host='db',
        port='5432'
    )
    return conn
 
# Ruta para agregar un libro
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    year = data.get('year')
    if not title or not author or not year:
        return jsonify({'message': 'Faltan datos requeridos (title, author, year)'}), 400
 
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO books (title, author, year, is_available) VALUES (%s, %s, %s, %s)",
            (title, author, year, True)
        )
        conn.commit()
        return jsonify({'message': 'Libro agregado con éxito!'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error al agregar libro: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para buscar libros por título
@app.route('/books/search', methods=['GET'])
def search_book():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'message': 'La consulta no puede estar vacía'}), 400
 
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM books WHERE title ILIKE %s", (f"%{query}%",))
        books = cur.fetchall()
        if books:
            return jsonify(books), 200
        else:
            return jsonify({'message': 'No se encontró ningún libro con el título especificado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al buscar libro: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para obtener todos los libros disponibles
@app.route('/books/available', methods=['GET'])
def get_available_books():
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM books WHERE is_available = TRUE")
        books = cur.fetchall()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'message': f'Error al obtener libros disponibles: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para eliminar un libro por ID
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM books WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Libro eliminado con éxito'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error al eliminar libro: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para obtener el último libro alquilado
@app.route('/last_rented', methods=['GET'])
def get_last_rented_book():
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT title, cost FROM rented_books ORDER BY rented_at DESC LIMIT 1")
        book = cur.fetchone()
        if book:
            return jsonify({'title': book[0], 'cost': book[1]}), 200
        else:
            return jsonify({'message': 'No hay libros alquilados recientemente'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al obtener último libro alquilado: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
# Ruta para alquilar un libro
@app.route('/rent', methods=['POST'])
def rent_book():
    data = request.get_json()
    title = data.get('title')
    days = data.get('days')
    if not title or not days:
        return jsonify({'message': 'Faltan datos requeridos (title, days)'}), 400
 
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM books WHERE LOWER(title) = %s AND is_available = TRUE", (title.lower(),))
        book = cur.fetchone()
        if not book:
            return jsonify({'message': 'El libro no está disponible'}), 404
 
        cur.execute("UPDATE books SET is_available = FALSE WHERE id = %s", (book[0],))
        cost = round(days * 0.25, 2)
        cur.execute(
            "INSERT INTO rented_books (title, author, year, days, cost) VALUES (%s, %s, %s, %s, %s)",
            (book[1], book[2], book[3], days, cost)
        )
        conn.commit()
        return jsonify({'message': 'Libro alquilado con éxito', 'title': book[1], 'days': days, 'cost': cost}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error al alquilar libro: {e}'}), 500
    finally:
        cur.close()
        conn.close()
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
