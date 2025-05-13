from peewee import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
)

from Model.BaseModel import BaseModel

class Especialista(BaseModel):
    nome = CharField(null=False)
    crm = IntegerField(null=False)
    email = CharField(null=False)
    senha = CharField(null=False)

class Paciente(BaseModel):
    nome = CharField(null=False)
    cpf = IntegerField(null=False)
    email = CharField(null=False)
    data_nascimento = DateField(null=False)
    peso = FloatField(null=False)
    altura = FloatField(null=False)
    especialista = ForeignKeyField(Especialista, backref='pacientes', null=False)

class Medicamento(BaseModel):
    nome = CharField()
    intervalo = CharField() # Formato 'HH:MM'
    quantidade = FloatField(default=0)
    data_inicio = DateTimeField(null=True) # Formato 'YYYY-MM-DD HH:MM:SS'
    data_fim = DateTimeField(null=True)
    paciente = ForeignKeyField(Paciente, backref='medicamentos')
    especialista = ForeignKeyField(Especialista, backref='medicamentos')

class Lembrete(BaseModel):
    data_hora = DateTimeField() # Formato 'YYYY-MM-DD HH:MM:SS'
    status = BooleanField(default=False)
    medicamento = ForeignKeyField(Medicamento, backref='lembretes')
    paciente = ForeignKeyField(Paciente, backref='lembretes')

db.connect()
db.create_tables([Especialista, Paciente, Medicamento, Lembrete])