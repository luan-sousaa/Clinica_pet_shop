# 💊 Sistema de Prescrições Médicas - Documentação

## 📋 Visão Geral

Sistema completo para veterinários criarem prescrições médicas e clientes visualizarem os tratamentos dos seus pets.

---

## 🔗 Rotas da API

### 👨‍⚕️ Rotas para Veterinários

#### 1. Criar Prescrição Médica
```http
POST /prescricoes
Content-Type: application/json

{
  "pet_id": 1,
  "veterinario": "Dr. João Silva",
  "veterinario_id": 1,
  "data_consulta": "2025-11-11",
  "diagnostico": "Infecção de ouvido (Otite externa)",
  "medicamentos": [
    {
      "nome": "Antibiótico Otomax",
      "dosagem": "5 gotas",
      "frequencia": "2x ao dia (manhã e noite)",
      "duracao": "7 dias",
      "observacoes": "Aplicar diretamente no ouvido após limpeza",
      "via_administracao": "Tópica"
    },
    {
      "nome": "Anti-inflamatório Prednisolona",
      "dosagem": "1 comprimido de 5mg",
      "frequencia": "1x ao dia",
      "duracao": "5 dias",
      "observacoes": "Administrar com alimento",
      "via_administracao": "Oral"
    }
  ],
  "orientacoes_gerais": "Manter o pet em repouso. Não permitir que coce a orelha.",
  "retorno": "2025-11-18"
}
```

**Resposta (201):**
```json
{
  "message": "Prescrição criada com sucesso",
  "prescricao": {
    "id": 1,
    "pet_id": 1,
    "veterinario": "Dr. João Silva",
    ...
  }
}
```

#### 2. Atualizar Prescrição
```http
PUT /prescricoes/1
Content-Type: application/json

{
  "medicamentos": [...],
  "orientacoes_gerais": "Orientações atualizadas"
}
```

#### 3. Finalizar Prescrição (marcar como concluída)
```http
PATCH /prescricoes/1/finalizar
```

**Resposta (200):**
```json
{
  "message": "Prescrição 1 marcada como concluída",
  "status": "concluída",
  "finalizado_em": "2025-11-18T14:00:00"
}
```

#### 4. Deletar Prescrição
```http
DELETE /prescricoes/1
```

---

### 👥 Rotas para Clientes

#### 1. Ver Histórico de Prescrições do Pet
```http
GET /historico/1/prescricoes
```

**Resposta (200):**
```json
{
  "pet_id": 1,
  "total_prescricoes": 2,
  "prescricoes": [
    {
      "id": 1,
      "data_consulta": "2025-11-11",
      "veterinario": "Dr. João Silva",
      "diagnostico": "Infecção de ouvido",
      "status": "ativa",
      "medicamentos_count": 2
    },
    {
      "id": 2,
      "data_consulta": "2025-10-15",
      "veterinario": "Dra. Maria Santos",
      "diagnostico": "Alergia alimentar",
      "status": "concluída",
      "medicamentos_count": 1
    }
  ]
}
```

#### 2. Ver Detalhes da Prescrição
```http
GET /prescricoes/1
```

**Resposta (200):**
```json
{
  "id": 1,
  "pet_id": 1,
  "nome_pet": "Rex",
  "veterinario": "Dr. João Silva",
  "crm_vet": "12345-SP",
  "data_consulta": "2025-11-11",
  "diagnostico": "Infecção de ouvido (Otite externa)",
  "medicamentos": [
    {
      "nome": "Antibiótico Otomax",
      "dosagem": "5 gotas",
      "frequencia": "2x ao dia",
      "duracao": "7 dias",
      "observacoes": "Aplicar após limpeza",
      "via_administracao": "Tópica"
    }
  ],
  "orientacoes_gerais": "Manter em repouso",
  "retorno": "2025-11-18",
  "status": "ativa"
}
```

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `prescricoes`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Primary Key |
| `pet_id` | INTEGER | Foreign Key → pets.id |
| `veterinario` | VARCHAR(100) | Nome do veterinário |
| `veterinario_id` | INTEGER | Foreign Key → veterinarios.id |
| `data_consulta` | DATE | Data da consulta |
| `diagnostico` | TEXT | Diagnóstico do veterinário |
| `orientacoes_gerais` | TEXT | Orientações gerais |
| `retorno` | DATE (nullable) | Data de retorno |
| `status` | VARCHAR(20) | ativa, concluída, cancelada |
| `criado_em` | DATETIME | Data de criação |
| `atualizado_em` | DATETIME | Data da última atualização |

### Tabela: `medicamentos_prescricao`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Primary Key |
| `prescricao_id` | INTEGER | Foreign Key → prescricoes.id |
| `nome` | VARCHAR(200) | Nome do medicamento |
| `dosagem` | VARCHAR(100) | Dosagem (ex: 1 comprimido) |
| `frequencia` | VARCHAR(100) | Frequência (ex: 2x ao dia) |
| `duracao` | VARCHAR(100) | Duração (ex: 7 dias) |
| `via_administracao` | VARCHAR(50) | Oral, Tópica, Injetável, etc |
| `observacoes` | TEXT | Observações específicas |

