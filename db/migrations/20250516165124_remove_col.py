from db.migration_manager import Migration

class RemoveCol(Migration):
    id = 20250516165124

    def sql(self):
        return """
                delete user where discord_id = 337401441813528586;
            """
