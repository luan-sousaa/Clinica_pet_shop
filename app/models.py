"""
Models - Classes de modelo para as tabelas do banco de dados petCare
"""

from app.database import Database, gerar_uuid, find_by_id, find_all, insert_and_get_id, update_by_id, delete_by_id
from datetime import datetime

# ========== GRUPO_USUARIO ==========

class GrupoUsuario:
    """Modelo para tabela GRUPO_USUARIO"""
    
    TIPO_ADMIN = 'Administrador'
    TIPO_VET = 'Veterinario'
    TIPO_CLIENTE = 'Cliente'
    
    @staticmethod
    def find_by_tipo(tipo_acesso):
        """Busca grupo de usuário por tipo"""
        query = "SELECT * FROM GRUPO_USUARIO WHERE TIPO_ACESSO = %s"
        return Database.execute_query(query, (tipo_acesso,), fetch_one=True)
    
    @staticmethod
    def get_all():
        """Retorna todos os grupos de usuário"""
        return find_all('GRUPO_USUARIO')

# ========== USUARIO ==========

class Usuario:
    """Modelo para tabela USUARIO"""
    
    @staticmethod
    def create(nome_completo, email, senha, grupo_usuario_id):
        """
        Cria um novo usuário
        O trigger hash_senha automaticamente faz o hash da senha
        """
        usuario_id = gerar_uuid()
        query = """
            INSERT INTO USUARIO (ID_USUARIO, NOME_COMPLETO, EMAIL, SENHA, GRUPO_USUARIO)
            VALUES (%s, %s, %s, %s, %s)
        """
        Database.execute_query(query, (usuario_id, nome_completo, email, senha, grupo_usuario_id), commit=True)
        return usuario_id
    
    @staticmethod
    def find_by_email(email):
        """Busca usuário por email (usa index USUARIO_EMAIL)"""
        query = """
            SELECT U.*, G.TIPO_ACESSO, G.ROLE_MYSQL
            FROM USUARIO U
            INNER JOIN GRUPO_USUARIO G ON U.GRUPO_USUARIO = G.ID_ACESSO
            WHERE U.EMAIL = %s
        """
        return Database.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def find_by_id(usuario_id):
        """Busca usuário por ID"""
        query = """
            SELECT U.*, G.TIPO_ACESSO, G.ROLE_MYSQL
            FROM USUARIO U
            INNER JOIN GRUPO_USUARIO G ON U.GRUPO_USUARIO = G.ID_ACESSO
            WHERE U.ID_USUARIO = %s
        """
        return Database.execute_query(query, (usuario_id,), fetch_one=True)
    
    @staticmethod
    def authenticate(email, senha):
        """
        Autentica usuário comparando senha com hash SHA256
        """
        query = """
            SELECT U.*, G.TIPO_ACESSO, G.ROLE_MYSQL
            FROM USUARIO U
            INNER JOIN GRUPO_USUARIO G ON U.GRUPO_USUARIO = G.ID_ACESSO
            WHERE U.EMAIL = %s AND U.SENHA = SHA2(%s, 256)
        """
        return Database.execute_query(query, (email, senha), fetch_one=True)
    
    @staticmethod
    def update_password(email, nova_senha):
        """
        Atualiza senha do usuário
        O trigger hash_atualiza automaticamente faz o hash da nova senha
        """
        query = "UPDATE USUARIO SET SENHA = %s WHERE EMAIL = %s"
        return Database.execute_query(query, (nova_senha, email), commit=True)
    
    @staticmethod
    def exists(email):
        """Verifica se email já está cadastrado"""
        query = "SELECT COUNT(*) as count FROM USUARIO WHERE EMAIL = %s"
        result = Database.execute_query(query, (email,), fetch_one=True)
        return result['count'] > 0

# ========== PET ==========

