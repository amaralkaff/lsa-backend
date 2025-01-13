# FastAPI Project Template

## Deskripsi

Template proyek FastAPI dengan autentikasi, database, dan struktur dasar.

## Persyaratan

- Python 3.8+
- PostgreSQL

## Instalasi

1. Clone repositori ini

```bash
git clone <repository-url>
```

2. Buat virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
.\venv\Scripts\activate  # Windows
```

3. Install dependensi

```bash
pip install -r requirements.txt
```

4. Salin file .env.example ke .env dan sesuaikan konfigurasi

```bash
cp .env.example .env
```

5. Jalankan aplikasi

```bash
uvicorn app.main:app --reload
```

## Struktur Proyek

```
.
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── tests/
├── static/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## API Documentation

Setelah menjalankan aplikasi, dokumentasi API tersedia di:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
