# Use a imagem base com Python 3.11
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from db.migration_manager import MigrationManager; MigrationManager('database.db', 'db/migrations/').migrate()" > migration.log 2>&1

CMD ["python", "main.py"]
