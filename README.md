# File Manager (FastAPI + Vue)

Веб-приложение для загрузки и скачивания файлов: бэкенд на FastAPI, фронтенд на Vue 3 + Vite.

## Требования

- **Локальный запуск:** Python 3.12+, Node.js 20+
- **Docker:** Docker и Docker Compose

---

## Запуск через Docker (рекомендуется)

1. Клонируйте репозиторий и перейдите в каталог проекта.

2. Запустите сервисы:
   ```bash
   docker compose up --build
   ```

3. Откройте в браузере:
   - **Фронтенд:** http://localhost
   - **API:** http://localhost:8000  
   Документация API: http://localhost:8000/docs

Файлы сохраняются в Docker volume `uploads_data` и не теряются при перезапуске контейнеров.

Остановка:
```bash
docker compose down
```

---

## Локальный запуск (без Docker)

### 1. Бэкенд

```bash
# Виртуальное окружение (по желанию)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Зависимости
pip install -r requirements.txt

# Опционально: скопировать и отредактировать переменные
cp .env.example .env

# Запуск
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен на http://localhost:8000

### 2. Фронтенд

В **другом** терминале:

```bash
cd frontend/filemanager

npm install
npm run dev
```

Фронтенд откроется на http://localhost:5173 и по умолчанию будет обращаться к API на http://localhost:8000.

---

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `UPLOAD_DIR` | Папка для загружаемых файлов | `./src` |
| `CORS_ORIGINS` | Разрешённые origins через запятую | `http://localhost:5173` |
| `HOST` | Хост сервера | `0.0.0.0` |
| `PORT` | Порт сервера | `8000` |
| `VITE_API_BASE` | URL API для фронтенда (при сборке) | `http://localhost:8000` |

Для локальной разработки бэкенда можно создать файл `.env` в корне проекта (по образцу `.env.example`).  
Для Docker переменные задаются в `docker-compose.yml` или в файле `.env` рядом с `docker-compose.yml` (например, `VITE_API_BASE` для сборки фронта).

---

## Структура проекта

```
.
├── main.py              # FastAPI-приложение
├── config.py            # Конфигурация из env
├── requirements.txt
├── Dockerfile           # Образ бэкенда
├── docker-compose.yml   # Backend + Frontend
├── .env.example
└── frontend/filemanager # Vue 3 + Vite
    ├── src/
    ├── Dockerfile       # Сборка + nginx
    └── nginx.conf
```

---

## Деплой

1. Настройте `.env` (или переменные в окружении):
   - `CORS_ORIGINS` — ваш домен фронтенда (например, `https://app.example.com`).
   - `VITE_API_BASE` — публичный URL API (например, `https://api.example.com`).

2. Пересоберите фронтенд с нужным `VITE_API_BASE`:
   ```bash
   VITE_API_BASE=https://api.example.com docker compose build frontend
   ```

3. Запустите:
   ```bash
   docker compose up -d
   ```

При использовании обратного прокси (nginx/traefik) убедитесь, что в `CORS_ORIGINS` указан реальный origin, с которого открывается фронтенд.
