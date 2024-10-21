FROM python:3.12 as system
WORKDIR "app"

ENV PYTHONUNBUFFERED = 1
ENV USER=app_user
ENV GROUP=regular_users
ENV VENV_PATH=.venv

RUN groupadd $GROUP \
 && adduser $USER \
 && usermod -aG $GROUP $USER

FROM system AS setup_poetry
# for instructions check: https://python-poetry.org/docs/#installing-manually
RUN python3 -m venv $VENV_PATH \
 && $VENV_PATH/bin/pip install -U pip setuptools \
 && $VENV_PATH/bin/pip install poetry

FROM setup_poetry AS base
COPY --chown=$USER:$GROUP pyproject.toml pyproject.toml
COPY --chown=$USER:$GROUP poetry.lock poetry.lock
COPY --chown=$USER:$GROUP task task
COPY --chown=$USER:$GROUP run.sh run.sh
COPY --chown=$USER:$GROUP manage.py manage.py
COPY --chown=$USER:$GROUP data data

FROM base AS build_dependencies
RUN $VENV_PATH/bin/poetry install --no-cache

FROM build_dependencies as set_user
USER $USER

FROM set_user as run
RUN chmod +x run.sh
ENTRYPOINT ["bash", "/app/run.sh"]