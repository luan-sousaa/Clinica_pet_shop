from flask import render_template, request, jsonify, current_app as app, send_from_directory
from app.models import Usuario, GrupoUsuario, Cliente, Pet, Veterinario, Consulta, Vacina
from app.auth import create_token, token_required, require_vet, require_client, role_required
from app.database import Database
from app.prescricao_storage import PrescricaoStorage
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

# ========== ROTAS ESTÁTICAS ==========

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Servir arquivos estáticos"""
    return send_from_directory(app.static_folder, path)

# ========== AUTENTICAÇÃO ==========

@app.route('/login', methods=['POST'])
def login():
    """Login de usuário com autenticação JWT"""
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        
        if not email or not senha:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400
        
        # Autenticar usuário (a senha será comparada com o hash SHA256)
        usuario = Usuario.authenticate(email, senha)
        
        if not usuario:
            return jsonify({'message': 'Credenciais inválidas'}), 401
        
        # Criar token JWT
        token = create_token(usuario)
        
        # Preparar resposta com dados do usuário
        user_response = {
            'id': usuario['ID_USUARIO'],
            'nome': usuario['NOME_COMPLETO'],
            'email': usuario['EMAIL'],
            'tipo': usuario['TIPO_ACESSO'],
            'role': usuario['ROLE_MYSQL']
        }
        
        # Se for cliente, buscar dados do pet
        if usuario['TIPO_ACESSO'] == 'Cliente':
            cliente = Cliente.find_by_id(usuario['ID_USUARIO'])
            if cliente:
                user_response['pet_id'] = cliente['ID_PET']
                user_response['cpf'] = cliente['CPF']
        
        # Se for veterinário, buscar CRMV
        elif usuario['TIPO_ACESSO'] == 'Veterinario':
            vet = Veterinario.find_by_usuario_id(usuario['ID_USUARIO'])
            if vet:
                user_response['crmv'] = vet['CRMV']
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'token': token,
            'user': user_response
        }), 200
        
    except Error as e:
        logger.error(f"Erro no login: {e}")
        return jsonify({'message': 'Erro ao realizar login'}), 500

@app.route('/cadastro', methods=['POST'])
def cadastro():
    """Cadastro de cliente (tutor) e pet"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['nome_tutor', 'cpf', 'email', 'senha', 'confirmar_senha', 
                              'nome_pet', 'raca_pet', 'datanascimento']
        
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'message': f'Campo {campo} é obrigatório'}), 400
        
        # Validar senhas
        if data['senha'] != data['confirmar_senha']:
            return jsonify({'message': 'Senhas não coincidem'}), 400
        
        # Verificar se email já existe
        if Usuario.exists(data['email']):
            return jsonify({'message': 'Email já cadastrado'}), 400
        
        # Buscar grupo de usuário Cliente
        grupo_cliente = GrupoUsuario.find_by_tipo('Cliente')
        if not grupo_cliente:
            return jsonify({'message': 'Erro ao buscar grupo de cliente'}), 500
        
        # Calcular idade do pet a partir da data de nascimento
        from datetime import datetime
        try:
            data_nasc = datetime.strptime(data['datanascimento'], '%Y-%m-%d')
            hoje = datetime.now()
            idade = (hoje - data_nasc).days / 365.25
        except:
            idade = 0
        
        # Criar pet primeiro (precisamos do ID para criar o cliente)
        pet_id = Pet.create(
            nome=data['nome_pet'],
            raca=data['raca_pet'],
            idade=idade,
            observacoes=data.get('observacoes_pet', '')
        )
        
        # Criar usuário (a senha será automaticamente hasheada pelo trigger)
        usuario_id = Usuario.create(
            nome_completo=data['nome_tutor'],
            email=data['email'],
            senha=data['senha'],
            grupo_usuario_id=grupo_cliente['ID_ACESSO']
        )
        
        # Criar cliente
        Cliente.create(
            usuario_id=usuario_id,
            telefone=data.get('telefone', ''),
            cpf=data['cpf'].replace('.', '').replace('-', ''),
            id_pet=pet_id
        )
        
        return jsonify({
            'message': f'Usuário {data["nome_tutor"]} cadastrado com sucesso!',
            'usuario_id': usuario_id,
            'pet_id': pet_id
        }), 201
        
    except Error as e:
        logger.error(f"Erro no cadastro: {e}")
        return jsonify({'message': f'Erro ao realizar cadastro: {str(e)}'}), 500

