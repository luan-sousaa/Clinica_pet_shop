# 🐾 Sistema de Gerenciamento de Pet Shop - PetCare

Sistema completo de gerenciamento de clínica veterinária desenvolvido com Flask (backend) e JavaScript vanilla (frontend), integrado com banco de dados MySQL.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

## Stack Tecnológica

### Backend
- **Flask 3.1.2** - Framework web Python
- **Flask-CORS 6.0.1** - Gerenciamento de CORS
- **MySQL Connector Python** - Conexão com banco de dados MySQL
- **PyJWT** - Autenticação via JSON Web Tokens
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **JavaScript ES6+** - Linguagem de programação
- **HTML5 & CSS3** - Interface do usuário
- **Fetch API** - Requisições HTTP

### Banco de Dados
- **MySQL 8.0** - Sistema de gerenciamento de banco de dados relacional
- **Triggers** - Hash automático de senhas (SHA256)
- **Stored Procedures** - Listagem de consultas do dia
- **Views** - Visualizações otimizadas de dados
- **Roles** - Controle de acesso (ADM, VET, CLI)
- **Indexes** - Otimização de consultas

## Arquitetura do Banco de Dados

### Estrutura de Tabelas

```
GRUPO_USUARIO
├── ID_ACESSO (CHAR(36) PK)
├── ROLE_MYSQL (VARCHAR(50))
├── TIPO_ACESSO (VARCHAR(20))
└── DESCRICAO (VARCHAR(225))

USUARIO
├── ID_USUARIO (CHAR(36) PK) - UUID gerado por function
├── NOME_COMPLETO (VARCHAR(250))
├── EMAIL (VARCHAR(225)) - INDEX
├── SENHA (VARCHAR(64)) - SHA256 hash via trigger
└── GRUPO_USUARIO (CHAR(36) FK)

CLIENTE
├── ID_USUARIO (CHAR(36) PK, FK)
├── TELEFONE (VARCHAR(11))
├── BAIRRO (VARCHAR(30))
├── RUA (INT(3))
├── CIDADE (VARCHAR(50))
├── CPF (BIGINT(11) UNIQUE)
└── ID_PET (INT FK)

PET
├── ID_PET (INT PK AUTO_INCREMENT)
├── NOME (VARCHAR(100))
├── RACA (VARCHAR(100))
├── IDADE (FLOAT)
├── OBSERVACOES (TEXT(250))
└── ID_VACINAS (INT FK)

VACINAS
├── ID_VAC (INT PK AUTO_INCREMENT)
├── NOME (VARCHAR(50))
├── DOSE (INT)
└── DATA_APLICADO (DATE)

VETERINARIO
├── CRMV (INT PK)
├── ID_USUARIO (CHAR(36) FK)
├── SALARIO (DOUBLE(7,2))
└── TURNO (VARCHAR(30))

CONSULTA
├── ID_PROCEDIMENTO (CHAR(36) PK) - UUID gerado por function
├── DATA_CONSULTA (DATE) - INDEX
├── VALOR (DOUBLE(7,2))
├── ID_PET (INT FK)
└── CRMV (INT FK)
```

### Recursos Avançados do Banco

#### 🔐 Triggers
- **hash_senha**: Converte senhas em SHA256 antes de inserir
- **hash_atualiza**: Atualiza senha com hash SHA256

#### ⚡ Procedures
- **listar_consultas**: Lista consultas por data específica

#### 👁️ Views
- **INFO_PET**: Informações do pet com dados do tutor
- **HISTORICO_VACINA**: Histórico completo de vacinas do pet

#### 🔑 Function
- **gera_id_dados_criticos()**: Gera UUID para dados sensíveis

#### 🛡️ Roles e Permissões
- **ADM**: Acesso total ao sistema
- **VET**: Gerenciar pets, consultas, vacinas, prescrições
- **CLI**: Visualizar dados do próprio pet

## Instalação e Configuração

### 1. Pré-requisitos

- Python 3.13+
- MySQL 8.0+
- Git

### 2. Clonar o Repositório

```bash
git clone https://github.com/luan-sousaa/Clinica_pet_shop.git
cd Clinica_pet_shop
```

### 3. Criar Ambiente Virtual

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

Dependências principais:
```
flask==3.1.2
flask-cors==6.0.1
mysql-connector-python
python-dotenv
PyJWT
```

### 5. Configurar Banco de Dados MySQL

