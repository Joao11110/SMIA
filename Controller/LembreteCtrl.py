from Model.Lembrete import Lembrete
from Model.DataBase import ConnectDataBase


class LembreteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createLembrete(
        self, data_hora: str, status: int, medicamento: int, paciente: int
    ):
        try:
            lembrete = Lembrete.create(
                data_hora=data_hora,
                status=status,
                medicamento=medicamento,
                paciente=paciente,
            )
            return lembrete
        except Exception as e:
            raise e

    def readLembrete(self, idLembrete: int):
        try:
            return Lembrete.get(Lembrete.id == idLembrete)
        except Lembrete.DoesNotExist:
            return None
        except Exception as e:
            raise e

    def listLembrete(self):
        try:
            return list(Lembrete.select())
        except Exception as e:
            raise e

    def updateLembrete(
        self,
        idLembrete: int,
        novaData_hora: str = None,
        NovoStatus: bool = None,  # Alterado de int para bool
        NovoMedicamento: int = None,
        NovoPaciente: int = None,
    ):
        try:
            lembrete = Lembrete.get(Lembrete.id == idLembrete)
            
            if novaData_hora:
                lembrete.data_hora = novaData_hora
            if NovoStatus is not None:
                lembrete.status = NovoStatus
            if NovoMedicamento:
                lembrete.medicamento = NovoMedicamento
            if NovoPaciente:
                lembrete.paciente = NovoPaciente
                
            lembrete.save()
            return lembrete
        except Lembrete.DoesNotExist:
            return None
        except Exception as e:
            raise e

    def deleteLembrete(self, idLembrete: int):
        try:
            return Lembrete.delete_by_id(idLembrete) > 0
        except Exception as e:
            raise e