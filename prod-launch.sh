#!/usr/bin/env bash

cd app || exit
alembic upgrade head
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:"$APP_PORT" --timeout 300