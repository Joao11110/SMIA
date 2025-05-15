from Model.Especialista import Especialista
from Model.DataBase import ConnectDataBase

class EspecialistaController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createEspecialista(self, nome: str, crm: int, email: str, senha: str):
        try:
            Especialista.create(nome=nome, crm=crm, email=email, senha=senha)
        except Exception as e:
            return e

    def readEspecialista(self, idEspecialista: int):
        try:
            comando = "select * from especialista where id == ?"
            return self.selectById(comando, idEspecialista)
        except Exception as e:
            return e

    def listEspecialista(self):
        try:
            comando = "select * from especialista"
            return self.selectAll(comando)
        except Exception as e:
            return e

    def updateEspecialista(self, idEspecialista: int, novoNome: str, novoCrm: int, novoEmail: str, novaSenha: str):
        try:
            e = Especialista.get(Especialista.id == idEspecialista)
            e.nome = novoNome
            e.crm = novoCrm
            e.email = novoEmail
            e.senha = novaSenha
            e.save()
        except Exception as e:
            return e

    def deleteEspecialista(self, idEspecialista: int):
        try:
            Especialista.delete_by_id(Especialista.id==idEspecialista)
        except Exception as e:
            return e