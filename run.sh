if [ "$1" = "server" ]; then
  echo Runnig server
  sleep 111111111111
else [ "$1" = "integration_test" ];
  echo Runnig integration_tests
  .venv/bin/poetry run python manage.py test
fi