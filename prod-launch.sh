#!/usr/bin/env bash

alembic upgrade head
cd app || exit
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:"$APP_PORT" --timeout 300