# currency exchange

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### Prerequisites

- Docker
- docker-compose

## Basic Commands

### Run Tests

     make test

### Run type checks and linters (flake8 and pylint)

     make lint

### To access admin panel create admin user

     make manage createsuperuser

### Running locally

     docker-compose up

- API: http://0.0.0.0:8000/api/
- API docs: http://0.0.0.0:8000/api/docs/
- API schema: http://0.0.0.0:8000/api/schema/
- Admin: http://0.0.0.0:8000/admin/
