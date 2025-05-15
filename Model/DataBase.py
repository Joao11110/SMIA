from Model.Especialista import Especialista
from Model.Lembrete import Lembrete
from Model.Medicamento import Medicamento
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

    def selectById(self, comando, idEspecifico):
        con = sqlite3.connect("Model/DB/database.db")
        cursor = con.cursor()
        cursor.execute(comando, (idEspecifico,))
        line = cursor.fetchone()
        return line

    def selectAll(self, comando):
        con = sqlite3.connect("Model/DB/database.db")
        cursor = con.cursor()
        cursor.execute(comando)
        lines = cursor.fetchall()
        return lines