from Model.BaseModel import BaseModel

from peewee import (
    CharField,
    IntegerField,
    PrimaryKeyField,
)

class Especialista(BaseModel):
    id = PrimaryKeyField(null=False)
    nome = CharField(null=False)
    crm = IntegerField(null=False)
    email = CharField(null=False)
    senha = CharField(null=False)
