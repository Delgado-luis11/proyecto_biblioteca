# Usa una imagen base ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias y las instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Expone el puerto de la aplicación
EXPOSE 5001

# Comando para ejecutar la aplicación
CMD ["python", "auth_service.py"]
