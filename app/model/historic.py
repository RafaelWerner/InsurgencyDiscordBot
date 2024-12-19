from app.model.base import BaseModel, FieldTypes

class Historic(BaseModel):
    TABLE = 'historic'
    PRIMARY_KEY = 'created_at'
    FIELDS = {
        'created_at': FieldTypes.DATETIME,
        'player': FieldTypes.TEXT,
        'plataform_id': FieldTypes.TEXT,
        'score': FieldTypes.INTEGER
    }