@app.route('/cadastro_vet', methods=['POST'])
def cadastro_vet():
    """Cadastro de veterinário"""
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['nome_completo', 'email', 'senha', 'confirmar_senha', 'crmv']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'message': f'Campo {campo} é obrigatório'}), 400
        
        # Validar senhas
        if data['senha'] != data['confirmar_senha']:
            return jsonify({'message': 'Senhas não coincidem'}), 400
        
        # Verificar se email já existe
        if Usuario.exists(data['email']):
            return jsonify({'message': 'Email já cadastrado'}), 400
        
        # Buscar grupo de usuário Veterinário
        grupo_vet = GrupoUsuario.find_by_tipo('Veterinario')
        if not grupo_vet:
            return jsonify({'message': 'Erro ao buscar grupo de veterinário'}), 500
        
        # Extrair apenas números do CRMV (remove letras, barras, espaços)
        import re
        crmv_numerico = re.sub(r'[^0-9]', '', data['crmv'])
        
        if not crmv_numerico:
            return jsonify({'message': 'CRMV inválido. Digite apenas números.'}), 400
        
        try:
            crmv_int = int(crmv_numerico)
        except ValueError:
            return jsonify({'message': 'CRMV inválido'}), 400
        
        # Criar usuário (a senha será automaticamente hasheada pelo trigger)
        usuario_id = Usuario.create(
            nome_completo=data['nome_completo'],
            email=data['email'],
            senha=data['senha'],
            grupo_usuario_id=grupo_vet['ID_ACESSO']
        )
        
        # Criar veterinário
        Veterinario.create(
            crmv=crmv_int,
            usuario_id=usuario_id,
            salario=data.get('salario'),
            turno=data.get('turno')
        )
        
        return jsonify({
            'message': f'Veterinário {data["nome_completo"]} cadastrado com sucesso',
            'crmv': data['crmv']
        }), 201
        
    except Error as e:
        logger.error(f"Erro no cadastro de veterinário: {e}")
        return jsonify({'message': f'Erro ao realizar cadastro: {str(e)}'}), 500

@app.route('/esqueceu_senha', methods=['POST'])
def esqueceu_senha():
    """Redefinir senha do usuário"""
    try:
        data = request.get_json()
        email = data.get('email')
        nova_senha = data.get('nova_senha')
        confirmar_nova_senha = data.get('confirmar_nova_senha')
        
        if not email or not nova_senha or not confirmar_nova_senha:
            return jsonify({'message': 'Todos os campos são obrigatórios'}), 400
        
        if nova_senha != confirmar_nova_senha:
            return jsonify({'message': 'Senhas não coincidem'}), 400
        
        # Verificar se usuário existe
        usuario = Usuario.find_by_email(email)
        if not usuario:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        # Atualizar senha (será automaticamente hasheada pelo trigger)
        Usuario.update_password(email, nova_senha)
        
        return jsonify({'message': f'Senha redefinida para {email} com sucesso'}), 200
        
    except Error as e:
        logger.error(f"Erro ao redefinir senha: {e}")
        return jsonify({'message': 'Erro ao redefinir senha'}), 500

# ========== ROTAS DO CLIENTE ==========

@app.route('/buscar_pet_cpf/<cpf>', methods=['GET'])
@token_required
def buscar_pet_por_cpf(cpf):
    """Buscar dados do pet por CPF do cliente (para veterinários)"""
    try:
        # Buscar cliente por CPF
        cliente = Cliente.find_by_cpf(cpf)
        
        if not cliente:
            return jsonify({'message': 'Cliente não encontrado com este CPF'}), 404
        
        # Buscar dados completos do pet
        pet = Pet.find_by_id(cliente['ID_PET'])
        
        if not pet:
            return jsonify({'message': 'Pet não encontrado'}), 404
        
        # Calcular data de nascimento aproximada a partir da idade
        from datetime import datetime, timedelta
        datanascimento = None
        if pet['IDADE']:
            anos = int(pet['IDADE'])
            dias = int((pet['IDADE'] - anos) * 365)
            data_aproximada = datetime.now() - timedelta(days=(anos * 365 + dias))
            datanascimento = data_aproximada.strftime('%Y-%m-%d')
        
        pet_data = {
            'id_pet': pet['ID_PET'],
            'nome_pet': pet['NOME'],
            'raca_pet': pet['RACA'],
            'idade': float(pet['IDADE']) if pet['IDADE'] else 0,
            'datanascimento': datanascimento,
            'observacoes_pet': pet['OBSERVACOES'] if pet['OBSERVACOES'] else 'Nenhuma',
            'tutor_nome': cliente['NOME_COMPLETO'],
            'tutor_email': cliente['EMAIL'],
            'tutor_telefone': cliente.get('TELEFONE', ''),
            'cpf': cpf
        }
        
        return jsonify(pet_data), 200
        
    except Error as e:
        logger.error(f"Erro ao buscar pet por CPF: {e}")
        return jsonify({'message': 'Erro ao buscar dados do pet'}), 500

