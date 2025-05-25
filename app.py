from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory
from Controller.EspecialistaCtrl import EspecialistaController
from Controller.PacienteCtrl import PacienteController
from Controller.MedicamentoCtrl import MedicamentoController
import os

app = Flask(__name__, static_folder='View')
CORS(app, origins=["http://localhost:5000"])

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

especialista_controller = EspecialistaController()
paciente_controller = PacienteController()
medicamento_ctrl = MedicamentoController()

@app.route('/api/especialistas', methods=['GET'])
def get_especialistas():
    try:
        especialistas = EspecialistaController().listEspecialista()
        especialistas_dict = [{
            'id': esp.id,
            'nome': esp.nome,
            'crm': esp.crm,
            'email': esp.email
        } for esp in especialistas]
        return jsonify(especialistas_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from playhouse.shortcuts import model_to_dict

@app.route('/api/especialistas/<int:id>', methods=['GET'])
def get_especialista(id):
    try:
        especialista = EspecialistaController().readEspecialista(id)
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
            'id': novo_especialista.id,
            'nome': novo_especialista.nome,
            'crm': novo_especialista.crm,
            'email': novo_especialista.email
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/especialistas/<int:id>', methods=['PUT'])
def update_especialista(id):
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({'error': 'Nenhum dado fornecido para atualização'}), 400

        especialista_atualizado = EspecialistaController().updateEspecialista(
            idEspecialista=id,
            novoNome=dados.get('nome'),
            novoCrm=dados.get('crm'),
            novoEmail=dados.get('email'),
            novaSenha=dados.get('senha')
        )
        
        if not especialista_atualizado:
            return jsonify({'error': 'Especialista não encontrado'}), 404
            
        return jsonify({
            'id': especialista_atualizado.id,
            'nome': especialista_atualizado.nome,
            'crm': especialista_atualizado.crm,
            'email': especialista_atualizado.email,
            'message': 'Especialista atualizado com sucesso'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    try:
        pacientes = paciente_controller.listPaciente()
        pacientes_dict = [{
            'id': pac.id,
            'nome': pac.nome,
            'cpf': pac.cpf,
            'email': pac.email,
            'data_nascimento': str(pac.data_nascimento),
            'peso': pac.peso,
            'altura': pac.altura,
            'especialista': pac.especialista.id
        } for pac in pacientes]
        return jsonify(pacientes_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes/<int:id>', methods=['GET'])
def get_paciente(id):
    try:
        paciente = paciente_controller.readPaciente(id)
        if paciente:
            return jsonify({
                'id': paciente.id,
                'nome': paciente.nome,
                'cpf': paciente.cpf,
                'email': paciente.email,
                'data_nascimento': str(paciente.data_nascimento),
                'peso': paciente.peso,
                'altura': paciente.altura,
                'especialista': paciente.especialista.id
            })
        return jsonify({'error': 'Paciente não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
def create_paciente():
    try:
        dados = request.get_json()

        if not all(key in dados for key in ['nome', 'cpf', 'email', 'data_nascimento', 'peso', 'altura', 'especialista']):
            return jsonify({'error': 'Dados incompletos'}), 400
            
        novo_paciente = paciente_controller.createPaciente(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            data_nascimento=dados['data_nascimento'],
            peso=dados['peso'],
            altura=dados['altura'],
            especialista=dados['especialista']
        )
        
        return jsonify({
            'id': novo_paciente.id,
            'nome': novo_paciente.nome,
            'message': 'Paciente criado com sucesso'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    try:
        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400
            
        deletado = paciente_controller.deletePaciente(id)
        
        if deletado:
            return jsonify({'message': 'Paciente deletado com sucesso'}), 200
        else:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes/<int:id>', methods=['PUT'])
def update_paciente(id):
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({'error': 'Nenhum dado fornecido para atualização'}), 400

        paciente_atualizado = paciente_controller.updatePaciente(
            idPaciente=id,
            novoNome=dados.get('nome'),
            novoCpf=dados.get('cpf'),
            novoEmail=dados.get('email'),
            novaData_nascimento=dados.get('data_nascimento'),
            novoPeso=dados.get('peso'),
            novaAltura=dados.get('altura'),
            novoEspecialista=dados.get('especialista')
        )
        
        if not paciente_atualizado:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        return jsonify({
            'id': paciente_atualizado.id,
            'nome': paciente_atualizado.nome,
            'cpf': paciente_atualizado.cpf,
            'email': paciente_atualizado.email,
            'data_nascimento': str(paciente_atualizado.data_nascimento),
            'peso': paciente_atualizado.peso,
            'altura': paciente_atualizado.altura,
            'especialista': paciente_atualizado.especialista.id,
            'message': 'Paciente atualizado com sucesso'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/medicamentos', methods=['POST'])
def criar_medicamento():
    data = request.get_json()
    try:
        medicamento = medicamento_ctrl.createMedicamento(
            nome=data['nome'],
            intervalo=data['intervalo'],
            quantidade=data['quantidade'],
            data_inicio=data['data_inicio'],
            data_fim=data['data_fim'],
            paciente=data['paciente'],
            especialista=data['especialista']
        )
        return jsonify({"message": "Medicamento criado com sucesso!", "id": medicamento.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/medicamentos/por-paciente/<int:paciente_id>', methods=['GET'])
def listar_medicamentos_por_paciente(paciente_id):
    try:
        medicamentos = medicamento_ctrl.listMedicamentoPorPaciente(paciente_id)
        return jsonify(medicamentos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/medicamentos/<int:id>', methods=['GET'])
def obter_medicamento(id):
    try:
        medicamento = medicamento_ctrl.readMedicamento(id)
        if medicamento:
            return jsonify(medicamento), 200
        return jsonify({"message": "Medicamento não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/medicamentos/<int:id>', methods=['PUT'])
def atualizar_medicamento(id):
    data = request.get_json()
    try:
        medicamento_ctrl.updateMedicamento(
            idMedicamento=id,
            novoNome=data.get('nome'),
            novoIntervalo=data.get('intervalo'),
            novaQuantidade=data.get('quantidade'),
            novaData_inicio=data.get('data_inicio'),
            novaData_fim=data.get('data_fim'),
            novoPaciente=data.get('paciente'),
            novoEspecialista=data.get('especialista')
        )
        return jsonify({"message": "Medicamento atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/medicamentos/<int:id>', methods=['DELETE'])
def deletar_medicamento(id):
    try:
        medicamento_ctrl.deleteMedicamento(id)
        return jsonify({"message": "Medicamento deletado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def serve_index():
    return send_from_directory('View', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('View', filename)

@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint não encontrado'}), 404
    return send_from_directory('View', 'index.html')

if __name__ == '__main__':
    if not os.path.exists('View'):
        os.makedirs('View')

    app.run(debug=True, host='0.0.0.0', port=5000)