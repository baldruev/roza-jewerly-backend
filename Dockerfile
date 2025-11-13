# Multi-stage build для оптимизации
FROM python:3.11.11-slim AS builder

# Установка зависимостей сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем UV из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app
COPY requirements.txt /app/

# Используем cache mount для ускорения сборки
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r requirements.txt

# Production stage
FROM python:3.11.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем non-root пользователя
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

# Копируем установленные пакеты из builder stage
COPY --from=builder /usr/local /usr/local

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Копируем код приложения
COPY --chown=app:app . /app/

# Создаем необходимые директории
RUN mkdir -p /app/static /app/media && \
    chown -R app:app /app 

# Переключаемся на non-root пользователя
USER app

EXPOSE 8000