from Model.DataBase import ConnectDataBase
from Model.Especialista import Especialista
from Model.Medicamento import Medicamento
from Model.Lembrete import Lembrete
from Model.Paciente import Paciente
from flask import jsonify
from peewee import JOIN

class LembreteController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def createLembrete(self, data_hora: str, status: int, medicamento_id: int, paciente_id: int):
        try:
            lembrete = Lembrete.create(
                data_hora=data_hora,
                status=status,
                medicamento=medicamento_id,
                paciente=paciente_id
            )
            return jsonify({
                'id': lembrete.id,
                'data_hora': lembrete.data_hora,
                'status': lembrete.status,
                'medicamento_id': lembrete.medicamento.id,
                'paciente_id': lembrete.paciente.id
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    def getLembrete(self, idLembrete: int):
        try:
            lembrete = (Lembrete.select(
                            Lembrete,
                            Paciente,
                            Medicamento
                        )
                        .join(Paciente, JOIN.LEFT_OUTER)
                        .join(Medicamento, JOIN.LEFT_OUTER)
                        .where(Lembrete.id == idLembrete)
                        .first())

            if not lembrete:
                return {'error': 'Lembrete não encontrado'}, 404

            paciente_data = {
                'id': lembrete.paciente.id,
                'nome': lembrete.paciente.nome
            } if lembrete.paciente else None

            medicamento_data = {
                'id': lembrete.medicamento.id,
                'nome': lembrete.medicamento.nome
            } if lembrete.medicamento else None

            return {
                'id': lembrete.id,
                'data_hora': lembrete.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'status': lembrete.status,
                'paciente': paciente_data,
                'medicamento': medicamento_data
            }

        except Exception as e:
            return {'error': f'Erro ao buscar lembrete: {str(e)}'}, 500

    def listLembretes(self):
        try:
            query = (Lembrete
                    .select(
                        Lembrete,
                        Paciente.nome.alias('nome_paciente'),
                        Especialista.nome.alias('nome_especialista'),
                        Medicamento.nome.alias('nome_medicamento')
                    )
                    .join(Paciente)
                    .join(Especialista)
                    .join(Medicamento))
            
            lembretes = []
            for lembrete in query:
                lembretes.append({
                    'id': lembrete.id,
                    'data_hora': lembrete.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': lembrete.status,
                    'paciente': {
                        'id': lembrete.paciente.id,
                        'nome': lembrete.paciente.nome
                    },
                    'medicamento': {
                        'id': lembrete.medicamento.id,
                        'nome': lembrete.medicamento.nome
                    }
                })
            
            return lembretes if lembretes else {'message': 'Nenhum lembrete encontrado'}

        except Exception as e:
            return {'error': f'Erro ao buscar lembretes: {str(e)}'}

    def updateLembrete(self, idLembrete: int, nova_data_hora: str, novo_status: int, novo_medicamento_id: int, novo_paciente_id: int):
        try:
            lembrete = Lembrete.get_by_id(idLembrete)
            lembrete.data_hora = nova_data_hora
            lembrete.status = novo_status
            lembrete.medicamento = novo_medicamento_id
            lembrete.paciente = novo_paciente_id
            lembrete.save()
            return jsonify({'message': 'Lembrete atualizado com sucesso'}), 200
        except Lembrete.DoesNotExist:
            return jsonify({'error': 'Lembrete não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    def deleteLembrete(self, idLembrete: int):
        try:
            lembrete = Lembrete.get_by_id(idLembrete)
            lembrete.delete_instance()
            return jsonify({'message': 'Lembrete deletado com sucesso'}), 200
        except Lembrete.DoesNotExist:
            return jsonify({'error': 'Lembrete não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400