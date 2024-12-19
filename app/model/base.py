from enum import Enum

from app.singleton.database import SingletonDatabase

class FieldTypes(Enum):
    INTEGER = 'int'
    TEXT = 'text'
    DATETIME = 'datetime'

class Struct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class BaseModel:
    TABLE = ''
    PRIMARY_KEY = ''
    FIELDS = {}

    def __init__(self):
        self.conn = SingletonDatabase().get()

    def _build_query(self, fields = []):
        if not fields:
            fields = ['*']

        return f"SELECT {', '.join(fields)} FROM {self.TABLE}"

    def _build_filtered_query(self, fields = [], filters = ''):
        return f"{self._build_query(fields)} WHERE {filters}"

    def _catch(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur

    def _execute(self, query):
        cur = self.conn.cursor()
        try:
            cur.execute(query)
            self.conn.commit()
        finally:
            cur.close()

    def _prepare_value_with_type(self, field, value):
        if field not in self.FIELDS:
            raise ValueError(f"Field '{field}' not allowed")

        field_type = self.FIELDS[field]

        if field_type == FieldTypes.INTEGER:
            return str(value)
        elif field_type == FieldTypes.TEXT or field_type == FieldTypes.DATETIME:
            return f"'{str(value)}'"
        else:
            raise ValueError(f"Field type '{field_type}' not allowed")

    def _parse_all_records(self, query):
        results = []
        cur = self._catch(query)
        try:
            for row in cur.fetchall():
                results.append(Struct(**dict(zip(self.FIELDS.keys(), row))))

            if len(results) == 0:
                return None

            return results
        finally:
            cur.close()

    def count(self, filters = ''):
        query = self._build_filtered_query(['COUNT(*)'], filters)

        cur = self._catch(query)
        try:
            value = cur.fetchone()[0]
        finally:
            cur.close()

        return value

    def all(self):
        return self._parse_all_records(self._build_query())

    def find_by(self, field_and_value):
        filter = ' and '.join([f"{field} = {self._prepare_value_with_type(field, value)}" for field, value in field_and_value.items()])
        query = self._build_filtered_query(filters = filter)

        return self._parse_all_records(query)

    def find_by_id(self, value):
        results = self.find_by(self.PRIMARY_KEY, value)

        if len(results) == 0:
            raise ValueError(f"Record with {self.PRIMARY_KEY} = {value} not found")

        if len(results) > 1:
            raise ValueError(f"Multiple records with {self.PRIMARY_KEY} = {value} found")

        return results[0]

    def create(self, data = {}):
        if not data:
            raise ValueError("You can't create records without data")

        values = []

        for field, value in data.items():
            values.append(self._prepare_value_with_type(field, value))

        query = f"INSERT INTO {self.TABLE} ({', '.join(data.keys())}) VALUES ({', '.join(values)})"
        self._execute(query)

    def update(self, data, filters):
        if not filters:
            raise ValueError("You can't update all records from table")

        if not data:
            raise ValueError("You can't update records without data")

        fields = ', '.join([f"{field} = {self._prepare_value_with_type(field, value)}" for field, value in data.items()])
        query = f"UPDATE {self.TABLE} SET {fields} WHERE {filters}"
        self._execute(query)

    def delete(self, filters):
        if not filters:
            raise ValueError("You can't delete all records from table")

        query = f"DELETE FROM {self.TABLE} WHERE {filters}"
        self._execute(query)
