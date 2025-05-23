from Model.Paciente import Paciente
from Model.DataBase import ConnectDataBase
from flask import jsonify
from datetime import datetime
from Model.Especialista import Especialista

class PacienteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def _serializePaciente(self, paciente):
        return {
            'id': paciente.id,
            'nome': paciente.nome,
            'cpf': paciente.cpf,
            'email': paciente.email,
            'senha': paciente.senha,
            'data_nascimento': paciente.data_nascimento,
            'peso': paciente.peso,
            'altura': paciente.altura,
            'especialista': {
                'id': paciente.especialista.id,
                'nome': paciente.especialista.nome
            }
        }

    def createPaciente(self, nome: str, cpf: int, email: str, data_nascimento: str, peso: float, altura: float, especialista: int):
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
                
                return jsonify(self._serializePaciente(paciente))
            except Exception as e:
                return jsonify({'error': str(e)}), 400

    def getPaciente(self, idPaciente: int):
        try:
            paciente = Paciente.get(Paciente.id == idPaciente)
            return jsonify(self._serializePaciente(paciente))
        except Paciente.DoesNotExist:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    def listPacientes(self):
        try:
            return list(Paciente().select())
        except Exception as e:
            raise e

    def updatePaciente(self, idPaciente: int, novoNome: str, novoCpf: int, novoEmail: str, novaData_nascimento: str, novoPeso: float, novaAltura: float, novoEspecialista: int):
        try:
            paciente = Paciente.get(Paciente.id == idPaciente)
            
            if len(str(novoCpf)) != 11:
                return jsonify({'error': 'CPF deve conter 11 dígitos'}), 400
            
            if '@' not in novoEmail or '.' not in novoEmail.split('@')[-1]:
                return jsonify({'error': 'Email inválido'}), 400
            
            try:
                datetime.strptime(novaData_nascimento, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Formato de data inválido (use YYYY-MM-DD)'}), 400

            if novoPeso <= 0 or novoPeso > 350:
                return jsonify({'error': 'Peso deve ser entre 0.1 e 350 kg'}), 400
                
            if novaAltura <= 0 or novaAltura > 2.5:
                return jsonify({'error': 'Altura deve ser entre 0.1 e 2.5 metros'}), 400
                
            try:
                Especialista.get_by_id(novoEspecialista)
            except Especialista.DoesNotExist:
                return jsonify({'error': 'Especialista não encontrado'}), 404

            if Paciente.select().where((Paciente.cpf == novoCpf) & (Paciente.id != idPaciente)).exists():
                return jsonify({'error': 'CPF já cadastrado para outro paciente'}), 400
                
            if Paciente.select().where((Paciente.email == novoEmail) & (Paciente.id != idPaciente)).exists():
                return jsonify({'error': 'Email já cadastrado para outro paciente'}), 400

            paciente.nome = novoNome.strip()
            paciente.cpf = novoCpf
            paciente.email = novoEmail.lower().strip()
            paciente.data_nascimento = novaData_nascimento
            paciente.peso = round(novoPeso, 1)
            paciente.altura = round(novaAltura, 2)
            paciente.especialista = novoEspecialista
            paciente.save()
            
            return jsonify({
                'message': 'Paciente atualizado com sucesso',
                'paciente': {
                    'id': paciente.id,
                    'nome': paciente.nome,
                    'cpf': paciente.cpf,
                    'email': paciente.email,
                    'data_nascimento': paciente.data_nascimento,
                    'peso': paciente.peso,
                    'altura': paciente.altura,
                    'especialista': paciente.especialista.id
                }
            }), 200
            
        except Paciente.DoesNotExist:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar paciente: {str(e)}'}), 500

    def deletePaciente(self, idPaciente: int):
        try:
            paciente = Paciente.get(Paciente.id == idPaciente)
            paciente.delete_instance()
            return jsonify({'message': 'Paciente deletado com sucesso'}), 200
        except Paciente.DoesNotExist:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400