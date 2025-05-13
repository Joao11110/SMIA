from peewee import Model, SqliteDatabase

db = SqliteDatabase('Model/DB/database.db')

class BaseModel(Model):
    class Meta:
        database = db