from db.migration_manager import Migration

class UpdateKelpexPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198071524069' where discord_id = 337401441813528586;
            """
