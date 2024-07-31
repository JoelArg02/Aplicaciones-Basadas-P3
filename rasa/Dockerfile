# Utilizar la imagen base de Python
FROM python:3.8-slim

# Actualizar pip
RUN pip install --upgrade pip

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos y el dominio
COPY requirements.txt ./
COPY domain.yml ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos restantes
COPY . .

# Exponer el puerto que usa Rasa (5005 por defecto)
EXPOSE 5005

# Comando para ejecutar el servidor Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
