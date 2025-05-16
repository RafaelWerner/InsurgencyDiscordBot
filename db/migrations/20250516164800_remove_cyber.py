from db.migration_manager import Migration

class RemoveCyber(Migration):
    id = 20250516164800

    def sql(self):
        return """
                delete user where discord_id = 1288253339372355614;
            """
