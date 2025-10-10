# Usa una imagen base de Python pequeña
FROM python:3.11-slim as builder

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencia e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación
COPY app/ /app/app
COPY tests/ /app/tests

# Expone el puerto por defecto de Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app/main.py"]