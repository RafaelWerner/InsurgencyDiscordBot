from db.migration_manager import Migration

class UpdateMauricioPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198086224734' where discord_id = 629333974392766484;
            """
