# Plano de Implementação — Monitor de Plantas

## Situação Atual

O projeto está com estrutura MVC criada mas **totalmente vazia**. Todos os modelos, serviços e templates precisam ser implementados. Os controllers existem como esqueleto com rotas retornando strings de placeholder.

---

## Bloco 1 — Models (Camada de Domínio)

### `models/usuario.py` — Classe `Colaborador` (RF01)
- Atributos: `id`, `nome`, `email`, `senha_hash`
- Método `verificar_senha()` para autenticação
- Serialização/deserialização JSON

### `models/cuidado.py` — Hierarquia OO com herança (RNF09)
- Classe base `Cuidado`: `id`, `tipo`, `data`, `observacao`
- Subclasses: `Rega`, `Adubacao`, `Poda` (cada uma com `tipo` fixo)

### `models/planta.py` — Classe `Planta` (RF05–RF14)
- Atributos: `id`, `nome`, `especie` (dict do JSON da API), `frequencia_rega`, `colaborador_id`, `historico_cuidados` (lista de `Cuidado`), `log_edicoes`
- Método `dias_sem_cuidado()` → calcula dias desde o último cuidado (RF09)
- Método `precisa_cuidado()` → compara com `frequencia_rega` (RF10, RF18)
- Método `registrar_cuidado(cuidado)` → atualiza histórico (RF16)

### `models/alerta.py` — Classe `Alerta` (RF18–RF20)
- Derivado dinamicamente das plantas (não persistido separadamente)
- Representa uma planta que ultrapassou o intervalo de rega

---

## Bloco 2 — Services (Persistência e API Externa)

### `services/repositorio.py` — Persistência JSON (RNF05)
- `carregar_colaboradores()` / `salvar_colaboradores()`
- `carregar_plantas()` / `salvar_plantas()`
- Arquivos de dados: `data/colaboradores.json`, `data/plantas.json`
- Instanciação de objetos a partir dos dicts JSON

### `services/especie_service.py` — Integração com API externa (RF02)
- `buscar_especies(query)` → consulta API de plantas
- `obter_especie(id)` → retorna `{nome_comum, nome_cientifico, frequencia_rega, luz, temp_minima}`
- Tratamento de erros e fallback

---

## Bloco 3 — Controllers (Rotas e Lógica)

### `colaborador_controller.py` (RF01, RNF02)
- `GET/POST /colaborador/login` → autenticação com `session` do Flask
- `GET/POST /colaborador/cadastro` → criação de colaborador
- `GET /colaborador/logout` → limpa sessão
- Decorator `@login_required` para proteger todas as rotas privadas

### `planta_controller.py` (RF05–RF14)
- `GET /plantas/` → lista plantas do colaborador logado
- `GET/POST /plantas/nova` → formulário com busca de espécie via API
- `GET /plantas/<id>` → detalhes + histórico de cuidados
- `GET/POST /plantas/<id>/editar` → edição com log de alterações (RF14)
- Validação de propriedade da planta (RF12)

### `registro_controller.py` (RF15–RF17)
- `GET/POST /registros/planta/<id>/novo` → formulário de cuidado (tipo + data + observação)
- `GET /registros/planta/<id>` → histórico completo da planta

### `alerta_controller.py` (RF18–RF20)
- `GET /alertas/` → lista plantas que precisam de cuidado
- `POST /alertas/rega-rapida/<id>` → registra rega diretamente do painel (RF20)

---

## Bloco 4 — Templates (Interface Jinja2)

| Template | Descrição |
|---|---|
| `base.html` | Layout base com navbar (Plantas / Alertas / Logout) |
| `login.html` | Formulário de login |
| `cadastro.html` | Formulário de cadastro de colaborador |
| `plantas.html` | Lista com badge "OK" / "Precisa de Cuidado" (RF10, RNF14) |
| `nova_planta.html` | Formulário com busca de espécie via API (RF03, RF04) |
| `detalhe_planta.html` | Detalhes + histórico de cuidados (RF08, RF17) |
| `editar_planta.html` | Formulário de edição (RF11) |
| `novo_registro.html` | Formulário de cuidado: rega / adubação / poda (RF15) |
| `alertas.html` | Painel de alertas com botão de rega rápida (RF19, RF20) |

