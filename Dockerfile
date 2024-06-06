# Используем официальный образ Python
FROM python:3.12.3-slim-bullseye

# Устанавливем рабочую директорию в /backend-app
WORKDIR /backend-app

# Копируем файлы проекта ПЕРЕД установкой зависимостей
COPY . /backend-app

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false --local

# Обновляем файл poetry.lock и устанавливаем зависимости
RUN poetry lock --no-update
RUN poetry install --only main

# Выполняем миграции Alembic и запускаем скрипт
CMD alembic upgrade head && python startup.py
