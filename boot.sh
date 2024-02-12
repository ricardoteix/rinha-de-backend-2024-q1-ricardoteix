#!/bin/sh

# exec gunicorn -b :"$API_PORT" --timeout 60 --workers=2 --access-logfile - --error-logfile - app:app;

uvicorn app:app --port "$API_PORT" --reload
