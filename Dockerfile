FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para PaddleOCR
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/
COPY input_pdfs/ ./input_pdfs/
COPY output/ ./output/

# Comando por defecto
CMD ["python", "src/main.py"]
