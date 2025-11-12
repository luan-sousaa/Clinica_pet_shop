from flask import render_template, request, jsonify, current_app as app

@app.route('/')
def index():
    return render_template('index.html')

# Adicione mais rotas conforme necessário
@app.route('/login', methods=['POST'])
def login():
    #logica login
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    # Lógica de autenticação aqui
    if email == 'admin@gmail.com' and senha == '1234':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
#cadastro de usuario e pet
@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome_tutor = data.get('nome_tutor')
    email = data.get('email')
    senha = data.get('senha')
    confirmar_senha = data.get('confirmar_senha')
    nome_pet = data.get('nome_pet')
    raca_pet = data.get('raca_pet')
    idadade_pet = data.get('idade_pet')
    observacoes_pet = data.get('observacoes_pet')
    if senha != confirmar_senha:
        return jsonify({'message': 'Senhas não coincidem'}), 400
    # Lógica de cadastro aqui
    return jsonify({'message': f'User {nome_tutor} registered successfully'}), 201

#esqueceu a senha
@app.route('/esqueceu_senha', methods=['POST'])
def esqueceu_senha():
    data = request.get_json()
    email = data.get('email')
    nova_senha = data.get('nova_senha')
    confirmar_nova_senha = data.get('confirmar_nova_senha')
    if nova_senha != confirmar_nova_senha:
        return jsonify({'message': 'Senhas não coincidem'}), 400
    # Lógica para redefinir a senha aqui
    return jsonify({'message': f'Senha redefinida para {email} com sucesso'}), 200

#tela cliente dados do pet
@app.route('/dados_pet', methods=['GET'])
def dados_pet():
    # Lógica para obter dados do pet aqui
    pet_data = {
        'nome_pet': 'Rex',
        'raca_pet': 'Labrador',
        'idade_pet': 5,
        'observacoes_pet': 'Nenhuma',
        'servicos_agendados': [
            {'servico': 'Banho', 'data': '2024-07-01', 'hora': '10:00'},
            {'servico': 'Tosa', 'data': '2024-07-15', 'hora': '14:00'}
        ]
    }
    return jsonify(pet_data), 200

#tela criar agendamentos
@app.route('/agendamentos', methods=['POST'])
def agendamentos():
    data = request.get_json()
    servico = data.get('servico')
    data_agendamento = data.get('data_agendamento')
    hora_agendamento = data.get('hora_agendamento')
    # Lógica para criar agendamento aqui
    return jsonify({'message': f'Agendamento para {servico} em {data_agendamento} às {hora_agendamento} criado com sucesso'}), 201

# MÉDICO: Registrar nova vacina
@app.route('/vacinas', methods=['POST'])
def criar_vacina():
    """
    Rota para médico veterinário registrar uma nova vacina
    Body JSON:
    {
        "pet_id": 1,
        "nome_vacina": "V10",
        "data_aplicacao": "2025-11-11",
        "proxima_dose": "2026-11-11",
        "lote": "ABC123",
        "veterinario": "Dr. João Silva",
        "observacoes": "Aplicação normal"
    }
    """
    data = request.get_json()
    
    # Validações básicas
    campos_obrigatorios = ['pet_id', 'nome_vacina', 'data_aplicacao', 'veterinario']
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
    
    # Aqui você salvaria no banco de dados
    vacina = {
        'id': 1,  # ID gerado pelo banco
        'pet_id': data.get('pet_id'),
        'nome_vacina': data.get('nome_vacina'),
        'data_aplicacao': data.get('data_aplicacao'),
        'proxima_dose': data.get('proxima_dose'),
        'lote': data.get('lote'),
        'veterinario': data.get('veterinario'),
        'observacoes': data.get('observacoes', ''),
        'criado_em': '2025-11-11T10:00:00'
    }
    
    return jsonify({
        'message': 'Vacina registrada com sucesso',
        'vacina': vacina
    }), 201

# CLIENTE: Ver histórico de vacinas do pet
@app.route('/historico/<int:pet_id>/vacinas', methods=['GET'])
def listar_vacinas_pet(pet_id):
    """
    Rota para cliente ver o histórico de vacinas do seu pet
    """
    # Exemplo de dados mockados:
    vacinas = [
        {
            'id': 1,
            'nome_vacina': 'V10',
            'data_aplicacao': '2025-01-15',
            'proxima_dose': '2026-01-15',
            'lote': 'ABC123',
            'veterinario': 'Dr. João Silva',
            'observacoes': 'Aplicação normal'
        },
        {
            'id': 2,
            'nome_vacina': 'Antirrábica',
            'data_aplicacao': '2025-03-20',
            'proxima_dose': '2026-03-20',
            'lote': 'XYZ789',
            'veterinario': 'Dra. Maria Santos',
            'observacoes': 'Pet apresentou leve sonolência'
        }
    ]
    
    return jsonify({
        'pet_id': pet_id,
        'total_vacinas': len(vacinas),
        'vacinas': vacinas
    }), 200

