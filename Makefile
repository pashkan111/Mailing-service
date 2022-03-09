# -*- coding: utf-8 -*-

PYTHON := /usr/bin/env python
APP_DIR := ./
APP_NAME := databases


run:
	docker-compose up -d --build

test:
	docker-compose run --rm -- web python manage.py test