#### Criar o banco de dados

Execute o script SQL fornecido no MySQL:

```bash
mysql -u root -p < database.sql
```

Ou execute manualmente no MySQL Workbench/Terminal:

```sql
CREATE DATABASE petCare;
USE petCare;

-- Execute todo o conteúdo do arquivo database.sql
-- (inclui criação de tabelas, triggers, procedures, views, roles, etc.)
```

#### Configurar credenciais

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Configurações do Banco de Dados MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_NAME=petCare

# Configurações da Aplicação
SECRET_KEY=sua_chave_secreta_aleatoria
FLASK_ENV=development
```

### 6. Popular Tabela de Grupos de Usuário

Execute o script para criar os grupos de acesso:

```bash
python populate_db.py
```

Este script cria os seguintes grupos:
- **Administrador** (Role: ADM)
- **Veterinario** (Role: VET)
- **Cliente** (Role: CLI)

### 7. Executar a Aplicação

```bash
python run.py
```

A aplicação estará disponível em: `http://localhost:5000`

## Endpoints da API REST

### Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/login` | Login de usuário | Não |
| POST | `/cadastro` | Cadastro de cliente/tutor | Não |
| POST | `/cadastro_vet` | Cadastro de veterinário | Não |
| POST | `/esqueceu_senha` | Redefinir senha | Não |

### Cliente (Role: CLI)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/dados_pet` | Dados do pet do cliente logado | JWT Token |
| GET | `/consultas/<pet_id>` | Listar consultas do pet | JWT Token |
| GET | `/historico/<pet_id>/vacinas` | Histórico de vacinas | JWT Token |
| GET | `/historico/<pet_id>/prescricoes` | Prescrições médicas | JWT Token |

### Veterinário (Role: VET)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/agendamentos` | Criar consulta/agendamento | JWT Token (VET) |
| GET | `/consultas_dia/<data>` | Consultas do dia (Procedure) | JWT Token (VET) |
| POST | `/vacinas` | Registrar vacina | JWT Token (VET) |
| PUT | `/vacinas/<id>` | Atualizar vacina | JWT Token (VET) |
| DELETE | `/vacinas/<id>` | Deletar vacina | JWT Token (VET) |
| POST | `/prescricoes` | Criar prescrição | JWT Token (VET) |

