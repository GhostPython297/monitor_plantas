# 🌱 Monitor de Plantas

Projeto acadêmico desenvolvido para a disciplina de **Análise e Projeto de Sistema** do curso de Análise e Desenvolvimento de Sistemas no **IFPB**.

O sistema é uma aplicação web para monitoramento de plantas domésticas e de jardim. Usuários podem cadastrar suas plantas, registrar cuidados (rega, adubação e poda) e receber alertas automáticos quando uma planta estiver precisando de atenção.

---

## 📋 Índice

- [Sobre o projeto](#-sobre-o-projeto)
- [Instalação](#-instalação)
- [Como executar](#-como-executar)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Exemplos de uso](#-exemplos-de-uso)

---

## 🌿 Sobre o projeto

O Monitor de Plantas acompanha a frequência de rega configurada para cada planta e gera alertas automáticos sempre que o intervalo for ultrapassado.

**Principais funcionalidades:**

- Cadastro de plantas com nome, espécie e frequência de rega
- Registro de cuidados com histórico completo e imutável
- Painel de alertas com ação rápida de rega diretamente na tela
- Indicadores visuais de saúde (✅ OK / ⚠️ Precisa de cuidado)
- Log de alterações para cada planta editada

**Stack utilizada:**

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 + Flask |
| Persistência | Arquivos JSON |
| Frontend | Jinja2 + CSS puro |
| Arquitetura | MVC |

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Opção 1 — Script automático (recomendado)

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/GhostPython297/monitor_plantas.git
cd monitor_plantas
pip install -r requirements.txt
```

### Opção 2 — Instalação manual das dependências

Se preferir instalar a dependência diretamente:

```bash
pip install flask
```

> O projeto utiliza apenas Flask como dependência externa. Todas as demais bibliotecas (`json`, `os`, `datetime`) são nativas do Python 3.

---

## ▶️ Como executar

Com as dependências instaladas, execute na raiz do projeto:

```bash
python app.py
```

Acesse no navegador:

```
http://localhost:5000
```

> O servidor roda em modo `debug=True` por padrão, adequado para ambiente de desenvolvimento.

---

## 📁 Estrutura de pastas

```
monitor_plantas/
│
├── app.py                  # Controller — rotas Flask
├── requirements.txt        # Dependências do projeto
├── CLAUDE.md               # Contexto do projeto para IAs
│
├── models/                 # Camada Model (orientação a objetos)
│   ├── __init__.py
│   ├── planta.py           # Classe Planta
│   ├── cuidado.py          # Classes Cuidado, Rega, Adubação, Poda (herança)
│   ├── usuario.py          # Classe Usuario
│   └── alerta.py           # Classe Alerta
│
├── services/               # Camada de serviços (persistência JSON)
│   ├── __init__.py
│   └── repositorio.py      # Leitura e escrita nos arquivos JSON
│
├── templates/              # Camada View (HTML + Jinja2)
│   ├── base.html           # Layout base com navegação
│   ├── plantas.html        # Lista de plantas do usuário
│   ├── nova_planta.html    # Formulário de cadastro
│   └── alertas.html        # Painel de alertas
│
├── static/
│   └── style.css           # Estilização global
│
└── planejamento/           # Documentação da disciplina
    ├── MINIMUNDO.md
    ├── REQUISITOS.md
    ├── DECISOES.md
    └── CONTRIBUICAO.md
```

---

## 💡 Exemplos de uso

### Cadastrar uma nova planta

1. Acesse **Minhas Plantas** na navegação principal
2. Clique em **Nova Planta**
3. Preencha o nome (ex: `Samambaia`), a espécie (ex: `Nephrolepis exaltata`) e a frequência de rega em dias (ex: `3`)
4. Confirme o cadastro — a planta aparecerá na listagem com status **✅ OK**

---

### Registrar um cuidado

1. Na lista de plantas, clique na planta desejada para ver seus detalhes
2. Clique em **Registrar Cuidado**
3. Selecione o tipo: `Rega`, `Adubação` ou `Poda`
4. Informe a data e, opcionalmente, uma observação (ex: `"Regada com água filtrada"`)
5. O sistema atualiza automaticamente a data do último cuidado e recalcula o status

---

### Consultar o painel de alertas

1. Acesse **Alertas** na navegação principal
2. Todas as plantas que ultrapassaram o intervalo de rega configurado aparecem listadas
3. Clique em **Regar agora** para registrar uma rega diretamente, sem sair da tela

---

### Editar dados de uma planta

1. Na lista de plantas, clique na planta desejada
2. Clique em **Editar**
3. Altere o nome, espécie ou frequência de rega
4. Salve — as mudanças são aplicadas imediatamente e um log da alteração é registrado

> ⚠️ O histórico de cuidados **não pode ser editado ou removido** após o registro.

---

## 🤝 Contribuindo

Consulte o arquivo [`planejamento/CONTRIBUICAO.md`](planejamento/CONTRIBUICAO.md) para entender o fluxo de trabalho com Issues e Pull Requests no GitHub Projects.
