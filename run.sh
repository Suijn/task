#!/bin/bash

if [ "$1" = "server" ]; then
  echo Running server

  # Gunicorn must see the project on the PYTHONPATH.
  # manage.py sets the PYTHONPATH: https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/
  # therefore:
  /app/.venv/bin/poetry run python manage.py migrate
  /app/.venv/bin/poetry run gunicorn -b 0.0.0.0:8000 --workers 3 task.wsgi
elif [ "$1" = "demo" ]; then
  echo Running demo

  /app/.venv/bin/poetry run python manage.py migrate
  /app/.venv/bin/poetry run python manage.py runserver 0.0.0.0:8000
else [ "$1" = "integration_test" ];
  echo Runnig integration_tests
  .venv/bin/poetry run python manage.py test -v 1
fi