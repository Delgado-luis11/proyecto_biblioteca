- Crear la tabla de usuarios si no existe
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
 
-- Insertar un usuario inicial con la contraseña hasheada
-- Recuerda que debes hashear la contraseña "777000" con el código en Python antes de insertar
-- La siguiente línea es un ejemplo de cómo insertar la contraseña ya hasheada.
INSERT INTO users (username, password)
VALUES 
('luis delgado', '$2b$12$eDwVSo9kqU2AxAfKxev1VQI8F3tQ5c5CT1jTt3xATjl4NACjVfT9e'); -- (Hash para la contraseña '777000')
