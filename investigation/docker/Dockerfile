FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml

RUN poetry config virtualenvs.create false \
    && poetry install --no-cache --no-root

COPY ./Makefile ./Makefile

COPY ./src ./

ENTRYPOINT ["make", "run_with_uvicorn"]