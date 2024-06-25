#!/usr/bin/env bash

alembic upgrade head
cd app || exit
uvicorn main:app --host 0.0.0.0 --port "$APP_PORT"