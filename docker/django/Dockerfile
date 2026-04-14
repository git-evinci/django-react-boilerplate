# docker/django/Dockerfile
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.3.4 \
    POETRY_VIRTUALENVS_CREATE=false
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install system dependencies (needed for certain Python packages like psycopg2 or cffi)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/
RUN cat /app/pyproject.toml
# Install dependencies (ignoring the virtualenv creation since we are in a container)
RUN poetry lock
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy the Django project
COPY ./backend /app/backend
COPY ./scripts /app/scripts

# Expose port
EXPOSE 8000

# The default command will be overridden by docker-compose, but we add a fallback
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]