### Geral

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/test_db` | Testar conexão com BD | Não |
| GET | `/vacinas/<id>` | Detalhes de vacina | JWT Token |
| GET | `/prescricoes/<id>` | Detalhes de prescrição | JWT Token |

## Autenticação JWT

O sistema utiliza JSON Web Tokens (JWT) para autenticação. 

### Como usar:

1. Faça login através do endpoint `/login`
2. Receba o token JWT na resposta
3. Inclua o token no header de requisições protegidas:

```javascript
headers: {
    'Authorization': 'Bearer seu_token_aqui',
    'Content-Type': 'application/json'
}
```

### Estrutura do Token:

```json
{
    "user_id": "uuid-do-usuario",
    "email": "usuario@email.com",
    "tipo_acesso": "Cliente|Veterinario|Administrador",
    "role": "CLI|VET|ADM",
    "exp": 1234567890
}
```

## Estrutura do Projeto

```
Pet-shop/
├── app/
│   ├── __init__.py           # Inicialização do Flask e BD
│   ├── auth.py               # Decorators de autenticação/autorização
│   ├── config.py             # Configurações da aplicação
│   ├── database.py           # Gerenciamento de conexão MySQL
│   ├── models.py             # Modelos de dados (ORM-like)
│   ├── routes.py             # Rotas da API
│   ├── static/               # Arquivos estáticos
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── config.js
│   │   │   ├── api.js
│   │   │   ├── utils.js
│   │   │   ├── auth.js
│   │   │   └── controllers/
│   │   │       ├── cadastroController.js
│   │   │       ├── cadastroVetController.js
│   │   │       ├── clienteController.js
│   │   │       ├── escolhaCadastroController.js
│   │   │       ├── loginController.js
│   │   │       └── veterinarioController.js
│   │   └── templates/
│   │       ├── index.html
│   │       ├── cadastrotutor.html
│   │       ├── cadastrovet.html
│   │       ├── cliente.html
│   │       ├── escolhacadastro.html
│   │       ├── redefinir-senha.html
│   │       └── veterinario.html
├── .env                      # Variáveis de ambiente (não versionado)
├── .env.example              # Exemplo de configuração
├── .gitignore
├── populate_db.py            # Script para popular GRUPO_USUARIO
├── requirements.txt          # Dependências Python
├── run.py                    # Ponto de entrada da aplicação
└── README.md
```

## Métricas do Projeto

- **Linhas de código Python**: ~1.200
- **Linhas de código JavaScript**: ~1.500
- **Módulos Python**: 6 (auth, config, database, models, routes, __init__)
- **Controllers JavaScript**: 6
- **Páginas HTML**: 7
- **Rotas da API**: 25+
- **Tabelas do Banco**: 7
- **Triggers**: 2
- **Procedures**: 1
- **Views**: 2
- **Roles**: 3

## Funcionalidades Implementadas

### Sistema de Autenticação
- Cadastro de clientes (tutores) com seus pets
- Cadastro de veterinários com CRMV
- Login com JWT authentication
- Redefinição de senha
- Hash automático de senhas (SHA256) via trigger

### Área do Cliente
- Visualizar dados do pet
- Histórico de consultas
- Histórico de vacinas (usando VIEW)
- Prescrições médicas

### Área do Veterinário
- Criar consultas/agendamentos
- Listar consultas do dia (usando PROCEDURE)
- Registrar vacinas
- Criar prescrições médicas
- Buscar cliente por CPF

### Segurança
- Autenticação via JWT
- Controle de acesso baseado em roles (ADM, VET, CLI)
- Senhas hasheadas com SHA256
- IDs sensíveis com UUID
- Validação de dados

### Performance
- Pool de conexões MySQL
- Indexes em campos críticos (EMAIL, DATA_CONSULTA)
- Views otimizadas para consultas frequentes

## Padrões Implementados

- **REST API**: Endpoints seguindo padrões RESTful
- **JWT Authentication**: Autenticação stateless
- **MVC**: Separação de Model, View e Controller
- **Repository Pattern**: Camada de acesso a dados
- **Dependency Injection**: Configurações via .env
- **Decorator Pattern**: Controle de acesso via decorators
- **Pool de Conexões**: Gerenciamento eficiente de recursos

## Testes

### Testar conexão com o banco:

```bash
curl http://localhost:5000/test_db
```

### Testar cadastro de cliente:

```bash
curl -X POST http://localhost:5000/cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "nome_tutor": "João Silva",
    "cpf": "12345678901",
    "email": "joao@email.com",
    "senha": "senha123",
    "confirmar_senha": "senha123",
    "telefone": "11999999999",
    "nome_pet": "Rex",
    "raca_pet": "Labrador",
    "datanascimento": "2020-01-15",
    "observacoes_pet": "Pet saudável"
  }'
```

### Testar login:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "senha": "senha123"
  }'
```

## Desenvolvimento

### Estrutura de Desenvolvimento

O projeto está configurado para desenvolvimento local com:

- Debug mode ativado
- Hot reload do Flask
- CORS liberado para desenvolvimento
- Logs detalhados

### Adicionar novas funcionalidades

1. **Criar modelo** em `app/models.py`
2. **Adicionar rotas** em `app/routes.py`
3. **Atualizar frontend** em `app/static/js/controllers/`
4. **Testar endpoints** com curl ou Postman

## Troubleshooting

### Erro de conexão com MySQL

```
Verifique:
- MySQL está rodando
- Credenciais no .env estão corretas
- Banco petCare foi criado
- Usuário MySQL tem permissões adequadas
```

### Erro "Grupo de usuário não encontrado"

```bash
Execute: python populate_db.py
```

### Token inválido/expirado

```
Tokens expiram em 24 horas.
Faça login novamente para obter novo token.
```

## Próximos Passos

- [ ] Implementar tabela PRESCRICAO no banco
- [ ] Adicionar upload de imagens de pets
- [ ] Sistema de notificações
- [ ] Dashboard com gráficos
- [ ] Relatórios em PDF
- [ ] Agendamento online
- [ ] Integração com pagamento

## Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## Contato

**Desenvolvedor**: Luan Sousa  
**GitHub**: [@luan-sousaa](https://github.com/luan-sousaa)  
**Repositório**: [Clinica_pet_shop](https://github.com/luan-sousaa/Clinica_pet_shop)

---

Desenvolvido com dedicação para aprimoramento de habilidades em desenvolvimento full-stack com Python, Flask, MySQL e JavaScript.