# CLIENTE/MÉDICO: Ver detalhes de uma vacina específica
@app.route('/vacinas/<int:vacina_id>', methods=['GET'])
def detalhes_vacina(vacina_id):
    """
    Rota para ver detalhes de uma vacina específica
    """
    # Aqui você buscaria no banco de dados
    vacina = {
        'id': vacina_id,
        'pet_id': 1,
        'nome_pet': 'Rex',
        'nome_vacina': 'V10',
        'data_aplicacao': '2025-01-15',
        'proxima_dose': '2026-01-15',
        'lote': 'ABC123',
        'veterinario': 'Dr. João Silva',
        'observacoes': 'Aplicação normal',
        'reacoes_adversas': 'Nenhuma',
        'criado_em': '2025-01-15T14:30:00'
    }
    
    return jsonify(vacina), 200

# MÉDICO: Atualizar registro de vacina
@app.route('/vacinas/<int:vacina_id>', methods=['PUT'])
def atualizar_vacina(vacina_id):
    """
    Rota para médico atualizar informações de uma vacina
    """
    data = request.get_json()
    
    # Aqui você atualizaria no banco de dados
    vacina_atualizada = {
        'id': vacina_id,
        'nome_vacina': data.get('nome_vacina'),
        'data_aplicacao': data.get('data_aplicacao'),
        'proxima_dose': data.get('proxima_dose'),
        'lote': data.get('lote'),
        'observacoes': data.get('observacoes'),
        'atualizado_em': '2025-11-11T10:30:00'
    }
    
    return jsonify({
        'message': 'Vacina atualizada com sucesso',
        'vacina': vacina_atualizada
    }), 200

# MÉDICO: Deletar registro de vacina
@app.route('/vacinas/<int:vacina_id>', methods=['DELETE'])
def deletar_vacina(vacina_id):
    """
    Rota para médico remover um registro de vacina (caso tenha sido cadastrado por engano)
    """
    # Aqui você deletaria do banco de dados
    
    return jsonify({
        'message': f'Vacina {vacina_id} removida com sucesso'
    }), 200

# MÉDICO: Criar prescrição médica
@app.route('/prescricoes', methods=['POST'])
def criar_prescricao():
    """
    Rota para veterinário criar uma prescrição médica
    Body JSON:
    {
        "pet_id": 1,
        "veterinario": "Dr. João Silva",
        "veterinario_id": 1,
        "data_consulta": "2025-11-11",
        "diagnostico": "Infecção de ouvido",
        "medicamentos": [
            {
                "nome": "Antibiótico XYZ",
                "dosagem": "1 comprimido",
                "frequencia": "2x ao dia",
                "duracao": "7 dias",
                "observacoes": "Administrar com alimento"
            }
        ],
        "orientacoes_gerais": "Manter o pet em repouso",
        "retorno": "2025-11-18"
    }
    """
    data = request.get_json()
    
    # Validações básicas
    campos_obrigatorios = ['pet_id', 'veterinario', 'data_consulta', 'diagnostico', 'medicamentos']
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
    
    # Validar se há pelo menos 1 medicamento
    if not data.get('medicamentos') or len(data.get('medicamentos')) == 0:
        return jsonify({'error': 'É necessário prescrever pelo menos 1 medicamento'}), 400
    
    # Aqui você salvaria no banco de dados
    prescricao = {
        'id': 1,  # ID gerado pelo banco
        'pet_id': data.get('pet_id'),
        'veterinario': data.get('veterinario'),
        'veterinario_id': data.get('veterinario_id'),
        'data_consulta': data.get('data_consulta'),
        'diagnostico': data.get('diagnostico'),
        'medicamentos': data.get('medicamentos'),
        'orientacoes_gerais': data.get('orientacoes_gerais', ''),
        'retorno': data.get('retorno'),
        'criado_em': '2025-11-11T10:00:00'
    }
    
    return jsonify({
        'message': 'Prescrição criada com sucesso',
        'prescricao': prescricao
    }), 201

