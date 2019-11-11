#!/bin/bash
PID=$(lsof -t -i:8000)
if [ -n "${PID}" ]; then
  kill -9 $PID
fi
python manage.py runserver localhost:8000
