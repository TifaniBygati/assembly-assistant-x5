# assembly-assistant-x5

FastAPI-проект для хранения клиентов и адресов доставки.

Проект хранит клиентов, их телефоны и связанные адреса. Один клиент может иметь несколько адресов.

## Технологии

- Python
- FastAPI
- PostgreSQL
- psycopg 3
- pytest
- Uvicorn

## Структура данных

Проект использует PostgreSQL.

Основные таблицы:

- `clients` — данные клиента:
  - `id`
  - `name`
  - `phone`

- `addresses` — адреса клиента:
  - `id`
  - `client_id`
  - `street`
  - `house`
  - `floor`
  - `entrance`
  - `apartment`
  - `comment`

Связь:

```text
addresses.client_id -> clients.id
```

Один клиент может иметь несколько адресов.

При удалении клиента его адреса удаляются автоматически через `ON DELETE CASCADE`.

## Формат ответа API

API возвращает клиентов в сгруппированном формате.

Пример клиента:

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

Контракт ответов:

```text
GET /clients                          -> list[client]
GET /clients/{client_id}              -> client
GET /clients/search                   -> list[client]
POST /clients                         -> client
PATCH /clients/{client_id}            -> client
PUT /clients/{client_id}              -> client
PATCH /clients/addresses/{address_id} -> client
PUT /clients/addresses/{address_id}   -> client
DELETE /clients/{client_id}           -> {"deleted_client_id": id}
```

## Данные

`data/database.json` используется как seed-файл для первичного заполнения базы.

Файл содержит исходные данные клиентов и адресов.

Поле `order_id` может присутствовать в JSON, но в текущей PostgreSQL-схеме не используется.

## Настройка PostgreSQL

Для разработки используется база:

```text
assembly_assistant_x5_dev
```

Для тестов используется база:

```text
assembly_assistant_x5_test
```

Имя базы можно переопределить через переменную окружения:

```bash
DB_NAME=assembly_assistant_x5_dev
```

## Создание таблиц

SQL-схема находится в файле:

```text
scripts/init_postgresql.sql
```

Скрипт создаёт таблицы `clients` и `addresses`, а также индекс для связи адресов с клиентами.

## Миграция данных из JSON в PostgreSQL

Для заполнения dev-базы из `data/database.json` используется скрипт:

```bash
python scripts/reset_and_seed_postgresql.py
```

Скрипт создаёт нужную базу при необходимости, пересоздаёт таблицы и загружает seed-данные.

## Запуск сервера

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Основные возможности API

- получить всех клиентов
- получить клиента по id
- найти клиентов по адресу
- создать клиента и адрес
- добавить новый адрес существующему клиенту по телефону
- частично обновить клиента
- частично обновить адрес
- полностью заменить данные клиента
- полностью заменить адрес
- удалить клиента вместе с его адресами

## Обработка ошибок

API возвращает понятные ошибки:

```text
400 -> некорректные данные запроса
404 -> клиент или адрес не найден
409 -> конфликт уникальности телефона
422 -> ошибка валидации FastAPI / Pydantic
```

Примеры `detail`:

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

## Тесты

Проект покрыт тестами через `pytest`.

Запуск всех тестов:

```bash
pytest
```

Тесты проверяют:

- health endpoint
- получение клиентов
- получение клиента по id
- поиск по адресу
- создание клиента
- обновление клиента
- обновление адреса
- удаление клиента
- негативные сценарии
- группировку плоских SQL-строк в клиентский response format

Тестовая база:

```text
assembly_assistant_x5_test
```

Перед тестами база пересоздаётся и заполняется тестовыми данными.

## Helper для группировки ответов

SQL-запросы после `JOIN` возвращают плоские строки.

Например:

```text
client_id | name | phone | address_id | street | house
```

Для API эти строки группируются в структуру:

```text
client -> addresses[]
```

Для этого используется helper:

```text
group_clients_with_addresses
```

Он принимает список плоских строк и возвращает список клиентов с вложенными адресами.

## Текущий статус проекта

Проект использует PostgreSQL, покрыт тестами через `pytest` и возвращает клиентов в сгруппированном формате: клиент с вложенным списком адресов `addresses`.