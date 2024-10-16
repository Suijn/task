if [ "$1" = "server" ]; then
  echo Runnig server

  # Gunicorn must see the project on the PYTHONPATH.
  # manage.py sets the PYTHONPATH: https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/
  # therefore:
  /app/.venv/bin/poetry run gunicorn -b 0.0.0.0:8000 --workers 3 task.wsgi
else [ "$1" = "integration_test" ];
  echo Runnig integration_tests
  .venv/bin/poetry run python manage.py test
fi