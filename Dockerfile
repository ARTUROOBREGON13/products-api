# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del proyecto
COPY . .

# Exponer el puerto en el que corre Flask
EXPOSE 5000

# Variables de entorno necesarias para Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production  

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
