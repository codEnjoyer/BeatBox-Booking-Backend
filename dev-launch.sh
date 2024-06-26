#!/usr/bin/env bash

cd app || exit
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port "$APP_PORT"