@app.route('/dados_pet', methods=['GET'])
@token_required
def dados_pet():
    """Obter dados do pet do cliente logado"""
    try:
        usuario_id = request.user['user_id']
        
        # Buscar pet do cliente
        pet = Cliente.get_pet(usuario_id)
        
        if not pet:
            return jsonify({'message': 'Pet não encontrado'}), 404
        
        # Buscar consultas do pet
        consultas = Consulta.find_by_pet(pet['ID_PET'])
        
        # Formatar consultas
        servicos_agendados = []
        for consulta in consultas:
            servicos_agendados.append({
                'servico': 'Consulta Veterinária',
                'data': str(consulta['DATA_CONSULTA']),
                'veterinario': consulta['NOME_VET'],
                'valor': float(consulta['VALOR']) if consulta['VALOR'] else 0
            })
        
        # Calcular data de nascimento aproximada a partir da idade
        from datetime import datetime, timedelta
        datanascimento = None
        if pet['IDADE']:
            anos = int(pet['IDADE'])
            dias = int((pet['IDADE'] - anos) * 365)
            data_aproximada = datetime.now() - timedelta(days=(anos * 365 + dias))
            datanascimento = data_aproximada.strftime('%Y-%m-%d')
        
        pet_data = {
            'id_pet': pet['ID_PET'],
            'nome_pet': pet['NOME'],
            'raca_pet': pet['RACA'],
            'idade': float(pet['IDADE']) if pet['IDADE'] else 0,
            'datanascimento': datanascimento,
            'observacoes_pet': pet['OBSERVACOES'] if pet['OBSERVACOES'] else 'Nenhuma',
            'servicos_agendados': servicos_agendados
        }
        
        return jsonify(pet_data), 200
        
    except Error as e:
        logger.error(f"Erro ao buscar dados do pet: {e}")
        return jsonify({'message': 'Erro ao buscar dados do pet'}), 500

@app.route('/consultas/<int:pet_id>', methods=['GET'])
@token_required
def listar_consultas_pet(pet_id):
    """Listar consultas agendadas de um pet"""
    try:
        consultas = Consulta.find_by_pet(pet_id)
        
        consultas_formatadas = []
        for consulta in consultas:
            consultas_formatadas.append({
                'id': consulta['ID_PROCEDIMENTO'],
                'data_consulta': str(consulta['DATA_CONSULTA']),
                'veterinario': consulta['NOME_VET'],
                'crmv': consulta['CRMV'],
                'valor': float(consulta['VALOR']) if consulta['VALOR'] else 0,
                'status': 'agendada'
            })
        
        return jsonify({
            'pet_id': pet_id,
            'total_consultas': len(consultas_formatadas),
            'consultas': consultas_formatadas
        }), 200
        
    except Error as e:
        logger.error(f"Erro ao listar consultas: {e}")
        return jsonify({'message': 'Erro ao listar consultas'}), 500

@app.route('/historico/<int:pet_id>/vacinas', methods=['GET'])
@token_required
def listar_vacinas_pet(pet_id):
    """Ver histórico de vacinas do pet (usa VIEW HISTORICO_VACINA)"""
    try:
        vacinas = Vacina.get_historico_pet(pet_id)
        
        vacinas_formatadas = []
        for vacina in vacinas:
            vacinas_formatadas.append({
                'nome_vacina': vacina['NOME'],
                'dose': vacina['DOSE'],
                'data_aplicacao': str(vacina['DATA_APLICADO'])
            })
        
        return jsonify({
            'pet_id': pet_id,
            'total_vacinas': len(vacinas_formatadas),
            'vacinas': vacinas_formatadas
        }), 200
        
    except Error as e:
        logger.error(f"Erro ao listar vacinas: {e}")
        return jsonify({'message': 'Erro ao listar vacinas'}), 500

# ========== ROTAS DO VETERINÁRIO ==========

