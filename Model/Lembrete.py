from Model.BaseModel import BaseModel
from Model.Medicamento import Medicamento
from Model.Paciente import Paciente

from peewee import (
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    PrimaryKeyField,
)

class Lembrete(BaseModel):
    id = PrimaryKeyField(null=False)
    data_hora = DateTimeField() # Formato 'YYYY-MM-DD HH:MM:SS'
    status = BooleanField(default=False)
    medicamento = ForeignKeyField(Medicamento, backref='lembretes')
    paciente = ForeignKeyField(Paciente, backref='lembretes')