# Pet Shop - Aplicação Flask

Uma aplicação web para gerenciamento de Pet Shop construída com Flask.

## Estrutura do Projeto

```
Pet-shop/
├── app/
│   ├── __init__.py          # Inicialização da aplicação
│   ├── routes.py            # Rotas da aplicação
│   ├── static/              # Arquivos estáticos
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   └── templates/           # Templates HTML
│       ├── base.html
│       ├── index.html
│       └── about.html
├── .venv/                   # Ambiente virtual (não versionado)
├── run.py                   # Arquivo principal para executar a aplicação
├── requirements.txt         # Dependências do projeto
├── .gitignore              # Arquivos a serem ignorados pelo git
└── README.md               # Este arquivo
```

## Instalação

1. Clone o repositório
2. O ambiente virtual já está configurado
3. As dependências já foram instaladas

## Como Executar

Para executar a aplicação:

```bash
/Users/luan/Desktop/Pet-shop/.venv/bin/python run.py
```

A aplicação estará disponível em: `http://127.0.0.1:5000`

## Funcionalidades

- Página inicial com apresentação dos serviços
- Página sobre com informações do Pet Shop
- Design responsivo
- Estrutura pronta para expansão

## Próximos Passos

- Adicionar mais páginas (serviços, contato, etc.)
- Implementar banco de dados
- Adicionar formulários de contato
- Criar sistema de agendamento
- Adicionar área administrativa

## Tecnologias

- Python 3.13
- Flask 3.0.0
- HTML5
- CSS3
- JavaScript

## Contribuindo

Sinta-se à vontade para contribuir com melhorias!
