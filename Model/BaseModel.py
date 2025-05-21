from peewee import Model, SqliteDatabase
import os

db = 'Model/DB/database.db'
os.makedirs(os.path.dirname(db), exist_ok=True)
db = SqliteDatabase(db)

class BaseModel(Model):
    class Meta:
        database = db