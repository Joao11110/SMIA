from Model.Especialista import Especialista
from Model.DataBase import ConnectDataBase
from Model.Medicamento import Medicamento
from Model.Paciente import Paciente
from peewee import DoesNotExist
from datetime import datetime
from flask import jsonify

class MedicamentoController(ConnectDataBase):
    def __init__(self):
        super().__init__()

    def _getRelacionamento(self, model, id_relacionamento):
        try:
            return model.get_by_id(id_relacionamento)
        except DoesNotExist:
            return None

    def _medicamentoToDict(self, medicamento):
        paciente = self._getRelacionamento(Paciente, medicamento.paciente_id)
        especialista = self._getRelacionamento(Especialista, medicamento.especialista_id)
        
        def format_datetime(value, time_only=False):
            if not value:
                return None
            if isinstance(value, str):
                try:
                    if time_only:
                        value = datetime.strptime(value, '%H:%M:%S').time()
                    else:
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return value
            if time_only:
                return value.strftime('%H:%M:%S') if hasattr(value, 'strftime') else str(value)
            return value.strftime('%Y-%m-%d %H:%M:%S') if hasattr(value, 'strftime') else str(value)
        
        return {
            "id": medicamento.id,
            "nome": medicamento.nome,
            "intervalo": format_datetime(medicamento.intervalo, time_only=True),
            "quantidade": float(medicamento.quantidade),
            "data_inicio": format_datetime(medicamento.data_inicio),
            "data_fim": format_datetime(medicamento.data_fim),
            "paciente": {
                "id": paciente.id,
                "nome": paciente.nome
            } if paciente else None,
            "especialista": {
                "id": especialista.id,
                "nome": especialista.nome
            } if especialista else None
        }

    def _verificarRelacionamentos(self, paciente_id, especialista_id):
        try:
            Paciente.get_by_id(paciente_id)
        except DoesNotExist:
            raise ValueError(f"Paciente com ID {paciente_id} não encontrado")
        
        try:
            Especialista.get_by_id(especialista_id)
        except DoesNotExist:
            raise ValueError(f"Especialista com ID {especialista_id} não encontrado")

    def createMedicamento(self, nome: str, intervalo: str, quantidade: float, 
                         data_inicio: str, data_fim: str, paciente: int, especialista: int):
        try:
            if not all([nome, intervalo, quantidade, data_inicio, paciente, especialista]):
                return jsonify({"error": "Todos os campos obrigatórios devem ser preenchidos"}), 400
            
            self._verificarRelacionamentos(paciente, especialista)

            medicamento = Medicamento.create(
                nome=nome, 
                intervalo=intervalo, 
                quantidade=quantidade, 
                data_inicio=data_inicio,
                data_fim=data_fim, 
                paciente=paciente, 
                especialista=especialista
            )
            return jsonify({
                "message": "Medicamento criado com sucesso",
                "medicamento": self._medicamentoToDict(medicamento)
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def getMedicamento(self, idMedicamento: int):
        try:
            medicamento = Medicamento.get_by_id(idMedicamento)
            return jsonify(self._medicamentoToDict(medicamento)), 200
        except DoesNotExist:
            return jsonify({"error": "Medicamento não encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def listMedicamentos(self):
        try:
            medicamentos = Medicamento.select()
            result = [self._medicamentoToDict(med) for med in medicamentos]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def updateMedicamento(self, idMedicamento: int, novoNome: str, novoIntervalo: str, novaQuantidade: float, novaData_inicio: str, novaData_fim: str, novoPaciente: int, novoEspecialista: int):
        try:
            m = Medicamento.get_by_id(idMedicamento)
            m.nome = novoNome
            m.intervalo = novoIntervalo
            m.quantidade = novaQuantidade
            m.data_inicio = novaData_inicio
            m.data_fim = novaData_fim
            m.paciente = novoPaciente
            m.especialista = novoEspecialista
            m.save()
            return jsonify({
                "message": "Medicamento atualizado com sucesso",
                "medicamento": self._medicamentoToDict(m)
            }), 200
        except Medicamento.DoesNotExist:
            return jsonify({"error": "Medicamento não encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def deleteMedicamento(self, idMedicamento: int):
        try:
            medicamento = Medicamento.get_by_id(idMedicamento)
            medicamento_dict = self._medicamentoToDict(medicamento)
            medicamento.delete_instance()
            return jsonify({
                "message": "Medicamento deletado com sucesso",
                "medicamento": medicamento_dict
            }), 200
        except Medicamento.DoesNotExist:
            return jsonify({"error": "Medicamento não encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500