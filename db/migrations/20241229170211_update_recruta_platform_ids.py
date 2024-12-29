from db.migration_manager import Migration

class UpdateRecrutaPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198298642012' where discord_id = 1252787533503266837;
            """
