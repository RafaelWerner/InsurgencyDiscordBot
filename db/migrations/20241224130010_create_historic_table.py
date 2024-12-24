from db.migration_manager import Migration

class CreateHistoricTable(Migration):
    id = 20241224130010

    def execute(self, connection):
        connection.execute(
            """
            CREATE TABLE historic (
                created_at   DATETIME      NOT NULL
                                        DEFAULT ( (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') ) ),
                player       VARCHAR (180) NOT NULL,
                plataform_id VARCHAR (80),
                score        INTEGER       NOT NULL
                                        DEFAULT (0)
            );
            """
        )