class Pet:
    """Modelo para tabela PET"""
    
    @staticmethod
    def create(nome, raca, idade, observacoes=None):
        """Cria um novo pet"""
        query = """
            INSERT INTO PET (NOME, RACA, IDADE, OBSERVACOES)
            VALUES (%s, %s, %s, %s)
        """
        result = Database.execute_query(query, (nome, raca, idade, observacoes), commit=True)
        return result['last_insert_id']
    
    @staticmethod
    def find_by_id(pet_id):
        """Busca pet por ID"""
        return find_by_id('PET', 'ID_PET', pet_id)
    
    @staticmethod
    def update(pet_id, data):
        """Atualiza dados do pet"""
        return update_by_id('PET', 'ID_PET', pet_id, data)
    
    @staticmethod
    def get_info_with_owner(pet_id):
        """Usa a VIEW INFO_PET para obter informações do pet com tutor"""
        query = """
            SELECT P.*, U.NOME_COMPLETO as NOME_TUTOR
            FROM PET P
            INNER JOIN CLIENTE C ON P.ID_PET = C.ID_PET
            INNER JOIN USUARIO U ON C.ID_USUARIO = U.ID_USUARIO
            WHERE P.ID_PET = %s
        """
        return Database.execute_query(query, (pet_id,), fetch_one=True)
    
    @staticmethod
    def add_vacina(pet_id, vacina_id):
        """Adiciona vacina ao pet"""
        query = "UPDATE PET SET ID_VACINAS = %s WHERE ID_PET = %s"
        return Database.execute_query(query, (vacina_id, pet_id), commit=True)

# ========== CLIENTE ==========

