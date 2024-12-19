from app.model.base import BaseModel, FieldTypes

class Task(BaseModel):
    TABLE = 'task'
    PRIMARY_KEY = 'id'
    FIELDS = {
        'id': FieldTypes.INTEGER,
        'kind': FieldTypes.TEXT,
        'interval': FieldTypes.INTEGER,
        'data': FieldTypes.TEXT
    }
