# assembly-assistant-x5

Backend-приложение на FastAPI для хранения клиентов и связанных с ними адресов доставки.

Один клиент может иметь несколько адресов. Проект поддерживает CRUD-операции, поиск клиентов по адресу, валидацию данных, обработку ошибок и работу с PostgreSQL через SQLAlchemy ORM.

## Технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic
- psycopg 3
- pytest
- Docker
- Docker Compose
- GitHub Actions
- GHCR
- Uvicorn

## Возможности API

API позволяет:

- получить список клиентов;
- получить клиента по `id`;
- найти клиентов по адресу;
- создать клиента с адресом;
- добавить новый адрес существующему клиенту;
- частично обновить клиента;
- полностью заменить данные клиента;
- частично обновить адрес;
- полностью заменить адрес;
- удалить клиента вместе со всеми его адресами.

Основные endpoints:

```text
GET    /clients
GET    /clients/{client_id}
GET    /clients/search

POST   /clients

PATCH  /clients/{client_id}
PUT    /clients/{client_id}

PATCH  /clients/addresses/{address_id}
PUT    /clients/addresses/{address_id}

DELETE /clients/{client_id}
```

## Структура данных

Проект использует PostgreSQL.

Основные таблицы:

### clients

```text
id
name
phone
```

### addresses

```text
id
client_id
street
house
floor
entrance
apartment
comment
```

Связь между таблицами:

```text
addresses.client_id -> clients.id
```

Один клиент может иметь несколько адресов.

При удалении клиента связанные адреса удаляются через:

```text
ON DELETE CASCADE
```

Для `addresses.client_id` создан индекс.

## Пример ответа API

```json
{
  "client_id": 1,
  "name": "Дима",
  "phone": "+79990000001",
  "addresses": [
    {
      "address_id": 1,
      "street": "Пушкина",
      "house": "7",
      "floor": "5",
      "entrance": "2",
      "apartment": "17",
      "comment": "домофон не работает"
    }
  ]
}
```

## PostgreSQL

Для локальной разработки используется база:

```text
assembly_assistant_x5_dev
```

Для тестов:

```text
assembly_assistant_x5_test
```

Настройки подключения задаются через переменные окружения:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
```

## Миграции Alembic

Структура базы данных управляется через Alembic.

ORM-модели описывают желаемую схему приложения, а migration-файлы хранят историю изменений структуры базы.

Применить все миграции до актуальной версии:

```bash
alembic upgrade head
```

Посмотреть текущую revision базы:

```bash
alembic current
```

Посмотреть историю миграций:

```bash
alembic history
```

Также миграции можно применить через вспомогательный скрипт:

```bash
python scripts/init_postgresql.py
```

Скрипт предполагает, что сама PostgreSQL database уже существует.

## Seed-данные

Начальные данные хранятся в:

```text
seed/initial_clients.json
```

Для загрузки seed-данных в уже подготовленную базу:

```bash
python scripts/seed_postgresql.py
```

Скрипт подключается к уже подготовленной базе данных и загружает начальные данные, если база ещё не заполнена.

## Сброс dev-данных

Для очистки данных и повторной загрузки seed-набора в PowerShell:

```powershell
$env:ALLOW_DB_RESET="true"
python scripts/reset_and_seed_postgresql.py
```

Скрипт:

```text
очищает clients и addresses
        ↓
сбрасывает значения identity
        ↓
сохраняет структуру базы
        ↓
повторно загружает seed-данные
```

Структура базы при этом не пересоздаётся и остаётся под управлением Alembic.

Без:

```text
ALLOW_DB_RESET=true
```

сброс базы блокируется.

## Запуск приложения

Локальный запуск:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
GET /health
```

## Docker

Проект поддерживает запуск через Docker Compose.

```bash
docker compose up
```

Compose поднимает:

```text
PostgreSQL
+
FastAPI application
```

При первой инициализации PostgreSQL создаёт database через переменную:

```text
POSTGRES_DB
```

После создания database структура должна быть приведена к актуальной версии через Alembic.

## Тесты

Проект покрыт тестами через `pytest`.

Локальный запуск:

```bash
pytest
```

Текущий набор содержит:

```text
34 tests
```

Тесты проверяют:

- health endpoint;
- получение клиентов;
- получение клиента по `id`;
- поиск по адресу;
- создание клиента;
- обновление клиента;
- обновление адреса;
- удаление клиента;
- обработку несуществующих ресурсов;
- некорректные payload;
- конфликты уникальности;
- валидацию входных данных;
- вспомогательную логику формирования API-ответов.

Перед тестами используется отдельная база:

```text
assembly_assistant_x5_test
```

Тестовый setup:

```text
создаёт test database при необходимости
        ↓
Alembic upgrade head
        ↓
очищает тестовые данные
        ↓
загружает тестовый набор
        ↓
запускает тест
```

Таким образом тестовая схема создаётся теми же Alembic-миграциями, которые используются для dev и production.

## Тесты в Docker

Тестовый Docker image содержит:

```text
app/
tests/
scripts/
alembic/
alembic.ini
```

Запуск:

```bash
docker compose -f compose.test.yaml up
```

Успешный прогон:

```text
34 passed
```

## Обработка ошибок

API использует стандартные HTTP-коды:

```text
400 -> некорректные данные
404 -> клиент или адрес не найден
409 -> конфликт уникальности
422 -> ошибка валидации FastAPI / Pydantic
```

Примеры ответов:

```json
{"detail": "client_not_found"}
```

```json
{"detail": "address_not_found"}
```

```json
{"detail": "no_update_fields"}
```

```json
{"detail": "invalid_phone"}
```

```json
{"detail": "invalid_street"}
```

```json
{"detail": "invalid_house"}
```

```json
{"detail": "phone_already_exists"}
```

## CI/CD

GitHub Actions используется для проверки, публикации и развёртывания проекта.

Pipeline включает:

```text
build Docker image
        ↓
container tests
        ↓
publish image to GHCR
        ↓
deploy to VDS
```

Production image публикуется в GitHub Container Registry.

Deployment выполняется на VDS через SSH.

Перед запуском новой версии приложения production-база должна быть приведена к актуальной revision через:

```bash
alembic upgrade head
```

## Текущий статус

Проект переведён с ручного создания PostgreSQL-схемы на SQLAlchemy ORM и Alembic.

Схема базы для:

```text
development
testing
production
```

управляется единым набором migration-файлов.

Тесты выполняются как локально, так и внутри Docker-контейнера.