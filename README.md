# TaskFlow Pro

> Sistema de gerenciamento de tarefas pessoais com autenticação, categorias, filtros e alertas de prazo.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=flat-square)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square)

🔗 **[Acesse o projeto ao vivo](https://taskflow-pro-6p1g.onrender.com)**

---

## Sobre o projeto

TaskFlow Pro é uma aplicação web full stack para organização de tarefas pessoais. Cada usuário possui sua própria conta e visualiza apenas suas próprias tarefas, com suporte a categorias, prioridades, prazos e alertas visuais.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento web, separação de responsabilidades e experiência de usuário limpa e responsiva.

---

## Funcionalidades

- **Autenticação completa** — cadastro, login e logout com senhas em hash (bcrypt)
- **CRUD de tarefas** — criar, editar, visualizar e deletar tarefas
- **Status** — pendente, em andamento e concluída com transições controladas
- **Prioridades** — baixa, média e alta com badges visuais
- **Categorias** — Geral, Pessoal, Trabalho e Estudos
- **Prazos opcionais** — com bloqueio de datas retroativas
- **Alertas de prazo** — destaque visual para tarefas vencidas e que vencem hoje
- **Contador de alertas** — badge na navbar com total de tarefas em atraso
- **Filtros combinados** — por status, prioridade e categoria simultaneamente
- **Ordenação** — por data de criação, prazo ou prioridade
- **Busca por título** — pesquisa em tempo real na lista de tarefas
- **Dashboard** — cards de resumo e barra de progresso geral
- **Design responsivo** — funciona em desktop e mobile

---

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.11, Flask |
| ORM | SQLAlchemy |
| Banco de dados | PostgreSQL (produção) / SQLite (desenvolvimento) |
| Frontend | Jinja2, Bootstrap 5, Bootstrap Icons |
| Autenticação | Werkzeug (hash de senhas) |
| Servidor WSGI | Gunicorn |
| Deploy | Render |

---

## Como rodar localmente

**Pré-requisitos:** Python 3.10+

```bash
# Clone o repositório
git clone https://github.com/EduardoFioreti/taskflow-pro.git
cd taskflow-pro

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
python app.py
```

Acesse em: `http://localhost:5000`

---

## Estrutura do projeto

```
taskflow-pro/
├── app.py              # Rotas e lógica da aplicação
├── models.py           # Modelos do banco de dados
├── requirements.txt    # Dependências do projeto
├── Procfile            # Configuração do servidor (Render)
└── templates/
    ├── base.html       # Layout base (navbar, flash messages)
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── tarefas.html
    ├── nova_tarefa.html
    └── editar_tarefa.html
```

---

## Deploy

A aplicação está em produção no **Render** com PostgreSQL. As variáveis de ambiente necessárias são:

| Variável | Descrição |
|----------|-----------|
| `DATABASE_URL` | URL de conexão com o PostgreSQL |
| `SECRET_KEY` | Chave secreta da sessão Flask |

---

## Autor

**Eduardo Fioreti**  
Estudante de Engenharia da Computação — UniCEUMA  
Analista de Suporte N1/N2 & Especialista ERP — Cads Informática  
Diretor Financeiro — Seeds Tecnologia

[![GitHub](https://img.shields.io/badge/GitHub-EduardoFioreti-181717?style=flat-square&logo=github)](https://github.com/EduardoFioreti)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Eduardo%20Fioreti-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/eduardofioreti)
