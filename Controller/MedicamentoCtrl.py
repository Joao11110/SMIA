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
            medicamento = Medicamento.create(
            nome=nome,
            intervalo=intervalo,
            quantidade=quantidade,
            data_inicio=data_inicio,
            data_fim=data_fim,
            paciente=paciente,
            especialista=especialista,
        )
            return medicamento
        except Exception as e:
            return None

    def listMedicamento(self):
        try:
            return list(Medicamento.select())  # Retorna uma lista de objetos Medicamento
        except Exception as e:
            return e

    def readMedicamento(self, idMedicamento: int):
        try:
            return Medicamento.get(Medicamento.id == idMedicamento)  # Retorna um objeto Medicamento
        except Medicamento.DoesNotExist:
            return None
        except Exception as e:
            return e
        
    def listMedicamentoPorPaciente(self, paciente_id: int):
        try:
            medicamentos = Medicamento.select().where(Medicamento.paciente == paciente_id)
            return [
                {
                    "id": med.id,
                    "nome": med.nome,
                    "intervalo": med.intervalo,
                    "quantidade": med.quantidade,
                    "data_inicio": med.data_inicio if isinstance(med.data_inicio, str) else (med.data_inicio.isoformat() if med.data_inicio else None),
                    "data_fim": med.data_fim if isinstance(med.data_fim, str) else (med.data_fim.isoformat() if med.data_fim else None),
                    "paciente": med.paciente.id,
                    "especialista": med.especialista.id
                }
                for med in medicamentos
            ]
        except Exception as e:
            print(f"Erro no controller: {e}")
            return []

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
