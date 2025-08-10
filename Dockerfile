# STAGE 1: Builder image, used to build the virtual environment

FROM python:3.13.2-bookworm as builder

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./
RUN touch README.md

RUN poetry install --no-interaction --no-root && rm -rf $POETRY_CACHE_DIR

##########################################################################

# STAGE 2: Runtime image, used to run the code in the virtual environment

FROM python:3.13.2-slim-bookworm as runtime

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY src ./src

ENTRYPOINT uvicorn src.api:api --host 0.0.0.0 --port ${PORT}