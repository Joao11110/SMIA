from Model.Medicamento import Medicamento
from Model.DataBase import ConnectDataBase


class MedicamentoController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createMedicamento(
        self,
        nome: str,
        intervalo: str,
        quantidade: float,
        data_inicio: str,
        data_fim: str,
        paciente: int,
        especialista: int,
    ):
        try:
            Medicamento.create(
                nome=nome,
                intervalo=intervalo,
                quantidade=quantidade,
                data_inicio=data_inicio,
                data_fim=data_fim,
                paciente=paciente,
                especialista=especialista,
            )
        except Exception as e:
            return e

    def readMedicamento(self, idMedicamento: int):
        try:
            comando = "select * from medicamento where id == ?"
            return self.selectById(comando, idMedicamento)
        except Exception as e:
            return e

    def listMedicamento(self):
        try:
            comando = "select * from medicamento"
            return self.selectAll(comando)
        except Exception as e:
            return e

    def updateMedicamento(
        self,
        idMedicamento: int,
        novoNome: str,
        novoIntervalo: str,
        novaQuantidade: float,
        novaData_inicio: str,
        novaData_fim: str,
        novoPaciente: int,
        novoEspecialista: int,
    ):
        try:
            m = Medicamento.get(Medicamento.id == idMedicamento)
            m.nome = novoNome
            m.intervalo = novoIntervalo
            m.quantidade = novaQuantidade
            m.data_inicio = novaData_inicio
            m.data_fim = novaData_fim
            m.paciente = novoPaciente
            m.especialista = novoEspecialista
            m.save()
        except Exception as e:
            return e

    def deleteMedicamento(self, idMedicamento: int):
        try:
            Medicamento.delete_by_id(Medicamento.id == idMedicamento)
        except Exception as e:
            return e
