# Use a imagem base com Python 3.11
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from db.migration_manager import MigrationManager; MigrationManager('database.db', 'db/migrations/').migrate()"

CMD ["sh", "-c", "mkdir -p /app/logs && python main.py > /app/logs/$(date +%Y-%m-%d_%H-%M-%S).log 2>&1"]
