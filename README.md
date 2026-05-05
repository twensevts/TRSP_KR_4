# Контрольная работа №4

Минимальный FastAPI-проект для выполнения заданий про Alembic, пользовательские ошибки, валидацию и async-тесты.

## Что установить

1. Python 3.11+.
2. Виртуальное окружение.
3. Зависимости из `requirements.txt`.

Пример для Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Чек-лист запуска

1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости из `requirements.txt`.
3. Примените миграции Alembic (добавляет два примера записей Product).
4. Запустите тесты, чтобы проверить функциональность.
5. Запустите приложение, если нужно.

## Миграции

Перед миграциями убедитесь, что venv активирован:

```powershell
.\.venv\Scripts\Activate.ps1
```

Применить все миграции (включая добавление двух примеров записей Product):

```powershell
alembic upgrade head
```

Сгенерировать новую миграцию, если модель изменилась:

```powershell
alembic revision --autogenerate -m "message"
```

## Запуск приложения

Убедитесь, что venv активирован:

```powershell
.\.venv\Scripts\Activate.ps1
```

Запустить приложение:

```powershell
uvicorn app.main:app --reload
```

После старта откройте:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Тесты

Убедитесь, что venv активирован:

```powershell
.\.venv\Scripts\Activate.ps1
```

Запустить тесты:

```powershell
pytest
```

## Что уже есть в проекте

- Alembic-конфигурация и две миграции для `Product`.
- Пользовательские исключения и обработчики ошибок.
- Проверка входных данных через Pydantic.
- Асинхронные тесты через `pytest-asyncio` и `httpx.AsyncClient`.
- Генерация тестовых данных через `Faker`.

## Основные ручные сценарии

1. `POST /users` - создать пользователя.
2. `GET /users/{user_id}` - получить пользователя.
3. `DELETE /users/{user_id}` - удалить пользователя.
4. `POST /validated-users` - проверить пользовательские данные.
5. `GET /errors/a` и `GET /errors/b` - увидеть кастомные ошибки.
