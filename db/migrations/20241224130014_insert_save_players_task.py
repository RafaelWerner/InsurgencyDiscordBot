from db.migration_manager import Migration

class InsertSavePlayersTask(Migration):
    id = 20241224130014

    def execute(self, connection):
        connection.execute("INSERT INTO task (data, interval, kind, id) VALUES ('{}', 600, 'save_players', 2);")
