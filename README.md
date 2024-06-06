### Python version 3.12.2

## Запуск приложения

1. Создайте .env файл в корневой директории с переменными из test.env
2. Измените поля со значением changeme и установите корректные значения для
   подключения к БД
3. Локальный запуск:
    1. Установите миграции (команды приведены ниже)
    2. Запустите скрипт
    ```bash
    python startup.py
    ```

4. Запуск в Docker-контейнере:

```bash
docker compose up --build
```

## Установка и обновление зависимостей

```bash
poetry install --with dev,test
poetry update --with dev
poetry add <packagename> --group dev
poetry remove <packagename> --group test
```

## Форматирование кода

```bash
black ./app
black --check . --diff
```

## Запуск тестов

```bash
pytest -v
```

## Миграции БД

```bash
alembic upgrade head
```
