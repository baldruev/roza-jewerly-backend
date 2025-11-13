# ===== Константы =====
DC := docker compose
STORAGES_FILE := docker_compose/storages.yaml
APP_FILE := docker_compose/backend.yaml
REDIS_FILE := docker_compose/redis.yaml
ENV_FILE = --env-file .env
LOGS = docker logs

DB_CONTAINER := postgres
APP_CONTAINER := backend
DB_USER := jewelry_user 
DB_NAME := jewelry_db

EXEC = docker exec -it
MANAGE_PY = python manage.py

.PHONY: storage
storage:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: storage-down
storage-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storage-logs
storage-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: postgres
postgres:
	${DC} -f ${STORAGES_FILE} exec ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME}

.PHONY: app
app:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${REDIS_FILE} ${ENV_FILE} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${REDIS_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: migrate
migrate:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: makemigrations
makemigrations:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec ${APP_CONTAINER} ${MANAGE_PY} collectstatic

.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} pytest