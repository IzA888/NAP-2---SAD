# Sistema de Gestão Financeira

## Visão Geral

Este projeto é um sistema de gestão financeira desenvolvido em Django que oferece funcionalidades abrangentes para gerenciar:

- Vendas e transações comerciais
- Fluxo de caixa
- Controle de estoque
- Relatórios financeiros
- Métricas e indicadores financeiros

## Funcionalidades Principais

### Dashboard
- Visão geral das métricas financeiras
- Gráfico do fluxo de caixa dos últimos 7 dias
- Listagem de transações recentes e pendentes

### Vendas
- Registro de novas vendas
- Gestão de itens de venda
- Comparativo de vendas por período
- Relatórios de vendas

### Fluxo de Caixa
- Controle de entradas e saídas
- Saldo acumulado
- Análise por períodos

### Estoque
- Cadastro de produtos
- Controle de estoque mínimo
- Atualização de quantidades

### Receitas
- Gestão de despesas
- Monitoramento de saldo
- Análise financeira

## Tecnologias Utilizadas

- Django (Framework web Python)
- PostgreSQL (Banco de dados)
- Celery (Tarefas assíncronas)
- Matplotlib (Geração de gráficos)
- Bootstrap (Interface do usuário)

## Configuração do Projeto

### Pré-requisitos

- Python 3.8+
- Django 4.0+
- PostgreSQL
- Celery
- Redis (para Celery)

### Instalação

1. Clone o repositório:
   ```
   git clone [URL do repositório]
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados no arquivo `settings.py`

5. Execute as migrações:
   ```
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```

7. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

8. Para tarefas assíncronas, inicie o Celery:
   ```
   celery -A GestaodeFinancas worker -l info
   celery -A GestaodeFinancas beat -l info
   ```

## Estrutura do Projeto

```
GestaodeFinancas/
│
├── Financas/
│   ├── migrations/       # Migrações do banco de dados
│   ├── static/          # Arquivos estáticos
│   ├── templates/       # Templates HTML
│   ├── __init__.py
│   ├── admin.py         # Configuração do admin
│   ├── apps.py          # Configuração do app
│   ├── celery.py        # Configuração do Celery
│   ├── controller.py    # Lógica de negócios
│   ├── forms.py         # Formulários
│   ├── indicadores_financeiros.py  # Cálculos financeiros
│   ├── models.py        # Modelos de dados
│   ├── urls.py          # URLs do app
│   ├── utils.py         # Utilitários
│   └── views.py         # Views
│
├── GestaodeFinancas/    # Configurações do projeto
└── manage.py            # Script de gerenciamento
```

## Modelos Principais

- `Produto`: Gestão de itens do estoque
- `Venda`: Registro de transações comerciais
- `ItemVenda`: Itens associados a cada venda
- `Fluxo_Caixa`: Controle de entradas e saídas
- `MetricasFinanceiras`: Indicadores e métricas
- `Transacao`: Registro de movimentações financeiras

## Tarefas Agendadas

O projeto inclui tarefas agendadas via Celery para:

- Exportação diária de dados (23:55)
- Cálculo de métricas financeiras
- Geração de relatórios periódicos

## Licença

[Inserir informação sobre licença aqui]

## Contato

Para mais informações, entre em contato com [seu email ou equipe].