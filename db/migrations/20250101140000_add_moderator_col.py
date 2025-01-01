from db.migration_manager import Migration

class AddModeratorCol(Migration):
    id = 20241229170211

    def sql(self):
        return """
                INSERT INTO user (created_by, created_at, role, name, plataform_id, discord_id)
                VALUES (321719984839720960, '2025-01-01 14:03:52.012', 'moderator', 'Col', 'SteamNWI:76561199087549540', 337401441813528586);
            """