@app.route('/agendamentos', methods=['POST'])
@require_vet
def criar_agendamento():
    """Criar novo agendamento/consulta (Veterinário)"""
    try:
        data = request.get_json()
        
        # Validar campos
        campos_obrigatorios = ['cpf_cliente', 'data_agendamento', 'valor']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'message': f'Campo {campo} é obrigatório'}), 400
        
        # Buscar cliente por CPF
        cpf_limpo = data['cpf_cliente'].replace('.', '').replace('-', '')
        cliente = Cliente.find_by_cpf(cpf_limpo)
        
        if not cliente:
            return jsonify({'message': 'Cliente não encontrado'}), 404
        
        # Buscar veterinário logado
        usuario_id = request.user['user_id']
        vet = Veterinario.find_by_usuario_id(usuario_id)
        
        if not vet:
            return jsonify({'message': 'Veterinário não encontrado'}), 404
        
        # Criar consulta
        consulta_id = Consulta.create(
            data_consulta=data['data_agendamento'],
            valor=data['valor'],
            id_pet=cliente['ID_PET'],
            crmv=vet['CRMV']
        )
        
        return jsonify({
            'message': f'Agendamento criado com sucesso',
            'consulta_id': consulta_id,
            'data': data['data_agendamento'],
            'pet': cliente['NOME_PET'],
            'cliente': cliente['NOME_COMPLETO']
        }), 201
        
    except Error as e:
        logger.error(f"Erro ao criar agendamento: {e}")
        return jsonify({'message': f'Erro ao criar agendamento: {str(e)}'}), 500

@app.route('/consultas_dia/<data_consulta>', methods=['GET'])
@require_vet
def consultas_do_dia(data_consulta):
    """Listar consultas do dia (usa PROCEDURE listar_consultas)"""
    try:
        # Chamar a procedure
        consultas = Database.call_procedure('listar_consultas', (data_consulta,))
        
        return jsonify({
            'data': data_consulta,
            'total': len(consultas),
            'consultas': consultas
        }), 200
        
    except Error as e:
        logger.error(f"Erro ao listar consultas do dia: {e}")
        return jsonify({'message': 'Erro ao listar consultas do dia'}), 500

@app.route('/vacinas', methods=['POST'])
@require_vet
def criar_vacina():
    """Registrar nova vacina (Veterinário)"""
    try:
        data = request.get_json()
        
        # Validar campos
        campos_obrigatorios = ['nome_vacina', 'dose', 'data_aplicacao']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'message': f'Campo {campo} é obrigatório'}), 400
        
        # Criar vacina
        vacina_id = Vacina.create(
            nome=data['nome_vacina'],
            dose=data['dose'],
            data_aplicado=data['data_aplicacao']
        )
        
        # Se foi informado o pet_id, vincular a vacina ao pet
        if data.get('pet_id'):
            Pet.add_vacina(data['pet_id'], vacina_id)
        
        return jsonify({
            'message': 'Vacina registrada com sucesso',
            'vacina_id': vacina_id
        }), 201
        
    except Error as e:
        logger.error(f"Erro ao criar vacina: {e}")
        return jsonify({'message': f'Erro ao criar vacina: {str(e)}'}), 500

@app.route('/vacinas/<int:vacina_id>', methods=['GET'])
@token_required
def detalhes_vacina(vacina_id):
    """Ver detalhes de uma vacina específica"""
    try:
        vacina = Vacina.find_by_id(vacina_id)
        
        if not vacina:
            return jsonify({'message': 'Vacina não encontrada'}), 404
        
        return jsonify(vacina), 200
        
    except Error as e:
        logger.error(f"Erro ao buscar vacina: {e}")
        return jsonify({'message': 'Erro ao buscar vacina'}), 500

@app.route('/vacinas/<int:vacina_id>', methods=['PUT'])
@require_vet
def atualizar_vacina(vacina_id):
    """Atualizar registro de vacina (Veterinário)"""
    try:
        data = request.get_json()
        
        # Remover campos que não devem ser atualizados
        data.pop('ID_VAC', None)
        
        if not data:
            return jsonify({'message': 'Nenhum dado para atualizar'}), 400
        
        Vacina.update(vacina_id, data)
        
        return jsonify({
            'message': 'Vacina atualizada com sucesso'
        }), 200
        
    except Error as e:
        logger.error(f"Erro ao atualizar vacina: {e}")
        return jsonify({'message': 'Erro ao atualizar vacina'}), 500

