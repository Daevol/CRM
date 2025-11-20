# AutoCare CRM Backend

FastAPI-бэкенд для CRM-системы автомоек и детейлинг-студий. Реализует модули клиентов, автомобилей, услуг, расписания, склада и финансового учета с JWT-аутентификацией.

## Стек
- Python 3.11
- FastAPI + SQLAlchemy
- PostgreSQL (по умолчанию SQLite для локального запуска)
- Redis/S3 могут быть добавлены отдельно

## Быстрый старт
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Установите переменную `CRM_DATABASE_URL` для работы с PostgreSQL (опционально). По умолчанию используется SQLite `./data.db`.
3. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Откройте документацию OpenAPI: http://localhost:8000/docs

## Основные эндпоинты
- `POST /auth/register` – регистрация пользователя.
- `POST /auth/login` – получение JWT.
- `POST /clients`, `GET /clients` – управление клиентами.
- `POST /vehicles`, `GET /vehicles/client/{client_id}` – автомобили клиентов.
- `POST /services`, `GET /services` – каталог услуг.
- `POST /bookings`, `GET /bookings`, `PATCH /bookings/{id}/status` – расписание и статусы.
- `POST /inventory/items`, `POST /inventory/movements`, `GET /inventory/*` – склад.
- `POST /finance/transactions`, `GET /finance/summary` – финансы.

## Тесты
Запуск интеграционного сценария:
```bash
pytest
```
