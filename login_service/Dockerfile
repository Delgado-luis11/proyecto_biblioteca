   # Usa una imagen base de Python
   FROM python:3.9
 
   # Establece el directorio de trabajo en el contenedor
   WORKDIR /app
 
   # Copia el archivo requirements.txt al contenedor
   COPY requirements.txt /app/
 
   # Instala las dependencias
   RUN pip install -r requirements.txt
 
   # Copia el resto de la aplicación al contenedor
   COPY . /app/
 
   # Expone el puerto 6000 dentro del contenedor
   EXPOSE 6000
 
   # Comando para ejecutar la aplicación de Flask
   CMD ["python", "auth_service.py"]
