from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory
from Controller.EspecialistaCtrl import EspecialistaController
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