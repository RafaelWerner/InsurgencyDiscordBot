from db.migration_manager import Migration

class UpdateBiuzeraPlatformIds(Migration):
    id = 20241229170211

    def sql(self):
        return """
                UPDATE user set plataform_id = 'SteamNWI:76561198272396684' where discord_id = 640322720021741636;
            """
