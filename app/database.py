import mysql.connector
from mysql.connector import Error, pooling
from app.config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """Classe para gerenciar conexões com o banco de dados MySQL"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Inicializa o pool de conexões"""
        try:
            if cls._connection_pool is None:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name=Config.POOL_NAME,
                    pool_size=Config.POOL_SIZE,
                    pool_reset_session=Config.POOL_RESET_SESSION,
                    **Config.get_db_config()
                )
                logger.info("Pool de conexões MySQL criado com sucesso")
        except Error as e:
            logger.error(f"Erro ao criar pool de conexões MySQL: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Obtém uma conexão do pool"""
        try:
            if cls._connection_pool is None:
                cls.initialize_pool()
            return cls._connection_pool.get_connection()
        except Error as e:
            logger.error(f"Erro ao obter conexão do pool: {e}")
            raise
    
    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """
        Executa uma query no banco de dados
        
        Args:
            query (str): Query SQL a ser executada
            params (tuple): Parâmetros da query
            fetch_one (bool): Se True, retorna apenas um resultado
            fetch_all (bool): Se True, retorna todos os resultados
            commit (bool): Se True, faz commit da transação
        
        Returns:
            dict: Resultado da query ou None
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if commit:
                connection.commit()
                return {'affected_rows': cursor.rowcount, 'last_insert_id': cursor.lastrowid}
            
            if fetch_one:
                result = cursor.fetchone()
                return result
            
            if fetch_all:
                results = cursor.fetchall()
                return results
            
            return {'affected_rows': cursor.rowcount}
            
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Erro ao executar consulta SQL: {e}")
            logger.error(f"Consulta: {query}")
            logger.error(f"Parâmetros: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def execute_many(cls, query, params_list):
        """
        Executa múltiplas queries com diferentes parâmetros
        
        Args:
            query (str): Query SQL a ser executada
            params_list (list): Lista de tuplas com parâmetros
        
        Returns:
            dict: Informações sobre a execução
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            
            cursor.executemany(query, params_list)
            connection.commit()
            
            return {'affected_rows': cursor.rowcount}
            
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Erro ao executar múltiplas consultas: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def call_procedure(cls, procedure_name, args=None):
        """
        Chama uma stored procedure
        
        Args:
            procedure_name (str): Nome da procedure
            args (tuple): Argumentos da procedure
        
        Returns:
            list: Resultados da procedure
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if args:
                cursor.callproc(procedure_name, args)
            else:
                cursor.callproc(procedure_name)
            
            # Recuperar todos os result sets
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            return results
            
        except Error as e:
            logger.error(f"Erro ao chamar procedimento armazenado {procedure_name}: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def execute_transaction(cls, queries):
        """
        Executa múltiplas queries em uma transação
        
        Args:
            queries (list): Lista de dicts com 'query' e 'params'
        
        Returns:
            bool: True se a transação foi bem-sucedida
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Iniciar transação
            connection.start_transaction()
            
            results = []
            for query_info in queries:
                query = query_info['query']
                params = query_info.get('params')
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results.append({
                    'affected_rows': cursor.rowcount,
                    'last_insert_id': cursor.lastrowid
                })
            
            # Commit da transação
            connection.commit()
            return {'success': True, 'results': results}
            
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Erro na transação: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def test_connection(cls):
        """Testa a conexão com o banco de dados"""
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            logger.info("Conexão com banco de dados testada com sucesso")
            return True
        except Error as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False

# Função auxiliar para gerar UUID (usar a function do MySQL)
def gerar_uuid():
    """Retorna UUID gerado pela function do MySQL"""
    result = Database.execute_query("SELECT gera_id_dados_criticos() as uuid", fetch_one=True)
    return result['uuid'] if result else None

# Funções auxiliares para queries comuns
def insert_and_get_id(table, data):
    """Insere dados e retorna o ID inserido"""
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    result = Database.execute_query(query, tuple(data.values()), commit=True)
    return result['last_insert_id']

def update_by_id(table, id_column, id_value, data):
    """Atualiza registro por ID"""
    set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
    params = tuple(data.values()) + (id_value,)
    
    return Database.execute_query(query, params, commit=True)

def delete_by_id(table, id_column, id_value):
    """Deleta registro por ID"""
    query = f"DELETE FROM {table} WHERE {id_column} = %s"
    return Database.execute_query(query, (id_value,), commit=True)

def find_by_id(table, id_column, id_value):
    """Busca registro por ID"""
    query = f"SELECT * FROM {table} WHERE {id_column} = %s"
    return Database.execute_query(query, (id_value,), fetch_one=True)

def find_all(table, conditions=None, order_by=None, limit=None):
    """Busca todos os registros com filtros opcionais"""
    query = f"SELECT * FROM {table}"
    params = []
    
    if conditions:
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query += f" WHERE {where_clause}"
        params = list(conditions.values())
    
    if order_by:
        query += f" ORDER BY {order_by}"
    
    if limit:
        query += f" LIMIT {limit}"
    
    return Database.execute_query(query, tuple(params) if params else None, fetch_all=True)
