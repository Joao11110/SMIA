from Model.Lembrete import Lembrete
from Model.DataBase import ConnectDataBase


class LembreteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createLembrete(
        self, data_hora: str, status: int, medicamento: int, paciente: int
    ):
        try:
            Lembrete.create(
                data_hora=data_hora,
                status=status,
                medicamento=medicamento,
                paciente=paciente,
            )
        except Exception as e:
            return e

    def readLembrete(self, idLembrete: int):
        try:
            comando = "select * from lembrete where id == ?"
            return self.selectById(comando, idLembrete)
        except Exception as e:
            return e

    def listLembrete(self):
        try:
            comando = "select * from lembrete"
            return self.selectAll(comando)
        except Exception as e:
            return e

    def updateLembrete(
        self,
        idLembrete: int,
        novaData_hora: str,
        NovoStatus: int,
        NovoMedicamento: int,
        NovoPaciente: int,
    ):
        try:
            l = Lembrete.get(Lembrete.id == idLembrete)
            l.data_hora = novaData_hora
            l.status = NovoStatus
            l.medicamento = NovoMedicamento
            l.paciente = NovoPaciente
            l.save()
        except Exception as e:
            return e

    def deleteLembrete(self, idLembrete: int):
        try:
            Lembrete.delete_by_id(Lembrete.id == idLembrete)
        except Exception as e:
            return e
