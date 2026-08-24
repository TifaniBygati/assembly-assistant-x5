# assembly-assistant-x5

Backend-проект на FastAPI для хранения клиентов и связанных с ними адресов доставки.

Проект создавался как учебный backend-проект и постепенно развивался от простого API с PostgreSQL до приложения с SQLAlchemy ORM, автоматическими тестами, Docker и CI/CD.

## Возможности

- CRUD для клиентов
- работа с несколькими адресами одного клиента
- поиск клиентов по адресу
- частичное обновление через PATCH
- полное обновление через PUT
- удаление клиента вместе со связанными адресами
- проверка уникальности телефонного номера
- обработка ошибок API
- отдельная PostgreSQL-база для тестов

## Стек

- Python
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- psycopg 3
- Pydantic
- pytest
- Docker
- Docker Compose
- GitHub Actions
- GHCR

## Архитектура

Основной поток запроса:

HTTP request  
→ FastAPI router  
→ dependency injection  
→ SQLAlchemy Session  
→ service layer  
→ PostgreSQL

SQLAlchemy `Engine` создаётся один раз при запуске приложения.

Для каждого HTTP-запроса FastAPI получает отдельную `Session` через `Depends(get_session)`. После завершения запроса Session закрывается.

Service-функции получают готовую Session и не управляют её жизненным циклом самостоятельно.

## Структура данных

Основные сущности:

### clients

- `id`
- `name`
- `phone`

### addresses

- `id`
- `client_id`
- `street`
- `house`
- `floor`
- `entrance`
- `apartment`
- `comment`

Связь:

`addresses.client_id → clients.id`

Один клиент может иметь несколько адресов.

Удаление клиента удаляет связанные адреса через PostgreSQL `ON DELETE CASCADE`.

## API

Основные endpoints:

`GET /clients` — получить всех клиентов

`GET /clients/{client_id}` — получить клиента по id

`GET /clients/search` — поиск клиентов по адресу

`POST /clients` — создать клиента или добавить адрес существующему клиенту

`PATCH /clients/{client_id}` — частично изменить клиента

`PUT /clients/{client_id}` — полностью изменить клиента

`PATCH /clients/addresses/{address_id}` — частично изменить адрес

`PUT /clients/addresses/{address_id}` — полностью изменить адрес

`DELETE /clients/{client_id}` — удалить клиента

Swagger UI после запуска приложения:

`http://127.0.0.1:8000/docs`

## Формат ответа

Клиент возвращается вместе со связанными адресами:

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

## Обработка ошибок

API обрабатывает основные негативные сценарии:

- `400` — некорректные данные
- `404` — клиент или адрес не найден
- `409` — конфликт уникальности телефона
- `422` — ошибка валидации FastAPI / Pydantic

## Тестирование

Проект покрыт автоматическими тестами через pytest.

Сейчас тестовый набор содержит 34 теста.

Проверяются:

- health endpoint
- GET endpoints
- поиск клиентов
- POST
- PATCH
- PUT
- DELETE
- негативные сценарии
- response helpers

Тесты используют отдельную PostgreSQL-базу:

`assembly_assistant_x5_test`

FastAPI dependency `get_session` во время тестов подменяется тестовой dependency через `app.dependency_overrides`.

## Docker

Проект поддерживает отдельные Docker-конфигурации для разработки, тестирования и production.

Тесты могут запускаться в отдельном Docker-контейнере вместе с отдельным PostgreSQL-сервисом через Docker Compose.

Внутри Compose сервисы взаимодействуют через внутреннюю Docker network.

## CI/CD

GitHub Actions автоматически:

1. запускает контейнерные тесты для pull request;
2. собирает Docker image;
3. публикует production image в GitHub Container Registry;
4. маркирует image тегами `latest` и commit SHA;
5. выполняет автоматический deployment на VDS.

Изменения в `main` проходят через pull request workflow.

## Локальный запуск

Установить зависимости:

pip install -r requirements.txt

Запустить FastAPI:

uvicorn app.main:app --reload

Также проект поддерживает запуск через Docker Compose.

## Конфигурация

Подключение к PostgreSQL задаётся через переменные окружения:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Пример конфигурации находится в `.env.example`.

## Seed-данные

Seed-данные клиентов и адресов хранятся отдельно от application-кода.

Для подготовки dev-базы используются вспомогательные PostgreSQL scripts.

## Статус проекта

Проект активно развивается.

Реализованы FastAPI REST API, PostgreSQL, SQLAlchemy ORM, автоматические тесты, контейнеризация и CI/CD.

Следующий этап развития проекта — управление изменениями схемы PostgreSQL через Alembic.