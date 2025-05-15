from Model.Paciente import Paciente
from Model.DataBase import ConnectDataBase

class PacienteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createPaciente(self, nome: str, cpf: int, email: str, data_nascimento: str, peso: float, altura: float, especialista: int):
        try:
            Paciente.create(nome=nome, cpf=cpf, email=email, data_nascimento=data_nascimento, peso=peso, altura=altura, especialista=especialista)
        except Exception as e:
            return e

    def readPaciente(self, idPaciente: int):
        try:
            comando = "select * from paciente where id == ?"
            return self.selectById(comando, idPaciente)
        except Exception as e:
            return e

    def listPaciente(self):
        try:
            comando = "select * from paciente"
            return self.selectAll(comando)
        except Exception as e:
            return e

    def updatePaciente(self, idPaciente: int, novoNome: str, novoCpf: int, novoEmail: str, novaData_nascimento: str, novoPeso: float, novaAltura: float, novoEspecialista: int):
        try:
            p = Paciente.get(Paciente.id == idPaciente)
            p.nome = novoNome
            p.cpf = novoCpf
            p.email = novoEmail
            p.data_nascimento = novaData_nascimento
            p.peso = novoPeso
            p.altura = novaAltura
            p.especialista = novoEspecialista
        except Exception as e:
            return e

    def deletePaciente(self, idPaciente: int):
        try:
            Paciente.delete_by_id(Paciente.id==idPaciente)
        except Exception as e:
            return e