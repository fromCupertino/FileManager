# 📁 File Manager

### FastAPI + Vue 3 + Docker

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-green.svg)]()
[![Vue](https://img.shields.io/badge/Vue-3.x-42b883.svg)]()
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

------------------------------------------------------------------------

🇷🇺 [Русская версия](#-русская-версия) • 🇬🇧 [English Version](Overview)

------------------------------------------------------------------------

# 🚀 Overview

Modern full-stack file manager with upload, download, preview and delete
functionality.

Designed with:
- clean backend architecture
- typed configuration
- RESTful API
- Docker-based deployment
- production-ready structure
------------------------------------------------------------------------

# 🏗 Architecture

## Backend

-   FastAPI
-   OpenAPI 3.1 schema
-   Environment-based configuration
-   Configurable file storage directory

## Frontend

-   Vue 3 (Composition API)
-   Vite
-   Axios API integration
-   Responsive UI

## Infrastructure

-   Docker multi-container setup
-   Nginx frontend serving
-   Persistent volume storage

------------------------------------------------------------------------

# 📡 API

## GET `/files`

Returns list of stored files.

Query: - `limit` (optional, integer ≥ 1)

------------------------------------------------------------------------

## DELETE `/files`

Deletes one or multiple files.

Query: - `names` (required, comma-separated string)

------------------------------------------------------------------------

## GET `/download/{filename}`

Downloads file by name.

Query: - `preview=true` → inline response (iframe/img compatible)

------------------------------------------------------------------------

## POST `/upload`

Uploads one or multiple files.

Content-Type:

    multipart/form-data

Form field:

    files[]

------------------------------------------------------------------------

# 🐳 Run with Docker (Recommended)

``` bash
docker compose up --build
```

Available at: 
- Frontend → http://localhost\
- API → http://localhost:8000\
- Swagger Docs → http://localhost:8000/docs

Persistent storage: Docker volume `uploads_data`

Stop:

``` bash
docker compose down
```

------------------------------------------------------------------------

# 💻 Local Development

## Backend

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Frontend

``` bash
cd frontend/filemanager
npm install
npm run dev
```

------------------------------------------------------------------------

# 🔐 Environment Variables

| Variable      | Description      | Default                                        |
| ------------- | ---------------- | ---------------------------------------------- |
| UPLOAD_DIR    | Upload directory | ./src                                          |
| CORS_ORIGINS  | Allowed origins  | [http://localhost:5173](http://localhost:5173) |
| HOST          | API host         | 0.0.0.0                                        |
| PORT          | API port         | 8000                                           |
| VITE_API_BASE | API base URL     | [http://localhost:8000](http://localhost:8000) |


------------------------------------------------------------------------

# 🌍 Русская версия

## Описание

Full-stack приложение для управления файлами: 
- загрузка
- скачивание
- предпросмотр
- удаление

Проект демонстрирует: 
- грамотную архитектуру backend
- конфигурацию через env
- контейнеризацию
- структурированный REST API

------------------------------------------------------------------------

# 📄 License

MIT
