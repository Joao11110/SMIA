from Model.Especialista import Especialista
from Model.Medicamento import Medicamento
from Model.Lembrete import Lembrete
from Model.Paciente import Paciente
from Model.BaseModel import db
import sqlite3

class ConnectDataBase:
    def __init__(self):
        self.connectDB()

    def connectDB(self):
        try:
            db.connect()
            db.create_tables([Especialista, Paciente, Medicamento, Lembrete])
        except Exception as e:
            return e