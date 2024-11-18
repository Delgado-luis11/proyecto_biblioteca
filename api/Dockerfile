# Usa una imagen base de Python
FROM python:3.9-slim
 
# Establece el directorio de trabajo
WORKDIR /usr/src/app
 
# Copia los archivos de requisitos y el código de tu aplicación
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
 
# Instala supervisord
RUN apt-get update && apt-get install -y supervisor && apt-get clean
 
# Copia tu archivo de configuración de supervisord
COPY supervisord.conf /etc/supervisord.conf
 
# Copia tu aplicación
COPY . .
 
# Comando para ejecutar supervisord
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
