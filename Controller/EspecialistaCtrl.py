from Model.Especialista import Especialista
from Model.DataBase import ConnectDataBase

class EspecialistaController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createEspecialista(self, nome: str, crm: int, email: str, senha: str):
        try:
            if Especialista.select().where(Especialista.crm == crm).exists():
                raise ValueError("CRM já cadastrado")
                
            if Especialista.select().where(Especialista.email == email).exists():
                raise ValueError("Email já cadastrado")
                
            novo_especialista = Especialista.create(
                nome=nome,
                crm=crm,
                email=email,
                senha=senha
            )
            return novo_especialista
        except Exception as e:
            raise e

    def readEspecialista(self, idEspecialista: int):
        try:
            return Especialista.get_by_id(idEspecialista)
        except Especialista.DoesNotExist:
            return None
        except Exception as e:
            raise e

    def listEspecialista(self):
        try:
            return list(Especialista.select())
        except Exception as e:
            raise e

    def updateEspecialista(self, idEspecialista: int, novoNome: str = None, novoCrm: int = None, novoEmail: str = None, novaSenha: str = None):
        try:
            especialista = Especialista.get_or_none(Especialista.id == idEspecialista)
            if not especialista:
                return None

            if novoNome is not None:
                especialista.nome = novoNome
            if novoCrm is not None:
                if Especialista.select().where(
                    (Especialista.crm == novoCrm) & 
                    (Especialista.id != idEspecialista)
                ).exists():
                    raise ValueError("CRM já está em uso por outro especialista")
                especialista.crm = novoCrm
            if novoEmail is not None:
                if Especialista.select().where(
                    (Especialista.email == novoEmail) & 
                    (Especialista.id != idEspecialista)
                ).exists():
                    raise ValueError("Email já está em uso por outro especialista")
                especialista.email = novoEmail
            if novaSenha is not None:
                especialista.senha = generate_password_hash(novaSenha)

            especialista.save()
            return especialista

        except Exception as e:
            raise e

    def deleteEspecialista(self, idEspecialista: int):
        try:
            especialista = Especialista.get_or_none(Especialista.id == idEspecialista)
            if not especialista:
                return False
                
            especialista.delete_instance()
            return True
            
        except Exception as e:
            raise e