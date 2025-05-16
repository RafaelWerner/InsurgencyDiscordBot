from db.migration_manager import Migration

class AddSantaAdmin(Migration):
    id = 20250516165242

    def sql(self):
        return """
                INSERT INTO user (created_by, created_at, role, name, plataform_id, discord_id)
                VALUES (321719984839720960, '2025-05-16 16:52:52.012', 'admin', 'santamorte® +Đi1ØØØ', 'SteamNWI:76561198118365524', 287641609078833153);
            """