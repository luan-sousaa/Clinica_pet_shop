# 💉 Sistema de Histórico de Vacinas - Documentação

## 📋 Visão Geral

O sistema de histórico de vacinas permite que:
- **Veterinários** registrem e gerenciem vacinas aplicadas
- **Clientes** visualizem o histórico completo de vacinas dos seus pets

---

## 🔗 Rotas da API

### 👨‍⚕️ Rotas para Veterinários

#### 1. Registrar Nova Vacina
```http
POST /api/vacinas
Content-Type: application/json

{
  "pet_id": 1,
  "nome_vacina": "V10 (Décupla)",
  "data_aplicacao": "2025-11-11",
  "proxima_dose": "2026-11-11",
  "lote": "V10-2025-ABC",
  "veterinario": "Dr. João Silva",
  "observacoes": "Primeira dose aplicada",
  "reacoes_adversas": "Nenhuma"
}
```

**Resposta (201):**
```json
{
  "message": "Vacina registrada com sucesso",
  "vacina": {
    "id": 1,
    "pet_id": 1,
    "nome_vacina": "V10 (Décupla)",
    ...
  }
}
```

#### 2. Atualizar Registro de Vacina
```http
PUT /api/vacinas/1
Content-Type: application/json

{
  "observacoes": "Pet apresentou leve sonolência",
  "reacoes_adversas": "Sonolência por 2 horas"
}
```

#### 3. Deletar Registro de Vacina
```http
DELETE /api/vacinas/1
```

---

### 👥 Rotas para Clientes

#### 1. Ver Histórico Completo do Pet
```http
GET /api/pets/1/vacinas
```

**Resposta (200):**
```json
{
  "pet_id": 1,
  "total_vacinas": 3,
  "vacinas": [
    {
      "id": 1,
      "nome_vacina": "V10 (Décupla)",
      "data_aplicacao": "2025-01-15",
      "proxima_dose": "2026-01-15",
      "lote": "V10-2025-ABC",
      "veterinario": "Dr. João Silva",
      "observacoes": "Aplicação normal"
    },
    ...
  ]
}
```

#### 2. Ver Detalhes de Uma Vacina
```http
GET /api/vacinas/1
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `vacinas`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Primary Key (auto incremento) |
| `pet_id` | INTEGER | Foreign Key → pets.id |
| `nome_vacina` | VARCHAR(100) | Nome da vacina |
| `data_aplicacao` | DATE | Data da aplicação |
| `proxima_dose` | DATE (nullable) | Data da próxima dose |
| `lote` | VARCHAR(50) | Número do lote |
| `veterinario` | VARCHAR(100) | Nome do veterinário |
| `veterinario_id` | INTEGER (nullable) | Foreign Key → veterinarios.id |
| `observacoes` | TEXT (nullable) | Observações gerais |
| `reacoes_adversas` | TEXT (nullable) | Reações adversas |
| `criado_em` | DATETIME | Data de criação do registro |
| `atualizado_em` | DATETIME | Data da última atualização |

---

## 📱 Fluxo de Uso

### Para Veterinários:

1. **Login** como veterinário
2. **Selecionar o pet** do cliente
3. **Registrar vacina** com todos os dados
4. **Atualizar** se necessário (ex: adicionar reações adversas)

### Para Clientes:

1. **Login** como cliente
2. **Acessar perfil do pet**
3. **Visualizar histórico** de vacinas
4. **Ver detalhes** de cada vacina aplicada
5. **Ver alerta** de próximas vacinas

---

## 🎨 Sugestão de Interface

### Para Clientes (Tela de Histórico):

```
┌─────────────────────────────────────────┐
│  🐕 Rex - Histórico de Vacinas          │
├─────────────────────────────────────────┤
│                                          │
│  ✅ V10 (Décupla)                       │
│     📅 15/01/2025                       │
│     🔄 Próxima: 15/01/2026              │
│     👨‍⚕️ Dr. João Silva                  │
│                                          │
│  ✅ Antirrábica                         │
│     📅 20/03/2025                       │
│     🔄 Próxima: 20/03/2026              │
│     👩‍⚕️ Dra. Maria Santos               │
│                                          │
│  ⚠️ PRÓXIMAS VACINAS:                   │
│     💉 Gripe Canina - 10/12/2025        │
│                                          │
└─────────────────────────────────────────┘
```

### Para Veterinários (Tela de Registro):

```
┌─────────────────────────────────────────┐
│  Registrar Nova Vacina                  │
├─────────────────────────────────────────┤
│  Pet: [Rex ▼]                          │
│  Vacina: [V10 (Décupla) ▼]            │
│  Data Aplicação: [11/11/2025]          │
│  Próxima Dose: [11/11/2026]            │
│  Lote: [_________________]             │
│  Veterinário: [Dr. João Silva]         │
│  Observações:                           │
│  [____________________________]         │
│                                          │
│  [Salvar] [Cancelar]                   │
└─────────────────────────────────────────┘
```

---

## 🔐 Permissões e Segurança

### Veterinários podem:
- ✅ Criar registros de vacinas
- ✅ Editar registros que criaram
- ✅ Ver todos os registros
- ❌ Não podem deletar (apenas marcar como erro)

### Clientes podem:
- ✅ Ver histórico dos SEUS pets apenas
- ✅ Ver detalhes das vacinas
- ❌ Não podem editar ou deletar

---

## 📊 Recursos Adicionais (Futuro)

- 📧 **Email de lembrete** quando próxima vacina estiver próxima
- 📄 **Exportar PDF** do cartão de vacinação
- 📊 **Dashboard** com estatísticas de vacinação
- 🔔 **Notificações push** para vacinas vencidas
- 📷 **Upload de comprovante** da vacina

---

## 🧪 Testando no Postman

### 1. Registrar Vacina (Veterinário):
```
POST http://127.0.0.1:5000/api/vacinas
Headers: Content-Type: application/json
Body: {JSON com dados da vacina}
```

### 2. Ver Histórico (Cliente):
```
GET http://127.0.0.1:5000/api/pets/1/vacinas
```

### 3. Ver Detalhes:
```
GET http://127.0.0.1:5000/api/vacinas/1
```

---

## 💡 Dicas de Implementação

1. **Adicionar autenticação** para verificar se usuário é veterinário ou cliente
2. **Implementar banco de dados** (SQLite, PostgreSQL, MySQL)
3. **Validar datas** (próxima dose deve ser posterior à aplicação)
4. **Adicionar tipos de usuário** (cliente, veterinário, admin)
5. **Criar filtros** (por tipo de vacina, por período)

---

Criado em: 11/11/2025