class Cliente:
    """Modelo para tabela CLIENTE"""
    
    @staticmethod
    def create(usuario_id, telefone, cpf, id_pet, bairro=None, rua=None, cidade=None):
        """Cria um novo cliente"""
        query = """
            INSERT INTO CLIENTE (ID_USUARIO, TELEFONE, CPF, ID_PET, BAIRRO, RUA, CIDADE)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        Database.execute_query(query, (usuario_id, telefone, cpf, id_pet, bairro, rua, cidade), commit=True)
        return usuario_id
    
    @staticmethod
    def find_by_id(usuario_id):
        """Busca cliente por ID"""
        return find_by_id('CLIENTE', 'ID_USUARIO', usuario_id)
    
    @staticmethod
    def find_by_cpf(cpf):
        """Busca cliente por CPF"""
        query = """
            SELECT C.*, U.NOME_COMPLETO, U.EMAIL, P.NOME as NOME_PET
            FROM CLIENTE C
            INNER JOIN USUARIO U ON C.ID_USUARIO = U.ID_USUARIO
            LEFT JOIN PET P ON C.ID_PET = P.ID_PET
            WHERE C.CPF = %s
        """
        return Database.execute_query(query, (cpf,), fetch_one=True)
    
    @staticmethod
    def get_pet(usuario_id):
        """Retorna o pet do cliente"""
        query = """
            SELECT P.*
            FROM PET P
            INNER JOIN CLIENTE C ON P.ID_PET = C.ID_PET
            WHERE C.ID_USUARIO = %s
        """
        return Database.execute_query(query, (usuario_id,), fetch_one=True)
    
    @staticmethod
    def update(usuario_id, data):
        """Atualiza dados do cliente"""
        return update_by_id('CLIENTE', 'ID_USUARIO', usuario_id, data)

# ========== VETERINARIO ==========

class Veterinario:
    """Modelo para tabela VETERINARIO"""
    
    @staticmethod
    def create(crmv, usuario_id, salario=None, turno=None):
        """Cria um novo veterinário"""
        query = """
            INSERT INTO VETERINARIO (CRMV, ID_USUARIO, SALARIO, TURNO)
            VALUES (%s, %s, %s, %s)
        """
        Database.execute_query(query, (crmv, usuario_id, salario, turno), commit=True)
        return crmv
    
    @staticmethod
    def find_by_crmv(crmv):
        """Busca veterinário por CRMV"""
        query = """
            SELECT V.*, U.NOME_COMPLETO, U.EMAIL
            FROM VETERINARIO V
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
            WHERE V.CRMV = %s
        """
        return Database.execute_query(query, (crmv,), fetch_one=True)
    
    @staticmethod
    def find_by_usuario_id(usuario_id):
        """Busca veterinário por ID do usuário"""
        query = """
            SELECT V.*, U.NOME_COMPLETO, U.EMAIL
            FROM VETERINARIO V
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
            WHERE V.ID_USUARIO = %s
        """
        return Database.execute_query(query, (usuario_id,), fetch_one=True)
    
    @staticmethod
    def listar_consultas_dia(crmv, data_consulta):
        """
        Usa a PROCEDURE listar_consultas para obter consultas do dia
        """
        return Database.call_procedure('listar_consultas', (data_consulta,))
    
    @staticmethod
    def get_all():
        """Lista todos os veterinários"""
        query = """
            SELECT V.*, U.NOME_COMPLETO, U.EMAIL
            FROM VETERINARIO V
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
        """
        return Database.execute_query(query, fetch_all=True)

# ========== VACINAS ==========

class Vacina:
    """Modelo para tabela VACINAS"""
    
    @staticmethod
    def create(nome, dose, data_aplicado):
        """Cria um novo registro de vacina"""
        query = """
            INSERT INTO VACINAS (NOME, DOSE, DATA_APLICADO)
            VALUES (%s, %s, %s)
        """
        result = Database.execute_query(query, (nome, dose, data_aplicado), commit=True)
        return result['last_insert_id']
    
    @staticmethod
    def find_by_id(vacina_id):
        """Busca vacina por ID"""
        return find_by_id('VACINAS', 'ID_VAC', vacina_id)
    
    @staticmethod
    def get_historico_pet(pet_id):
        """
        Usa a VIEW HISTORICO_VACINA para obter histórico de vacinas do pet
        """
        query = """
            SELECT V.NOME, V.DOSE, V.DATA_APLICADO
            FROM VACINAS V
            INNER JOIN PET P ON V.ID_VAC = P.ID_VACINAS
            WHERE P.ID_PET = %s
            ORDER BY V.DATA_APLICADO DESC
        """
        return Database.execute_query(query, (pet_id,), fetch_all=True)
    
    @staticmethod
    def update(vacina_id, data):
        """Atualiza dados da vacina"""
        return update_by_id('VACINAS', 'ID_VAC', vacina_id, data)
    
    @staticmethod
    def delete(vacina_id):
        """Deleta vacina"""
        return delete_by_id('VACINAS', 'ID_VAC', vacina_id)

# ========== CONSULTA ==========

class Consulta:
    """Modelo para tabela CONSULTA"""
    
    @staticmethod
    def create(data_consulta, valor, id_pet, crmv):
        """Cria uma nova consulta"""
        consulta_id = gerar_uuid()
        query = """
            INSERT INTO CONSULTA (ID_PROCEDIMENTO, DATA_CONSULTA, VALOR, ID_PET, CRMV)
            VALUES (%s, %s, %s, %s, %s)
        """
        Database.execute_query(query, (consulta_id, data_consulta, valor, id_pet, crmv), commit=True)
        return consulta_id
    
    @staticmethod
    def find_by_id(consulta_id):
        """Busca consulta por ID"""
        query = """
            SELECT C.*, P.NOME as NOME_PET, P.RACA, V.*, U.NOME_COMPLETO as NOME_VET
            FROM CONSULTA C
            INNER JOIN PET P ON C.ID_PET = P.ID_PET
            INNER JOIN VETERINARIO V ON C.CRMV = V.CRMV
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
            WHERE C.ID_PROCEDIMENTO = %s
        """
        return Database.execute_query(query, (consulta_id,), fetch_one=True)
    
    @staticmethod
    def find_by_pet(pet_id):
        """Lista consultas de um pet (usa index DATA_CONSULTA)"""
        query = """
            SELECT C.*, U.NOME_COMPLETO as NOME_VET, V.CRMV
            FROM CONSULTA C
            INNER JOIN VETERINARIO V ON C.CRMV = V.CRMV
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
            WHERE C.ID_PET = %s
            ORDER BY C.DATA_CONSULTA DESC
        """
        return Database.execute_query(query, (pet_id,), fetch_all=True)
    
    @staticmethod
    def find_by_data(data_consulta):
        """Lista consultas de uma data específica (usa index DATA_CONSULTA)"""
        query = """
            SELECT C.*, P.NOME as NOME_PET, P.RACA, U.NOME_COMPLETO as NOME_VET
            FROM CONSULTA C
            INNER JOIN PET P ON C.ID_PET = P.ID_PET
            INNER JOIN VETERINARIO V ON C.CRMV = V.CRMV
            INNER JOIN USUARIO U ON V.ID_USUARIO = U.ID_USUARIO
            WHERE C.DATA_CONSULTA = %s
            ORDER BY C.DATA_CONSULTA
        """
        return Database.execute_query(query, (data_consulta,), fetch_all=True)
    
    @staticmethod
    def update(consulta_id, data):
        """Atualiza consulta"""
        return update_by_id('CONSULTA', 'ID_PROCEDIMENTO', consulta_id, data)
    
    @staticmethod
    def delete(consulta_id):
        """Deleta consulta"""
        return delete_by_id('CONSULTA', 'ID_PROCEDIMENTO', consulta_id)

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
