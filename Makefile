SHELL := /bin/bash
FILES=$(shell docker ps -a -q --filter "name=airflow*")

# Verifica versao do docker compose.
COMPOSE_COMMAND=$(shell command -v docker-compose >/dev/null 2>&1 && echo "docker-compose" || echo "docker compose")


build:
	docker build -t airflow:2.9.1 .

init: build
	$(COMPOSE_COMMAND) up airflow-init

up: build
	$(COMPOSE_COMMAND) up

make down:
	$(COMPOSE_COMMAND) down

bash:
	docker exec -ti airflow-webserver bash 
