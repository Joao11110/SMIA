from flask import Flask, jsonify, request, send_from_directory
from Controller.EspecialistaController import EspecialistaController
from Controller.LembreteController import LembreteController
from Controller.MedicamentoController import MedicamentoController
from Controller.PacienteController import PacienteController
import os


app = Flask(__name__, static_folder='View')


@app.route('/api/especialistas', methods=['POST'])
def create_especialista():
    try:
        dados = request.get_json()

        if not all(key in dados for key in ['nome', 'crm', 'email', 'senha']):
            return jsonify({'error': 'Dados incompletos'}), 400

        novo_especialista = EspecialistaController().createEspecialista(
            nome=dados['nome'],
            crm=dados['crm'],
            email=dados['email'],
            senha=dados['senha']
        )

        return jsonify({
            'nome': novo_especialista.nome,
            'crm': novo_especialista.crm,
            'email': novo_especialista.email,
            'id': novo_especialista.id
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/especialistas', methods=['GET'])
def list_especialistas():
    try:
        especialistas = EspecialistaController().listEspecialista()
        especialistas_dict = [{
            'id': _.id,
            'nome': _.nome,
            'crm': _.crm,
            'email': _.email
        } for _ in especialistas]
        return jsonify(especialistas_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from playhouse.shortcuts import model_to_dict


@app.route('/api/especialistas/<int:id>', methods=['GET'])
def get_especialista(id):
    try:
        especialista = EspecialistaController().getEspecialista(id)
        if especialista:
            return jsonify({
                'id': especialista.id,
                'nome': especialista.nome,
                'crm': especialista.crm,
                'email': especialista.email,
                'senha': especialista.senha
            })
        return jsonify({'error': 'Especialista não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/especialistas/<int:idEspecialista>', methods=['PUT'])
def update_especialista(idEspecialista):
    data = request.get_json()
    result, status_code = EspecialistaController().updateEspecialista(
        idEspecialista,
        novoNome=data.get('nome'),
        novoCrm=data.get('crm'),
        novoEmail=data.get('email'),
        novaSenha=data.get('senha')
    )
    return jsonify(result), status_code


@app.route('/api/especialistas/<int:id>', methods=['DELETE'])
def delete_especialista(id):
    try:
        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        deletado = EspecialistaController().deleteEspecialista(id)

        if deletado:
            return jsonify({'message': 'Especialista deletado com sucesso'}), 200
        else:
            return jsonify({'error': 'Especialista não encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pacientes', methods=['POST'])
def create_paciente():
    data = request.get_json()
    return PacienteController().createPaciente(
        data['nome'],
        data['cpf'],
        data['email'],
        data['data_nascimento'],
        data['peso'],
        data['altura'],
        data['especialista']
    )


@app.route('/api/pacientes/<int:idPaciente>', methods=['GET'])
def get_paciente(idPaciente):
    return PacienteController().getPaciente(idPaciente)


@app.route('/api/pacientes', methods=['GET'])
def list_pacientes():
    try:
        pacientes = PacienteController().listPacientes()
        pacientes_dict = [{
            'id': paciente.id,
            'nome': paciente.nome,
            'cpf': paciente.cpf,
            'email': paciente.email,
            'data_nascimento': paciente.data_nascimento.strftime('%Y-%m-%d'),
            'peso': paciente.peso,
            'altura': paciente.altura,
            'especialista': paciente.especialista.id
        } for paciente in pacientes]
        return jsonify(pacientes_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pacientes/<int:idPaciente>', methods=['PUT'])
def update_paciente(idPaciente):
    data = request.get_json()
    return PacienteController().updatePaciente(
        idPaciente,
        data['nome'],
        data['cpf'],
        data['email'],
        data['data_nascimento'],
        data['peso'],
        data['altura'],
        data['especialista']
    )


@app.route('/api/pacientes/<int:idPaciente>', methods=['DELETE'])
def delete_paciente(idPaciente):
    return PacienteController().deletePaciente(idPaciente)


@app.route('/api/medicamentos', methods=['POST'])
def create_medicamento():
    data = request.get_json()
    return MedicamentoController().createMedicamento(
        nome=data.get('nome'),
        intervalo=data.get('intervalo'),
        quantidade=data.get('quantidade'),
        data_inicio=data.get('data_inicio'),
        data_fim=data.get('data_fim'),
        paciente=data.get('paciente'),
        especialista=data.get('especialista')
    )


@app.route('/api/medicamentos/<int:id>', methods=['GET'])
def get_medicamento(id):
    return MedicamentoController().getMedicamento(id)


@app.route('/api/medicamentos', methods=['GET'])
def list_medicamentos():
    return MedicamentoController().listMedicamentos()


@app.route('/api/medicamentos/<int:id>', methods=['PUT'])
def update_medicamento(id):
    data = request.get_json()
    return MedicamentoController().updateMedicamento(
        idMedicamento=id,
        novoNome=data.get('nome'),
        novoIntervalo=data.get('intervalo'),
        novaQuantidade=data.get('quantidade'),
        novaData_inicio=data.get('data_inicio'),
        novaData_fim=data.get('data_fim'),
        novoPaciente=data.get('paciente'),
        novoEspecialista=data.get('especialista')
    )


@app.route('/api/medicamentos/<int:id>', methods=['DELETE'])
def delete_medicamento(id):
    return MedicamentoController().deleteMedicamento(id)


@app.route('/api/lembretes', methods=['POST'])
def create_lembrete():
    data = request.get_json()
    return LembreteController().createLembrete(
        data['data_hora'],
        data['status'],
        data['medicamento'],
        data['paciente']
    )


@app.route('/api/lembretes/<int:idLembrete>', methods=['GET'])
def get_lembrete(idLembrete):
    try:
        result, status_code = LembreteController().getLembrete(idLembrete)
        return jsonify(result), status_code
    except ValueError:
        result = LembreteController().getLembrete(idLembrete)
        if isinstance(result, tuple) and len(result) == 2:
            return jsonify(result[0]), result[1]
        return jsonify(result), 200


@app.route('/api/lembretes', methods=['GET'])
def list_lembretes():
    try:
        result = LembreteController().listLembretes()
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/lembretes/<int:idLembrete>', methods=['DELETE'])
def delete_lembrete(idLembrete):
    return LembreteController().deleteLembrete(idLembrete)


@app.route('/')
def serve_index():
    return send_from_directory('View', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('View', filename)


@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint nao encontrado'}), 404
    return send_from_directory('View', 'index.html')

if __name__ == '__main__':
    if not os.path.exists('View'):
        os.makedirs('View')
    app.run(debug=True, port=3000)