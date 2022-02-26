PYTHON := /usr/bin/env python
APP_DIR := ./


run:
        python manage.py runserver

migrate:
        python manage.py migrate

makemigr:
        python manage.py makemigrations
