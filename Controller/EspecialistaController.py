from Model.Especialista import Especialista
from Model.DataBase import ConnectDataBase
from flask import jsonify

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

    def getEspecialista(self, idEspecialista: int):
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
                return {'error': 'Especialista não encontrado'}, 404

            updates = {}
            if novoNome != None:
                novoNome = novoNome.strip()
                if len(novoNome) < 3:
                    return {'error': 'Nome deve ter pelo menos 3 caracteres'}, 400
                updates['nome'] = novoNome

            if novoCrm != None:
                if len(str(novoCrm)) != 6:
                    return {'error': 'CRM deve conter 6 dígitos'}, 400
                if Especialista.select().where(
                    (Especialista.crm == novoCrm) & 
                    (Especialista.id != idEspecialista)
                ).exists():
                    return {'error': 'CRM já está em uso por outro especialista'}, 400
                updates['crm'] = novoCrm

            if novoEmail != None:
                novoEmail = novoEmail.lower().strip()
                if '@' not in novoEmail or '.' not in novoEmail.split('@')[-1]:
                    return {'error': 'Formato de email inválido'}, 400
                if Especialista.select().where(
                    (Especialista.email == novoEmail) & (Especialista.id != idEspecialista)
                ).exists():
                    return {'error': 'Email já está em uso por outro especialista'}, 400
                updates['email'] = novoEmail

            if novaSenha != None:
                if len(novaSenha) < 6:
                    return {'error': 'Senha deve ter pelo menos 6 caracteres'}, 400
                updates['senha'] = generate_password_hash(novaSenha)

            Especialista.update(**updates).where(Especialista.id == idEspecialista).execute()
            
            updated = Especialista.get_by_id(idEspecialista)
            
            return {
                'message': 'Especialista atualizado com sucesso',
                'especialista': {
                    'id': updated.id,
                    'nome': updated.nome,
                    'crm': updated.crm,
                    'email': updated.email,
                }
            }, 200

        except Exception as e:
            return {'error': f'Erro ao atualizar especialista: {str(e)}'}, 500

    def deleteEspecialista(self, idEspecialista: int):
        try:
            especialista = Especialista.get_or_none(Especialista.id == idEspecialista)
            if not especialista:
                return False

            especialista.delete_instance()
            return True

        except Exception as e:
            raise e