---

## Bloco 5 — Estilo (CSS)

### `static/style.css`
- Indicadores visuais: `.status-ok` (verde) e `.status-alerta` (vermelho/laranja) (RNF14)
- Layout responsivo simples para uso interno em navegador

---

## Bloco 6 — Infraestrutura

- `requirements.txt` → adicionar `requests` para chamadas à API externa
- `data/` → criar diretório com arquivos JSON iniciais vazios (`colaboradores.json`, `plantas.json`)
- `.replit` → garantir workflow configurado para executar `app.py`

---

## Rastreabilidade de Requisitos

| Requisito | Bloco / Arquivo |
|---|---|
| RF01 — Cadastro de colaborador | Bloco 1 (`usuario.py`) + Bloco 3 (`colaborador_controller`) |
| RF02 — Consulta de espécies via API | Bloco 2 (`especie_service.py`) |
| RF03 — Associar espécie a planta | Bloco 3 (`planta_controller`) + Bloco 4 (`nova_planta.html`) |
| RF04 — Frequência de rega sugerida como padrão | Bloco 3 (`planta_controller`) |
| RF05 — Cadastro de planta | Bloco 1 (`planta.py`) + Bloco 3 (`planta_controller`) |
| RF06 — Planta associada ao colaborador logado | Bloco 3 (`planta_controller`) |
| RF07 — Listar plantas do colaborador | Bloco 3 (`planta_controller`) + Bloco 4 (`plantas.html`) |
| RF08 — Detalhes de uma planta | Bloco 3 (`planta_controller`) + Bloco 4 (`detalhe_planta.html`) |
| RF09 — Dias desde último cuidado | Bloco 1 (`planta.py` — método `dias_sem_cuidado()`) |
| RF10 — Indicador visual de status | Bloco 1 (`planta.py`) + Bloco 4 + Bloco 5 |
| RF11 — Edição de planta | Bloco 3 (`planta_controller`) + Bloco 4 (`editar_planta.html`) |
| RF12 — Apenas dono pode editar | Bloco 3 (`planta_controller` — validação de propriedade) |
| RF13 — Edições afetam cálculos futuros | Bloco 2 (`repositorio.py`) + Bloco 1 (`planta.py`) |
| RF14 — Log de edições | Bloco 1 (`planta.py`) + Bloco 3 (`planta_controller`) |
| RF15 — Registro de cuidado | Bloco 1 (`cuidado.py`) + Bloco 3 (`registro_controller`) |
| RF16 — Atualizar data do último cuidado | Bloco 1 (`planta.py` — método `registrar_cuidado()`) |
| RF17 — Histórico de cuidados | Bloco 3 (`registro_controller`) + Bloco 4 (`detalhe_planta.html`) |
| RF18 — Geração automática de alertas | Bloco 1 (`planta.py` — método `precisa_cuidado()`) |
| RF19 — Painel de alertas | Bloco 3 (`alerta_controller`) + Bloco 4 (`alertas.html`) |
| RF20 — Rega rápida pelo painel | Bloco 3 (`alerta_controller`) |
| RNF01–RNF03 — Autenticação e isolamento | Sessions Flask + decorator `login_required` |
| RNF05 — Persistência JSON | Bloco 2 (`repositorio.py`) |
| RNF06 — API externa | Bloco 2 (`especie_service.py`) |
| RNF08 — Arquitetura MVC | Estrutura de pastas existente |
| RNF09 — Herança em cuidados | Bloco 1 (`cuidado.py` — `Rega`, `Adubacao`, `Poda`) |
| RNF10 — CSS dinâmico via Jinja2 | Bloco 4 + Bloco 5 |
| RNF11 — Docstrings PEP 257 | Aplicar em todas as classes e métodos públicos |
| RNF14 — Indicadores visuais claros | Bloco 4 + Bloco 5 |
| RNF15 — Alertas na navegação principal | Bloco 4 (`base.html`) |
| RNF16 — Histórico imutável | Sem rotas de edição/exclusão em registros |