@app.route('/vacinas/<int:vacina_id>', methods=['DELETE'])
@require_vet
def deletar_vacina(vacina_id):
    """Deletar registro de vacina (Veterinário)"""
    try:
        Vacina.delete(vacina_id)
        
        return jsonify({
            'message': f'Vacina {vacina_id} removida com sucesso'
        }), 200
        
    except Error as e:
        logger.error(f"Erro ao deletar vacina: {e}")
        return jsonify({'message': 'Erro ao deletar vacina'}), 500

# ========== ROTAS DE PRESCRIÇÃO (Mantidas como estavam - podem ser expandidas depois) ==========

@app.route('/prescricoes', methods=['POST'])
@require_vet
def criar_prescricao():
    """Criar prescrição médica (Veterinário)"""
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['cpf_cliente', 'veterinario', 'data_consulta', 'diagnostico', 'medicamentos']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
        
        if not data.get('medicamentos') or len(data.get('medicamentos')) == 0:
            return jsonify({'error': 'É necessário prescrever pelo menos 1 medicamento'}), 400
        
        # Buscar cliente por CPF para pegar o ID do pet
        cpf_limpo = data['cpf_cliente'].replace('.', '').replace('-', '')
        cliente = Cliente.find_by_cpf(cpf_limpo)
        
        if not cliente:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Adicionar id_pet aos dados
        data['id_pet'] = cliente['ID_PET']
        data['veterinario_id'] = request.user.get('user_id')
        
        # Salvar prescrição
        prescricao = PrescricaoStorage.criar_prescricao(data)
        
        return jsonify({
            'message': 'Prescrição criada com sucesso',
            'prescricao': prescricao
        }), 201
        
    except Error as e:
        logger.error(f"Erro ao criar prescrição: {e}")
        return jsonify({'error': f'Erro ao criar prescrição: {str(e)}'}), 500

@app.route('/historico/<int:pet_id>/prescricoes', methods=['GET'])
@token_required
def listar_prescricoes_pet(pet_id):
    """Ver prescrições médicas do pet"""
    try:
        prescricoes_raw = PrescricaoStorage.listar_por_pet(pet_id)
        
        prescricoes_formatadas = []
        for p in prescricoes_raw:
            prescricoes_formatadas.append({
                'id': p['id'],
                'diagnostico': p['diagnostico'],
                'veterinario': p['veterinario'],
                'data_consulta': p['data_consulta'],
                'status': p['status'],
                'medicamentos_count': len(p.get('medicamentos', [])),
                'orientacoes_gerais': p.get('orientacoes_gerais', '')
            })
        
        return jsonify({
            'pet_id': pet_id,
            'total_prescricoes': len(prescricoes_formatadas),
            'prescricoes': prescricoes_formatadas
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar prescrições: {e}")
        return jsonify({'message': 'Erro ao listar prescrições'}), 500

@app.route('/prescricoes/<int:prescricao_id>', methods=['GET'])
@token_required
def detalhes_prescricao(prescricao_id):
    """Ver detalhes de uma prescrição"""
    try:
        prescricao = PrescricaoStorage.buscar_por_id(prescricao_id)
        
        if not prescricao:
            return jsonify({'message': 'Prescrição não encontrada'}), 404
        
        return jsonify(prescricao), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar prescrição: {e}")
        return jsonify({'message': 'Erro ao buscar prescrição'}), 500

@app.route('/prescricoes/<int:prescricao_id>', methods=['PUT'])
@require_vet
def atualizar_prescricao(prescricao_id):
    """Atualizar prescrição (Veterinário)"""
    return jsonify({'message': 'Funcionalidade será implementada futuramente'}), 200

@app.route('/prescricoes/<int:prescricao_id>/finalizar', methods=['PATCH'])
@require_vet
def finalizar_prescricao(prescricao_id):
    """Finalizar prescrição (Veterinário)"""
    return jsonify({'message': 'Funcionalidade será implementada futuramente'}), 200

@app.route('/prescricoes/<int:prescricao_id>', methods=['DELETE'])
@require_vet
def deletar_prescricao(prescricao_id):
    """Deletar prescrição (Veterinário)"""
    return jsonify({'message': 'Funcionalidade será implementada futuramente'}), 200

# ========== ROTA DE TESTE ==========

@app.route('/test_db', methods=['GET'])
def test_database():
    """Testar conexão com banco de dados"""
    if Database.test_connection():
        return jsonify({'message': 'Conexão com banco de dados OK'}), 200
    else:
        return jsonify({'message': 'Erro na conexão com banco de dados'}), 500
