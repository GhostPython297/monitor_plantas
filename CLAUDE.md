# Monitor de plantas

Sistema de monitoramento de plantas com Flask e Python OO.

## Stack

- **Python 3 + Flask** — leve e adequado para projetos pequenos/médios
- **Persistência em JSON** — formato simples, sem complexidade de banco relacional
- **Frontend com Jinja2 + CSS puro**
- **Arquitetura MVC** — models (entidades), services (persistência), rotas como controllers

## Estrutura

- models/ → classes Planta, Cuidado, Usuario, Alerta
- services/ → Repositorio (persistência)
- templates/ → HTMLs do Flask
- app.py → rotas (Controller)
- docs/ → decisões e contexto do projeto (acessível à equipe e IA)

## Metodologia

- **Kanban** em vez de Scrum (workflow flexível para equipe pequena)
- **GitHub Projects** para rastreamento de tarefas

## Convenções

- Classes em português
- Métodos em snake_case
- Sem autenticação, uploads de fotos ou notificações por email (fora do escopo)
