### Python version 3.12.2

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
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head 
alembic downgrade -1
```
