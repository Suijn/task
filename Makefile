.PHONY: server integration_tests down style reformat

server:
	docker compose up --build server

integration_tests:
	docker compose up --build integration_tests

down:
	docker compose down -v

style:
	black --check .
	isort --check .
	flake8 .

reformat:
	black .
	isort .