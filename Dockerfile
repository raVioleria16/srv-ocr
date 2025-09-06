FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ita \
    poppler-utils \
    python3-dev \
    python3-setuptools \
    libjpeg-dev \
    zlib1g-dev \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TUTTO il contenuto nella cartella /app
COPY . /app

EXPOSE 6000

CMD ["python", "app.py"]