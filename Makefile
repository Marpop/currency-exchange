DJANGO_CONTAINER_NAME=django
COMPOSE_RUN=docker-compose run --rm $(DJANGO_CONTAINER_NAME)
MANAGE_RUN=docker-compose run --rm $(DJANGO_CONTAINER_NAME) python manage.py

test:
	$(COMPOSE_RUN) pytest

format:
	$(COMPOSE_RUN) black . && $(COMPOSE_RUN)  isort --atomic .

flake:
	$(COMPOSE_RUN) flake8 .

mypy:
	$(COMPOSE_RUN) mypy .

pylint:
	$(COMPOSE_RUN) pylint config/ apps/

lint: flake mypy pylint

manage:
	$(MANAGE_RUN) $(filter-out $@,$(MAKECMDGOALS))

%: # Ignore unknown commands and extra params
	@:
