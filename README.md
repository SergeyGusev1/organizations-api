# Справочник организаций — REST API

FastAPI + Pydantic + SQLAlchemy + Alembic + PostgreSQL + Docker

---

## Запуск через Docker (рекомендуемый способ)

```bash
# 1. Скопировать переменные окружения
cp .env.example .env

# 2. Поднять контейнеры (DB → миграции → seed → сервер)
docker compose up --build
```

API будет доступно на `http://localhost:8000`.
Документация Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

---

## Локальный запуск (без Docker)

```bash
pip install -r requirements.txt

# Создать .env с вашими настройками
cp .env.example .env

# Применить миграции
alembic upgrade head

# Заполнить тестовыми данными
python seed.py

# Запустить сервер
uvicorn app.main:app --reload
```

---

## Аутентификация

Все запросы требуют заголовок:

```
X-API-Key: supersecretapikey
```

Значение ключа задаётся через переменную окружения `API_KEY`.

---

## Генерация миграции после изменений моделей

```bash
alembic revision --autogenerate -m "describe changes"
alembic upgrade head
```

---

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/v1/organizations/{id}` | Организация по ID |
| GET | `/api/v1/organizations/by-building/{building_id}` | Организации в здании |
| GET | `/api/v1/organizations/by-activity/{activity_id}` | Организации по деятельности (рекурсивно) |
| GET | `/api/v1/organizations/search?name=...` | Поиск по названию |
| GET | `/api/v1/organizations/geo/radius?lat=&lon=&radius_km=` | Организации в радиусе |
| GET | `/api/v1/organizations/geo/rectangle?min_lat=&max_lat=&min_lon=&max_lon=` | Организации в прямоугольнике |
| GET | `/api/v1/buildings/` | Список зданий |
| GET | `/api/v1/buildings/{id}` | Здание по ID |
| GET | `/api/v1/activities/` | Дерево деятельностей |
| GET | `/api/v1/activities/{id}` | Деятельность по ID |

---

## Структура проекта

```
.
├── app/
│   ├── main.py              # точка входа FastAPI
│   ├── config.py            # настройки (pydantic-settings)
│   ├── database.py          # движок SQLAlchemy, get_db
│   ├── models/              # ORM-модели
│   ├── schemas/             # Pydantic-схемы запросов/ответов
│   ├── repositories/        # слой доступа к данным
│   ├── services/            # бизнес-логика
│   └── api/v1/              # роутеры FastAPI
├── alembic/                 # миграции
├── seed.py                  # тестовые данные
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
