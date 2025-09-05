# OCR Service

Un servizio REST basato su FastAPI per eseguire OCR (Optical Character Recognition) su immagini e documenti PDF utilizzando Tesseract OCR.

## Caratteristiche

- Supporto per il riconoscimento testo in immagini (PNG, JPG, ecc.)
- Supporto per l'estrazione di testo da PDF
- Supporto multilingua (Inglese e Italiano preinstallati)
- API RESTful con documentazione automatica
- Containerizzato con Docker

## Requisiti di Sistema

- Python 3.9+
- Docker e Docker Compose (per l'esecuzione containerizzata)
- Tesseract OCR
- Poppler Utils (per la gestione dei PDF)

## Installazione

### Usando Docker (Raccomandato)

1. Clona il repository:
   ```bash
   git clone https://github.com/raVioleria16/srv-ocr.git
   cd srv-ocr
   ```

2. Costruisci e avvia il container:
   ```bash
   docker-compose up -d --build
   ```

Il servizio sarà disponibile su `http://localhost:6000`

### Installazione Locale

1. Clona il repository:
   ```bash
   git clone https://github.com/raVioleria16/srv-ocr.git
   cd srv-ocr
   ```

2. Installa le dipendenze di sistema:
   ```bash
   sudo apt-get update && sudo apt-get install -y \
       tesseract-ocr \
       tesseract-ocr-eng \
       tesseract-ocr-ita \
       poppler-utils \
       python3-dev \
       python3-pip \
       python3-setuptools \
       libjpeg-dev \
       zlib1g-dev
   ```

3. Crea e attiva un ambiente virtuale:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Installa le dipendenze Python:
   ```bash
   pip install -r requirements.txt
   ```

5. Avvia il servizio:
   ```bash
   python src/app.py
   ```

## Utilizzo

### Endpoint API

- `POST /api/v1/ocr`
  - Accetta file multipart/form-data con il campo "file"
  - Supporta immagini e PDF
  - Restituisce il testo estratto in formato JSON

### Esempi di Utilizzo

1. OCR su un'immagine:
```bash
curl -X POST -F "file=@immagine.png" http://localhost:6000/api/v1/ocr
```

Risposta:
```json
{
    "text": "testo estratto dall'immagine",
    "pages": 1
}
```

2. OCR su un PDF:
```bash
curl -X POST -F "file=@documento.pdf" http://localhost:6000/api/v1/ocr
```

Risposta:
```json
{
    "text": "testo completo del documento",
    "pages": 3,
    "pages_content": [
        "testo pagina 1",
        "testo pagina 2",
        "testo pagina 3"
    ]
}
```

## Sviluppo

### Struttura del Progetto

```srv-ocr/
├── src/
│   ├── app.py              # Applicazione FastAPI principale
│   ├── ocr_service/        # Logica OCR
│   │   └── tesseract_handler.py
│   └── routes/             # Route API
│       └── api.py
├── Dockerfile             
└── docker-compose.yml
```

## Licenza

### Esecuzione dei Test

```bash
# Installa le dipendenze di test
pip install -r tests/requirements_test.txt

# Esegui i test
pytest tests/ -v
```

## Licenza

MIT

## Autore

raVioleria16
