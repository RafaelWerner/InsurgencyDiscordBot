from app.model.base import BaseModel, FieldTypes

class User(BaseModel):
    TABLE = 'user'
    PRIMARY_KEY = 'discord_id'
    FIELDS = {
        'discord_id': FieldTypes.INTEGER,
        'plataform_id': FieldTypes.TEXT,
        'name': FieldTypes.TEXT,
        'role': FieldTypes.TEXT,
        'created_at': FieldTypes.DATETIME,
        'created_by': FieldTypes.INTEGER
    }
