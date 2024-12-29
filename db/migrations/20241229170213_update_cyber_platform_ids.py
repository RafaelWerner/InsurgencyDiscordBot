from db.migration_manager import Migration

class UpdateCyberPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198169892135' where discord_id = 1288253339372355614;
            """
