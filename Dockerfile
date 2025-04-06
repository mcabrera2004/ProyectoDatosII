# Usar imagen base de Python 3.10
FROM python:3.12.6

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Variables de entorno para MongoDB Atlas (se configurarán en docker-compose)
ENV MONGO_URI=""
ENV DB_NAME="viajes_db"
