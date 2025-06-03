# Organization Catalog FastAPI

## Запуск проекта
- Скачайте проект: git clone https://github.com/EscapeFromHell/organization_catalog.git
- После скачивания проекта, перейдите в папку проекта: cd organization_catalog
- Выполните команду: docker compose up -d
- После запуска контейнеров, интерактивная документация будет доступна по ссылке: http://127.0.0.1:8000/docs#/

## Миграции и инициализация тестовых данных
Миграции накатятся автоматически.
При первом запуске в базу автоматически добавляются:

- 10 зданий
- 10 активностей (вложенность до 3 уровней)
- 20 организаций
- Cвязи организаций и активностей

## Статический API-ключ
При каждом запросе в заголовке необходимо передавать api-key: "secret_api_key"

## Эндпоинты

### Activities

- GET /api_v1/activities — Список всех активностей.
- GET /api_v1/activities/{activity_id} — Получить активность по ID.
- POST /api_v1/activities — Создание активности.
- PUT /api_v1/activities/{activity_id} — Обновление активности.
- DELETE /api_v1/activities/{activity_id} — Удаление активности.

### Buildings:

- GET /api_v1/buildings — Получить список всех зданий.
- GET /api_v1/buildings/{building_id} — Получить здание по ID.
- GET /api_v1/buildings/buildings_by_radius — Поиск зданий в радиусе.
- POST /api_v1/buildings — Создание нового здания.
- PUT /api_v1/buildings/{building_id} — Обновление информации о здании.
- DELETE /api_v1/buildings/{building_id} — Удаление здания.

### Organizations:

- GET /api_v1/organizations — Список всех организаций.
- GET /api_v1/organizations/{organization_id} — Получить организацию по ID.
- GET /api_v1/organizations/by_building/{building_id} — Список организаций в здании.
- GET /api_v1/organizations/by_activity — Список организаций по названию активности.
- GET /api_v1/organizations/by_activity_tree — Список организаций по названию активности (учитывая вложенность активностей).
- GET /api_v1/organizations/by_radius — Организации по геолокации.
- GET /api_v1/organizations/by_name — Поиск организаций по названию.
- POST /api_v1/organizations — Создание организации.
- PUT /api_v1/organizations/{organization_id} — Обновление организации.
- DELETE /api_v1/organizations/{organization_id} — Удаление организации.

## Технологии
Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, Docker
