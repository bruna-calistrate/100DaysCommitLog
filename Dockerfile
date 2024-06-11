FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]