# CLIENTE: Ver prescrições do pet
@app.route('/historico/<int:pet_id>/prescricoes', methods=['GET'])
def listar_prescricoes_pet(pet_id):
    """
    Rota para cliente ver as prescrições médicas do seu pet
    """
    # Exemplo de dados mockados:
    prescricoes = [
        {
            'id': 1,
            'data_consulta': '2025-11-11',
            'veterinario': 'Dr. João Silva',
            'diagnostico': 'Infecção de ouvido',
            'status': 'ativa',
            'medicamentos_count': 2
        },
        {
            'id': 2,
            'data_consulta': '2025-10-15',
            'veterinario': 'Dra. Maria Santos',
            'diagnostico': 'Alergia alimentar',
            'status': 'concluída',
            'medicamentos_count': 1
        }
    ]
    
    return jsonify({
        'pet_id': pet_id,
        'total_prescricoes': len(prescricoes),
        'prescricoes': prescricoes
    }), 200

# CLIENTE/MÉDICO: Ver detalhes de uma prescrição
@app.route('/prescricoes/<int:prescricao_id>', methods=['GET'])
def detalhes_prescricao(prescricao_id):
    """
    Rota para ver detalhes completos de uma prescrição
    """
    # Aqui você buscaria no banco de dados
    prescricao = {
        'id': prescricao_id,
        'pet_id': 1,
        'nome_pet': 'Rex',
        'raca_pet': 'Labrador',
        'idade_pet': 5,
        'veterinario': 'Dr. João Silva',
        'veterinario_id': 1,
        'crm_vet': '12345-SP',
        'data_consulta': '2025-11-11',
        'diagnostico': 'Infecção de ouvido (Otite externa)',
        'medicamentos': [
            {
                'nome': 'Antibiótico Otomax',
                'dosagem': '5 gotas',
                'frequencia': '2x ao dia (manhã e noite)',
                'duracao': '7 dias',
                'observacoes': 'Aplicar diretamente no ouvido após limpeza',
                'via_administracao': 'Tópica'
            },
            {
                'nome': 'Anti-inflamatório Prednisolona',
                'dosagem': '1 comprimido de 5mg',
                'frequencia': '1x ao dia',
                'duracao': '5 dias',
                'observacoes': 'Administrar com alimento',
                'via_administracao': 'Oral'
            }
        ],
        'orientacoes_gerais': 'Manter o pet em repouso. Não permitir que coce a orelha. Retornar se os sintomas piorarem.',
        'retorno': '2025-11-18',
        'status': 'ativa',
        'criado_em': '2025-11-11T10:00:00'
    }
    
    return jsonify(prescricao), 200

# MÉDICO: Atualizar prescrição
@app.route('/prescricoes/<int:prescricao_id>', methods=['PUT'])
def atualizar_prescricao(prescricao_id):
    """
    Rota para médico atualizar uma prescrição (ex: adicionar medicamento, alterar orientações)
    """
    data = request.get_json()
    
    # Aqui você atualizaria no banco de dados
    prescricao_atualizada = {
        'id': prescricao_id,
        'diagnostico': data.get('diagnostico'),
        'medicamentos': data.get('medicamentos'),
        'orientacoes_gerais': data.get('orientacoes_gerais'),
        'retorno': data.get('retorno'),
        'atualizado_em': '2025-11-11T11:00:00'
    }
    
    return jsonify({
        'message': 'Prescrição atualizada com sucesso',
        'prescricao': prescricao_atualizada
    }), 200

# MÉDICO: Finalizar prescrição (marcar como concluída)
@app.route('/prescricoes/<int:prescricao_id>/finalizar', methods=['PATCH'])
def finalizar_prescricao(prescricao_id):
    """
    Rota para marcar prescrição como concluída
    """
    # Aqui você atualizaria o status no banco de dados
    
    return jsonify({
        'message': f'Prescrição {prescricao_id} marcada como concluída',
        'status': 'concluída',
        'finalizado_em': '2025-11-18T14:00:00'
    }), 200

# MÉDICO: Deletar prescrição
@app.route('/prescricoes/<int:prescricao_id>', methods=['DELETE'])
def deletar_prescricao(prescricao_id):
    """
    Rota para médico remover uma prescrição (caso tenha sido criada por engano)
    """
    # Aqui você deletaria do banco de dados
    
    return jsonify({
        'message': f'Prescrição {prescricao_id} removida com sucesso'
    }), 200