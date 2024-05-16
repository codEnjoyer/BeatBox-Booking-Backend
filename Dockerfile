# Используем официальный образ Python
FROM python:3.12.3-slim-bullseye

# Устанавливем рабочую директорию в /backend-app
WORKDIR /backend-app

# Копируем весь текущий каталог в рабочую директорию
COPY .. /backend-app

# Устанавливаем переменные среды, которые:
# 1. Поедотвращает создагние .pyc файлов (байт-код), для избежания ненужного рассхода места
# 2. Отключает буферизацию стандартного вывода и ввода/вывода ошибок, используют в докере для быстрого вывода
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false --local

# Обновляем файл poetry.lock без обновления зависимостей и устанавливаем их через poetry
RUN poetry lock --no-update
RUN poetry install --only main

# Открываем порт 8000 для приложения
EXPOSE 8000

# Базовая строка запуска приложения (переопределяется в docker-compose.yml)
CMD alembic upgrade head && python startup.py
