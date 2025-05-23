from Model.BaseModel import BaseModel
from Model.Especialista import Especialista
from Model.Paciente import Paciente

from peewee import (
    CharField,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    PrimaryKeyField,
)

class Medicamento(BaseModel):
    id = PrimaryKeyField(null=False)
    nome = CharField()
    intervalo = DateField() # Formato 'HH:MM'
    quantidade = FloatField(default=0)
    data_inicio = DateTimeField(null=True) # Formato 'YYYY-MM-DD HH:MM:SS'
    data_fim = DateTimeField(null=True) # Formato 'YYYY-MM-DD HH:MM:SS'
    paciente = ForeignKeyField(Paciente, backref='medicamentos')
    especialista = ForeignKeyField(Especialista, backref='medicamentos')