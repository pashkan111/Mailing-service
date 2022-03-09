PYTHON := /usr/bin/env python
APP_DIR := ./
APP_NAME := databases


run: build:
	docker-compose up -d --build

test: build
	docker-compose run --rm -- web python manage.py test