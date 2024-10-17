.PHONY: server integration_tests down down_vol style reformat admin

# Variables used by the `admin` command.
# Note: they are very tied with the variables defined in Docker Compose.
IMG = task_temporary_name
CONTAINER_NAME = task_temporary_container
POSTGRES_CONTAINER_NAME = temp_db
POSTGRES_DB = prefixes_dev
NETWORK = temporary_network
VOLUME = dbvolume
PGDATA = /dbvolume

server:
	docker volume create ${VOLUME}
	docker compose up --build server

integration_tests:
	docker volume create ${VOLUME}
	docker compose up --build integration_tests

down:
	docker compose down -v

down_vol:
	docker volume rm ${VOLUME}

style:
	black --check .
	isort --check .
	flake8 .

reformat:
	black .
	isort .


admin:
	# setup
	docker volume create ${VOLUME}
	docker network create --driver=bridge --attachable ${NETWORK}
	docker run --name ${POSTGRES_CONTAINER_NAME} -e POSTGRES_PASSWORD=very_secret -e POSTGRES_DB=${POSTGRES_DB} -e PGDATA=${PGDATA} --network ${NETWORK} -v ${VOLUME}:/${VOLUME} -d postgres:17

	docker build -t ${IMG} . --no-cache
	docker run --network ${NETWORK} -v ${VOLUME}:/${VOLUME} -d --name ${CONTAINER_NAME} ${IMG} server

	# commit migrations to the DB
	docker exec -e POSTGRES_HOST=${POSTGRES_CONTAINER_NAME} ${CONTAINER_NAME} bash -c ".venv/bin/poetry run python manage.py migrate"

	# create admin
	docker exec -e POSTGRES_HOST=${POSTGRES_CONTAINER_NAME} -e DJANGO_SUPERUSER_PASSWORD=admin ${CONTAINER_NAME} bash -c ".venv/bin/poetry run python manage.py createsuperuser --noinput --username admin --email admin@admin.com"

	# teardown
	# do not remove the $VOLUME. Docker compose uses it.
	docker container rm -f ${CONTAINER_NAME}
	docker container rm -f ${POSTGRES_CONTAINER_NAME}
	docker image rm -f ${IMG}
	docker network rm ${NETWORK}
