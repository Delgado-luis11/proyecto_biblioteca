CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
-- Insertar un usuario de prueba (opcional)
-- INSERT INTO users (username, password) VALUES ('test_user', 'test_password');
-- Crear la tabla de libros alquilados si no existe
CREATE TABLE IF NOT EXISTS rented_books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    days INT NOT NULL,
    cost NUMERIC(5, 2) NOT NULL,
    rented_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar algunos libros de ejemplo en la tabla books
INSERT INTO books (title, author, year, is_available) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 1967, TRUE),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, TRUE),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', 1985, TRUE),
('1984', 'George Orwell', 1949, TRUE),
('Moby Dick', 'Herman Melville', 1851, TRUE),
('Orgullo y prejuicio', 'Jane Austen', 1813, TRUE),
('Crimen y castigo', 'Fiódor Dostoyevski', 1866, TRUE),
('El gran Gatsby', 'F. Scott Fitzgerald', 1925, TRUE),
('En busca del tiempo perdido', 'Marcel Proust', 1913, TRUE),
('Ulises', 'James Joyce', 1922, TRUE),
('El extranjero', 'Albert Camus', 1942, TRUE),
('Los hermanos Karamazov', 'Fiódor Dostoyevski', 1880, TRUE),
('La metamorfosis', 'Franz Kafka', 1915, TRUE),
('Cumbres borrascosas', 'Emily Brontë', 1847, TRUE),
('El retrato de Dorian Gray', 'Oscar Wilde', 1890, TRUE),
('La sombra del viento', 'Carlos Ruiz Zafón', 2001, TRUE),
('El principito', 'Antoine de Saint-Exupéry', 1943, TRUE),
('Rayuela', 'Julio Cortázar', 1963, TRUE),
('El Aleph', 'Jorge Luis Borges', 1949, TRUE),
('La casa de los espíritus', 'Isabel Allende', 1982, TRUE),
('Harry Potter y la piedra filosofal', 'J.K. Rowling', 1997, TRUE),
('El hobbit', 'J.R.R. Tolkien', 1937, TRUE);
