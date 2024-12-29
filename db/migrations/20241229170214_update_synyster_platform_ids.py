from db.migration_manager import Migration

class UpdateSynysterPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198878308868' where discord_id = 424262828057427981;
            """
