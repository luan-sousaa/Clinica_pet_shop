"""
Sistema de armazenamento temporário para prescrições
Enquanto a tabela PRESCRICAO não é criada no banco de dados
"""
import json
import os
from datetime import datetime

# Usar caminho absoluto baseado no diretório do arquivo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESCRICOES_FILE = os.path.join(BASE_DIR, 'prescricoes.json')

class PrescricaoStorage:
    """Gerencia prescrições em arquivo JSON"""
    
    @staticmethod
    def _load_prescricoes():
        """Carrega prescrições do arquivo"""
        if os.path.exists(PRESCRICOES_FILE):
            try:
                with open(PRESCRICOES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    @staticmethod
    def _save_prescricoes(prescricoes):
        """Salva prescrições no arquivo"""
        with open(PRESCRICOES_FILE, 'w', encoding='utf-8') as f:
            json.dump(prescricoes, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def criar_prescricao(data):
        """Cria uma nova prescrição"""
        prescricoes = PrescricaoStorage._load_prescricoes()
        
        # Gerar ID
        novo_id = max([p.get('id', 0) for p in prescricoes], default=0) + 1
        
        # Criar prescrição
        prescricao = {
            'id': novo_id,
            'cpf_cliente': data.get('cpf_cliente'),
            'id_pet': data.get('id_pet'),
            'veterinario': data.get('veterinario'),
            'veterinario_id': data.get('veterinario_id'),
            'data_consulta': data.get('data_consulta'),
            'diagnostico': data.get('diagnostico'),
            'medicamentos': data.get('medicamentos', []),
            'orientacoes_gerais': data.get('orientacoes_gerais', ''),
            'retorno': data.get('retorno'),
            'status': 'ativa',
            'created_at': datetime.now().isoformat()
        }
        
        prescricoes.append(prescricao)
        PrescricaoStorage._save_prescricoes(prescricoes)
        
        return prescricao
    
    @staticmethod
    def listar_por_pet(id_pet):
        """Lista prescrições de um pet"""
        prescricoes = PrescricaoStorage._load_prescricoes()
        return [p for p in prescricoes if p.get('id_pet') == id_pet]
    
    @staticmethod
    def buscar_por_id(prescricao_id):
        """Busca prescrição por ID"""
        prescricoes = PrescricaoStorage._load_prescricoes()
        for p in prescricoes:
            if p.get('id') == prescricao_id:
                return p
        return None
    
    @staticmethod
    def atualizar_status(prescricao_id, novo_status):
        """Atualiza status da prescrição"""
        prescricoes = PrescricaoStorage._load_prescricoes()
        for p in prescricoes:
            if p.get('id') == prescricao_id:
                p['status'] = novo_status
                PrescricaoStorage._save_prescricoes(prescricoes)
                return p
        return None
