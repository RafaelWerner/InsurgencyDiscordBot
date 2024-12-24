from db.migration_manager import Migration

class CreateTaskTable(Migration):
    id = 20241224130011

    def sql(self):
        return """
            CREATE TABLE task (
                id       INTEGER      PRIMARY KEY ASC AUTOINCREMENT
                                    NOT NULL,
                kind     VARCHAR (64) NOT NULL,
                interval BIGINT       NOT NULL
                                    DEFAULT (600),
                data     TEXT         NOT NULL
                                    DEFAULT ('{}')
            );
            """
