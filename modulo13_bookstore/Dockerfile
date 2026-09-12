FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.4

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

COPY pyproject.toml ./
RUN poetry install --no-root --without dev --no-interaction

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
