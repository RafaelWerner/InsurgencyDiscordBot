import sqlite3
import os
import importlib.util

class Migration:
    id = None

    def sql(self):
        raise NotImplementedError()

class MigrationManager:
    def __init__(self, db_path, migrations_folder):
        self.db_path = db_path
        self.migrations_folder = migrations_folder
        self.conn = sqlite3.connect(db_path)
        self._ensure_migrations_table_exists()
        self._load_applied_migrations()

    def _ensure_migrations_table_exists(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS migrations (id BIGINT PRIMARY KEY);")
        finally:
            cursor.close()

        self.conn.commit()

    def _load_applied_migrations(self):
        cursor = self.conn.cursor()
        try:
            rows = cursor.execute("SELECT id FROM migrations order by id desc;").fetchall()
        finally:
            cursor.close()

        self.applied_migrations = {row[0] for row in rows}

    def _load_migration(self, file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, Migration) and cls is not Migration:
                return cls()

        raise ValueError(f"Migration class not found in {file_path}")

    def _insert_applied_migration(self, timestamp):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO migrations (id) VALUES (?);", (timestamp,))
        finally:
            cursor.close()

    def _apply_migration(self, migration_file):
        timestamp = int(os.path.splitext(migration_file)[0].split('_')[0])

        if timestamp in self.applied_migrations:
            return

        file_path = os.path.join(self.migrations_folder, migration_file)
        migration = self._load_migration(file_path)
        print(f"Applying migration {timestamp}")

        cursor = self.conn.cursor()
        try:
            cursor.execute(migration.sql())
        finally:
            cursor.close()

        self._insert_applied_migration(timestamp)

    def migrate(self):
        migrations_files = sorted([f for f in os.listdir(self.migrations_folder) if f.endswith('.py')])

        for migration_file in migrations_files:
            self._apply_migration(migration_file)

        self.conn.commit()
        print("All migrations applied")
