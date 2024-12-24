#!/bin/sh

mkdir -p /app/logs
LOG_FILE=/app/logs/$(date +%Y-%m-%d_%H-%M-%S).log

python main.py > $LOG_FILE 2>&1
