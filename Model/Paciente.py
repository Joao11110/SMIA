from Model.BaseModel import BaseModel
from Model.Especialista import Especialista

from peewee import (
    CharField,
    DateField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    PrimaryKeyField,
)


class Paciente(BaseModel):
    id = PrimaryKeyField(null=False)
    nome = CharField(null=False)
    cpf = IntegerField(null=False)
    email = CharField(null=False)
    data_nascimento = DateField(null=False)
    peso = FloatField(null=False)
    altura = FloatField(null=False)
    especialista = ForeignKeyField(Especialista, backref="pacientes", null=False)
