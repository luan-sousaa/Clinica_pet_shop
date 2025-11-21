# 📋 Instruções para Configurar o Projeto

## 1. Clonar o Repositório
```bash
git clone https://github.com/luan-sousaa/Clinica_pet_shop.git
cd Clinica_pet_shop
```

## 2. Criar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

## 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

## 4. Configurar Banco de Dados MySQL

### Criar banco de dados:
```sql
CREATE DATABASE petCare;
```

### Importar estrutura:
```bash
mysql -u root -p petCare < database.sql
```

### Popular dados (opcional):
```bash
python populate_db.py
```

## 5. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=petCare
SECRET_KEY=sua_chave_secreta_jwt
```

## 6. Executar o Sistema
```bash
flask run
```

Ou:
```bash
python run.py
```

## 7. Acessar o Sistema
Abra o navegador em: http://localhost:5000

## 🔐 Credenciais de Teste

### Cliente:
- Email: carlos@teste.com
- Senha: senha123

### Veterinário:
- Email: Use o email do veterinário que você cadastrar
- Senha: senha123

## 📝 Observações Importantes

1. Certifique-se de que o MySQL está rodando
2. A porta 5000 deve estar livre
3. Crie um SECRET_KEY forte no .env
4. Não compartilhe o arquivo .env

## 🆘 Problemas Comuns

### Erro de conexão com MySQL:
- Verifique se o MySQL está rodando
- Confirme usuário e senha no .env
- Verifique se o banco petCare foi criado

### Erro de módulos não encontrados:
```bash
pip install -r requirements.txt
```

### Porta 5000 em uso:
```bash
# Matar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```
