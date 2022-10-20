FROM python:3.10.6

# Envs
ENV PYTHONPATH /app/src/
ENV PATH /app/src/:$PATH
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.0

# change workdir
WORKDIR /app

# install poetry
RUN pip3 install --no-cache-dir "poetry==$POETRY_VERSION"

# install packages
RUN poetry config virtualenvs.create false
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml
RUN poetry install

COPY . /app

