from Model.Paciente import Paciente
from Model.DataBase import ConnectDataBase


class PacienteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createPaciente(
        self,
        nome: str,
        cpf: int,
        email: str,
        data_nascimento: str,
        peso: float,
        altura: float,
        especialista: int,
    ):
        try:
            paciente = Paciente.create(
            nome=nome,
            cpf=cpf,
            email=email,
            data_nascimento=data_nascimento,
            peso=peso,
            altura=altura,
            especialista=especialista
        )
            return paciente
        except Exception as e:
            print(f"Erro ao criar paciente: {str(e)}")
        raise ValueError(f"Erro ao criar paciente: {str(e)}")

    def readPaciente(self, idPaciente: int):
        try:
            paciente = Paciente.get_by_id(idPaciente)
            return paciente
        except Paciente.DoesNotExist:
            return None
        except Exception as e:
            print(f"Erro ao buscar paciente: {str(e)}")
        raise

    def listPaciente(self):
        try:
            return list(Paciente.select())
        except Exception as e:
            print(f"Erro ao listar pacientes: {str(e)}")
        raise e

    def updatePaciente(self, idPaciente: int, novoNome: str, novoCpf: int, novoEmail: str,
                  novaData_nascimento: str, novoPeso: float, novaAltura: float, novoEspecialista: int):
        try:
            paciente = Paciente.get_by_id(idPaciente)
            paciente.nome = novoNome or paciente.nome
            paciente.cpf = novoCpf or paciente.cpf
            paciente.email = novoEmail or paciente.email
            paciente.data_nascimento = novaData_nascimento or paciente.data_nascimento
            paciente.peso = novoPeso or paciente.peso
            paciente.altura = novaAltura or paciente.altura
            paciente.especialista = novoEspecialista or paciente.especialista
            paciente.save()
            return paciente
        except Paciente.DoesNotExist:
            return None
        except Exception as e:
            print(f"Erro ao atualizar paciente: {str(e)}")
            return None

    def deletePaciente(self, idPaciente: int):
        try:
            paciente = Paciente.get_by_id(idPaciente)
            paciente.delete_instance()
            return True
        except Paciente.DoesNotExist:
            return False
        except Exception as e:
            print(f"Erro ao deletar paciente: {str(e)}")
            return False