---

## 📱 Fluxo de Uso

### Para Veterinários:

1. **Realizar consulta** no pet
2. **Criar prescrição** com diagnóstico
3. **Adicionar medicamentos** necessários
4. **Definir orientações** para o tutor
5. **Agendar retorno** se necessário
6. **Atualizar** prescrição se necessário
7. **Finalizar** quando tratamento concluir

### Para Clientes:

1. **Login** no sistema
2. **Acessar histórico** de prescrições do pet
3. **Ver detalhes** da prescrição ativa
4. **Consultar medicamentos** e dosagens
5. **Ver orientações** do veterinário
6. **Verificar data** de retorno

---

## 🎨 Sugestão de Interface

### Para Clientes (Tela de Prescrição):

```
┌─────────────────────────────────────────┐
│  💊 Prescrição Médica - Rex             │
├─────────────────────────────────────────┤
│  👨‍⚕️ Dr. João Silva - CRM: 12345-SP     │
│  📅 Data: 11/11/2025                    │
│                                          │
│  🔍 DIAGNÓSTICO:                        │
│  Infecção de ouvido (Otite externa)     │
│                                          │
│  💊 MEDICAMENTOS:                       │
│                                          │
│  1️⃣ Antibiótico Otomax                 │
│     📏 Dose: 5 gotas                    │
│     ⏰ Frequência: 2x ao dia            │
│     📅 Duração: 7 dias                  │
│     📝 Aplicar após limpeza do ouvido   │
│                                          │
│  2️⃣ Anti-inflamatório Prednisolona     │
│     📏 Dose: 1 comprimido (5mg)         │
│     ⏰ Frequência: 1x ao dia            │
│     📅 Duração: 5 dias                  │
│     📝 Dar com alimento                 │
│                                          │
│  📋 ORIENTAÇÕES GERAIS:                 │
│  • Manter em repouso                    │
│  • Não deixar coçar a orelha            │
│  • Retornar se piorar                   │
│                                          │
│  🔄 Retorno: 18/11/2025                 │
│                                          │
│  [Imprimir PDF] [Marcar Medicamento]   │
└─────────────────────────────────────────┘
```

### Para Veterinários (Criar Prescrição):

```
┌─────────────────────────────────────────┐
│  Criar Prescrição - Rex (Labrador)      │
├─────────────────────────────────────────┤
│  Data Consulta: [11/11/2025]           │
│                                          │
│  Diagnóstico:                           │
│  [____________________________]         │
│                                          │
│  MEDICAMENTOS:                          │
│  ┌────────────────────────────┐         │
│  │ Nome: [Antibiótico Otomax] │         │
│  │ Dosagem: [5 gotas]         │         │
│  │ Frequência: [2x ao dia]    │         │
│  │ Duração: [7 dias]          │         │
│  │ Via: [Tópica ▼]            │         │
│  │ Obs: [_________________]   │         │
│  └────────────────────────────┘         │
│  [+ Adicionar outro medicamento]        │
│                                          │
│  Orientações Gerais:                    │
│  [____________________________]         │
│                                          │
│  Data Retorno: [18/11/2025]            │
│                                          │
│  [Salvar Prescrição] [Cancelar]        │
└─────────────────────────────────────────┘
```

---

## 🔐 Validações Importantes

### Na criação:
- ✅ Pelo menos 1 medicamento obrigatório
- ✅ Campos obrigatórios: pet_id, veterinário, data, diagnóstico
- ✅ Data de retorno deve ser posterior à consulta
- ✅ Dosagens devem ser claras e específicas

### Segurança:
- 🔒 Apenas veterinários podem criar/editar
- 🔒 Clientes só veem prescrições dos SEUS pets
- 🔒 Registrar histórico de alterações
- 🔒 Não permitir deletar após 24h (apenas desativar)

---

## 📊 Status da Prescrição

| Status | Descrição |
|--------|-----------|
| `ativa` | Tratamento em andamento |
| `concluída` | Tratamento finalizado |
| `cancelada` | Prescrição cancelada |
| `vencida` | Prazo de tratamento expirado |

---

## 🧪 Testando no Postman

### 1. Criar Prescrição:
```
POST http://127.0.0.1:5000/prescricoes
Headers: Content-Type: application/json
Body: {JSON completo}
```

### 2. Ver Histórico:
```
GET http://127.0.0.1:5000/historico/1/prescricoes
```

### 3. Ver Detalhes:
```
GET http://127.0.0.1:5000/prescricoes/1
```

### 4. Finalizar:
```
PATCH http://127.0.0.1:5000/prescricoes/1/finalizar
```

---

## 💡 Recursos Futuros

- 📧 **Email com prescrição** para o cliente
- 📱 **Notificação** de horário dos medicamentos
- 📄 **Gerar PDF** da prescrição
- 🔔 **Alertas** de retorno próximo
- 📊 **Dashboard** de prescrições ativas
- 🏥 **Histórico médico** completo do pet
- 💬 **Chat** veterinário-cliente sobre prescrição

---

Criado em: 11/11/2025
