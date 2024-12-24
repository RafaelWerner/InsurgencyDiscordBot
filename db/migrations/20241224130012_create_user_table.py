from db.migration_manager import Migration

class CreateUserTable(Migration):
    id = 20241224130012

    def execute(self, connection):
        connection.execute(
            """
            CREATE TABLE user (
                discord_id   BIGINT        PRIMARY KEY
                                        NOT NULL
                                        UNIQUE,
                plataform_id VARCHAR (250) UNIQUE,
                name         VARCHAR (200) NOT NULL,
                role         VARCHAR (50)  NOT NULL
                                        DEFAULT ('jogador'),
                created_at   DATETIME      DEFAULT ( (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') ) )
                                        NOT NULL,
                created_by   BIGINT        NOT NULL
            );
            """
        )
