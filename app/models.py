# models.py - Estrutura de dados para o sistema

"""
Este arquivo define a estrutura de dados que você usará
quando implementar o banco de dados (SQLite, PostgreSQL, etc.)
"""

# ========== ESTRUTURA DE VACINA ==========

class VacinaModel:
    """
    Modelo de dados para registro de vacinas
    """
    def __init__(self):
        self.estrutura = {
            'id': 'int (auto incremento)',
            'pet_id': 'int (FK - relaciona com a tabela pets)',
            'nome_vacina': 'string (ex: V10, Antirrábica, Gripe Canina)',
            'data_aplicacao': 'date (formato: YYYY-MM-DD)',
            'proxima_dose': 'date (nullable - pode ser None)',
            'lote': 'string (número do lote da vacina)',
            'veterinario': 'string (nome do veterinário responsável)',
            'veterinario_id': 'int (FK - relaciona com tabela de veterinários)',
            'observacoes': 'text (nullable)',
            'reacoes_adversas': 'text (nullable)',
            'criado_em': 'datetime',
            'atualizado_em': 'datetime'
        }

# ========== EXEMPLO DE DADOS MOCKADOS ==========

VACINAS_MOCK = [
    {
        'id': 1,
        'pet_id': 1,
        'nome_vacina': 'V10 (Décupla)',
        'data_aplicacao': '2025-01-15',
        'proxima_dose': '2026-01-15',
        'lote': 'V10-2025-ABC',
        'veterinario': 'Dr. João Silva',
        'veterinario_id': 1,
        'observacoes': 'Primeira dose aplicada com sucesso',
        'reacoes_adversas': 'Nenhuma',
        'criado_em': '2025-01-15T14:30:00',
        'atualizado_em': '2025-01-15T14:30:00'
    },
    {
        'id': 2,
        'pet_id': 1,
        'nome_vacina': 'Antirrábica',
        'data_aplicacao': '2025-03-20',
        'proxima_dose': '2026-03-20',
        'lote': 'RAB-2025-XYZ',
        'veterinario': 'Dra. Maria Santos',
        'veterinario_id': 2,
        'observacoes': 'Reforço anual',
        'reacoes_adversas': 'Leve sonolência por 2 horas',
        'criado_em': '2025-03-20T10:15:00',
        'atualizado_em': '2025-03-20T10:15:00'
    },
    {
        'id': 3,
        'pet_id': 1,
        'nome_vacina': 'Gripe Canina',
        'data_aplicacao': '2025-06-10',
        'proxima_dose': '2025-12-10',
        'lote': 'GRIPE-2025-789',
        'veterinario': 'Dr. João Silva',
        'veterinario_id': 1,
        'observacoes': 'Dose preventiva antes do inverno',
        'reacoes_adversas': 'Nenhuma',
        'criado_em': '2025-06-10T16:45:00',
        'atualizado_em': '2025-06-10T16:45:00'
    }
]

# ========== TIPOS DE VACINAS COMUNS ==========

TIPOS_VACINAS = [
    'V10 (Décupla)',
    'V8 (Óctupla)',
    'Antirrábica',
    'Gripe Canina (Tosse dos Canis)',
    'Giardíase',
    'Leishmaniose',
    'V4 (Quádrupla Felina)',
    'V5 (Quíntupla Felina)',
    'Antirrábica Felina',
    'FeLV (Leucemia Felina)',
]
