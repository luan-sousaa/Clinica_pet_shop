"""
Script para popular a tabela GRUPO_USUARIO com os tipos de acesso padrão
Execute este script apenas UMA vez após criar o banco de dados
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import Database, gerar_uuid

def popular_grupos_usuario():
    """Insere os grupos de usuário padrão no banco de dados"""
    
    print("🔄 Iniciando população da tabela GRUPO_USUARIO...")
    
    try:
        # Verificar se já existem grupos cadastrados
        query_check = "SELECT COUNT(*) as count FROM GRUPO_USUARIO"
        result = Database.execute_query(query_check, fetch_one=True)
        
        if result and result['count'] > 0:
            print(f"⚠️  Já existem {result['count']} grupos cadastrados no banco.")
            resposta = input("Deseja continuar e adicionar novos grupos? (s/n): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada pelo usuário.")
                return
        
        # Dados dos grupos
        grupos = [
            {
                'id_acesso': gerar_uuid(),
                'role_mysql': 'ADM',
                'tipo_acesso': 'Administrador',
                'descricao': 'Acesso total ao sistema, pode gerenciar usuários e configurações'
            },
            {
                'id_acesso': gerar_uuid(),
                'role_mysql': 'VET',
                'tipo_acesso': 'Veterinario',
                'descricao': 'Acesso para veterinários: criar consultas, vacinas e prescrições'
            },
            {
                'id_acesso': gerar_uuid(),
                'role_mysql': 'CLI',
                'tipo_acesso': 'Cliente',
                'descricao': 'Acesso para clientes: visualizar dados do pet e histórico'
            }
        ]
        
        # Inserir grupos
        query_insert = """
            INSERT INTO GRUPO_USUARIO (ID_ACESSO, ROLE_MYSQL, TIPO_ACESSO, DESCRICAO)
            VALUES (%s, %s, %s, %s)
        """
        
        for grupo in grupos:
            try:
                Database.execute_query(
                    query_insert,
                    (grupo['id_acesso'], grupo['role_mysql'], grupo['tipo_acesso'], grupo['descricao']),
                    commit=True
                )
                print(f"✓ Grupo '{grupo['tipo_acesso']}' criado com sucesso")
            except Exception as e:
                if "Duplicate entry" in str(e):
                    print(f"⚠️  Grupo '{grupo['tipo_acesso']}' já existe")
                else:
                    raise
        
        print("\n✅ População da tabela GRUPO_USUARIO concluída!")
        print("\n📋 Grupos cadastrados:")
        
        # Listar todos os grupos
        query_list = "SELECT * FROM GRUPO_USUARIO"
        grupos_db = Database.execute_query(query_list, fetch_all=True)
        
        for grupo in grupos_db:
            print(f"   - {grupo['TIPO_ACESSO']} (Role: {grupo['ROLE_MYSQL']})")
        
    except Exception as e:
        print(f"\n❌ Erro ao popular tabela GRUPO_USUARIO: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("POPULAÇÃO DA TABELA GRUPO_USUARIO")
    print("=" * 60)
    print()
    
    try:
        Database.initialize_pool()
        if Database.test_connection():
            print("✓ Conexão com banco de dados MySQL estabelecida com sucesso\n")
            popular_grupos_usuario()
        else:
            print("❌ Não foi possível conectar ao banco de dados MySQL")
            print("Verifique as configurações no arquivo .env")
    except Exception as e:
        print(f"❌ Erro ao executar script: {e}")
