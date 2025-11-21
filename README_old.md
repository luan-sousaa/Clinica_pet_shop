# PetLover - Sistema de Gestão de Clínica Veterinária

![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![Python](https://img.shields.io/badge/Python-3.13.5-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![Status](https://img.shields.io/badge/Status-Integrado-success)

Sistema completo de gerenciamento para clínicas veterinárias com front-end e back-end totalmente integrados.

---

## Funcionalidades

### Para Tutores (Donos de Pets)
- Cadastro completo de tutor e pet com validação de CPF
- Sistema de autenticação com recuperação de senha
- Visualização completa de dados do pet incluindo data de nascimento
- Histórico detalhado de vacinas com informações de dosagem e veterinário responsável
- Acompanhamento de consultas agendadas com motivo e observações
- Visualização de prescrições médicas com detalhamento de medicamentos
- Agenda integrada de compromissos veterinários

### Para Veterinários
- Cadastro profissional com validação de CRMV
- Criação de consultas identificadas por CPF do tutor
- Registro de vacinas com controle de lote e datas
- Emissão de prescrições médicas com múltiplos medicamentos
- Gerenciamento completo de histórico médico dos pacientes
- Interface dedicada para busca de pets por CPF do tutor

---

## Arquitetura do Sistema

```
Pet-shop/
├── app/
│   ├── __init__.py          # Inicialização + CORS
│   ├── routes.py            # API REST + Static files
│   ├── models.py            # Modelos de dados
│   └── static/              # Front-end
│       ├── *.html           # 5 páginas integradas
│       ├── style.css        # Estilização
│       ├── images/          # Assets
│       └── js/              # 8 módulos JavaScript
│           ├── config.js         # Configurações
│           ├── api.js            # Camada de API
│           ├── utils.js          # Utilitários
│           ├── auth.js           # Autenticação
│           └── *.controller.js   # Controllers por página
├── docs/                    # Documentação completa
├── run.py                   # Servidor
└── requirements.txt         # Dependências
```

---

## Instalação e Execução

### Pré-requisitos
- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual Python (venv)

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/luan-sousaa/Clinica_pet_shop.git
cd Pet-shop
```

### Passo 2: Configurar Ambiente Virtual
```bash
# Criar ambiente virtual (se ainda não existe)
python -m venv .venv

# Ativar ambiente virtual
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar o Servidor
```bash
python run.py
```

### Passo 5: Acessar a Aplicação
Abrir navegador e acessar: **http://127.0.0.1:5000**

---

## Uso do Sistema

### Credenciais de Teste
```
Tutor:
Email: admin@gmail.com
Senha: 1234

Veterinário:
Email: vet@gmail.com
Senha: 1234
```

### Fluxo de Operação
1. Acesso inicial através da página de login
2. Opção de cadastro diferenciado para tutores e veterinários
3. Dashboard personalizado com base no tipo de usuário
4. Criação e gerenciamento de consultas pelo veterinário
5. Visualização de histórico completo pelo tutor

---

## Endpoints da API REST

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/login` | Autenticação de usuário | Não |
| POST | `/cadastro` | Cadastro de tutor e pet | Não |
| POST | `/cadastro_vet` | Cadastro de veterinário | Não |
| POST | `/esqueceu_senha` | Redefinição de senha | Não |
| GET | `/dados_pet` | Informações do pet | Sim |
| GET | `/consultas/<pet_id>` | Consultas agendadas | Sim |
| POST | `/agendamentos` | Criar consulta | Sim |
| GET | `/historico/<pet_id>/vacinas` | Histórico de vacinas | Sim |
| POST | `/vacinas` | Registrar nova vacina | Sim |
| GET | `/vacinas/<vacina_id>` | Detalhes de vacina | Sim |
| PUT | `/vacinas/<vacina_id>` | Atualizar vacina | Sim |
| DELETE | `/vacinas/<vacina_id>` | Remover vacina | Sim |
| GET | `/historico/<pet_id>/prescricoes` | Histórico de prescrições | Sim |
| POST | `/prescricoes` | Criar prescrição médica | Sim |
| GET | `/prescricoes/<prescricao_id>` | Detalhes de prescrição | Sim |
| PUT | `/prescricoes/<prescricao_id>` | Atualizar prescrição | Sim |
| PATCH | `/prescricoes/<prescricao_id>/finalizar` | Finalizar prescrição | Sim |
| DELETE | `/prescricoes/<prescricao_id>` | Remover prescrição | Sim |

Documentação técnica detalhada disponível em: [`docs/INTEGRACAO_FRONTEND_BACKEND.md`](docs/INTEGRACAO_FRONTEND_BACKEND.md)

---

## Stack Tecnológica

### Back-end
- **Flask 3.1.2** - Framework web Python
- **Flask-CORS 6.0.1** - Gerenciamento de Cross-Origin Resource Sharing
- **Python 3.13.5** - Linguagem de programação principal
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente

### Front-end
- **HTML5** - Estrutura semântica de páginas
- **CSS3** - Estilização com design responsivo
- **JavaScript ES6+** - Lógica de aplicação modularizada
- **Fetch API** - Comunicação HTTP assíncrona

### Padrões de Desenvolvimento
- Arquitetura MVC (Model-View-Controller)
- REST API com métodos HTTP padronizados
- Código modularizado em 11 módulos JavaScript
- Separation of Concerns entre camadas
- Princípios SOLID e Clean Code
- DRY (Don't Repeat Yourself)

---

## Métricas do Projeto

- **Código Python**: ~600 linhas
- **Código JavaScript**: ~1.200 linhas
- **Módulos JavaScript**: 11 arquivos
- **Páginas HTML**: 7 interfaces
- **Endpoints REST**: 18 rotas
- **Controllers**: 6 classes especializadas

---

## Documentação Técnica

A documentação completa do sistema está organizada nos seguintes arquivos:

- [Integração Front-end e Back-end](docs/INTEGRACAO_FRONTEND_BACKEND.md)
- [Sistema de Histórico de Vacinas](docs/HISTORICO_VACINAS.md)
- [Prescrições Médicas](docs/PRESCRICOES_MEDICAS.md)

---

## Características da Interface

### Sistema de Validações
- Validação de formato de email via expressão regular
- Verificação de CPF com exatamente 11 dígitos numéricos
- Validação de CRMV para cadastro de veterinários
- Confirmação de senha com verificação de correspondência
- Campos obrigatórios sinalizados visualmente

### Experiência do Usuário
- Sistema de notificações toast com animações suaves
- Estados de carregamento durante requisições assíncronas
- Feedback visual imediato para ações do usuário
- Design responsivo compatível com múltiplos dispositivos
- Navegação intuitiva com botões de retorno

### Segurança
- Sanitização de dados de entrada no cliente e servidor
- Validação dupla (front-end e back-end)
- Configuração CORS restritiva
- Persistência segura de sessão via localStorage
- Prevenção de injeção de código

---

## Arquitetura dos Módulos JavaScript

```javascript
// config.js - Configurações centralizadas do sistema
const CONFIG = {
    API_BASE_URL: window.location.origin,
    ENDPOINTS: {
        LOGIN: '/login',
        CADASTRO_TUTOR: '/cadastro',
        CADASTRO_VET: '/cadastro_vet',
        // ... demais endpoints
    },
    STORAGE_KEYS: {
        USER: 'petlover_user',
        PET_ID: 'petlover_pet_id'
    }
};

// api.js - Camada de comunicação com API
class APIService {
    async request(endpoint, options) {
        // Requisições HTTP genéricas
    }
    async login(email, senha) {
        // Autenticação de usuário
    }
    async cadastroTutor(dados) {
        // Registro de tutor
    }
    // ... 16 métodos de API
}

// utils.js - Funções utilitárias
const Utils = {
    isValidEmail(email) {
        // Validação de email
    },
    showSuccess(message) {
        // Exibição de notificações
    },
    showError(message) {
        // Exibição de erros
    }
};

// auth.js - Gerenciamento de autenticação
const Auth = {
    saveUser(userData) {
        // Persistência de sessão
    },
    isAuthenticated() {
        // Verificação de autenticação
    },
    requireAuth() {
        // Proteção de rotas
    }
};

// Controllers - Controladores especializados por página
class LoginController {
    async handleLogin(event) { /* ... */ }
}
class CadastroTutorController {
    async handleCadastro(event) { /* ... */ }
}
class CadastroVetController {
    async handleCadastro(event) { /* ... */ }
}
class ClienteController {
    async loadConsultas() { /* ... */ }
    async loadPrescricoes() { /* ... */ }
}
class VeterinarioController {
    async handleNovaConsulta(event) { /* ... */ }
    async handleNovaPrescricao(event) { /* ... */ }
}
class RedefinirSenhaController {
    async handleRedefinirSenha(event) { /* ... */ }
}
```

---

## Processo de Debug

### Ativação de Logs Detalhados
```javascript
// Console do navegador (F12):
localStorage.setItem('debug', 'true');
```

### Monitoramento de Erros
```bash
# Logs do servidor Flask
python run.py

# Console do navegador para debug client-side
F12 → Console → Network
```

### Ferramentas Recomendadas
- Inspetor de Elementos do navegador
- Network tab para análise de requisições HTTP
- Console para erros JavaScript
- Breakpoints para debugging de código

---

## Roadmap de Desenvolvimento

### Próximas Implementações
- Integração com banco de dados relacional (PostgreSQL/MySQL)
- Sistema de autenticação JWT com refresh tokens
- Upload e armazenamento de imagens de pets
- Sistema de notificações em tempo real via WebSocket
- Geração de relatórios e histórico em PDF
- Dashboard com gráficos e estatísticas
- Cobertura de testes unitários e integração
- Containerização com Docker e Docker Compose
- CI/CD com GitHub Actions
- Documentação de API com Swagger/OpenAPI

---

## Contribuições

### Como Contribuir
1. Realizar fork do repositório
2. Criar branch de feature (`git checkout -b feature/nome-funcionalidade`)
3. Implementar mudanças seguindo padrões do projeto
4. Realizar commit das alterações (`git commit -m 'Descrição detalhada'`)
5. Enviar push para a branch (`git push origin feature/nome-funcionalidade`)
6. Abrir Pull Request com descrição completa

### Diretrizes de Código
- Seguir padrões de nomenclatura existentes
- Adicionar comentários em código complexo
- Manter modularização e separação de responsabilidades
- Validar dados tanto no cliente quanto no servidor
- Testar funcionalidades antes de submeter PR

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

## Informações do Projeto

**Desenvolvedor**: Luan Sousa  
**Repositório**: [github.com/luan-sousaa/Clinica_pet_shop](https://github.com/luan-sousaa/Clinica_pet_shop)  
**GitHub**: [@luan-sousaa](https://github.com/luan-sousaa)

---

## Padrões Implementados

O sistema foi desenvolvido seguindo as melhores práticas de engenharia de software:

- Clean Architecture para separação de camadas
- RESTful API Design com métodos HTTP padronizados
- Modern JavaScript (ES6+) com classes e módulos
- Responsive Web Design para múltiplos dispositivos
- User Experience (UX) com feedback visual consistente
- Separation of Concerns entre lógica e apresentação
- SOLID principles em controllers e serviços

---

Para informações técnicas detalhadas sobre integração e arquitetura, consulte a [documentação completa](docs/INTEGRACAO_FRONTEND_BACKEND.md).
