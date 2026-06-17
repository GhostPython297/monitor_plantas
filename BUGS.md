# Relatório de Bugs — Monitor de Plantas

> Gerado em: 17/06/2026  
> Método: análise estática do código + execução do script `testar_backend.py` + inspeção dos logs da aplicação

---

## 🔴 Críticos

### BUG-01 — Loop de redirecionamento: login não persiste a sessão

**Arquivo:** `app.py` (linhas 15–16)

**Descrição:**  
As configurações `SESSION_COOKIE_SAMESITE = "None"` e `SESSION_COOKIE_SECURE = True` fazem com que o navegador só envie o cookie de sessão em conexões HTTPS. Em ambiente de desenvolvimento local (HTTP), o cookie nunca é transmitido de volta ao servidor após o login. Isso causa o loop confirmado nos logs:

```
POST /colaborador/login → 302 /plantas/
GET  /plantas/          → 302 /colaborador/login   ← sessão perdida
```

**Evidência nos logs:**
```
POST /colaborador/login HTTP/1.1" 302 -
GET /plantas/ HTTP/1.1" 302 -
GET /colaborador/login HTTP/1.1" 200 -
```

**Correção sugerida:**  
Condicionar `SESSION_COOKIE_SECURE` e `SESSION_COOKIE_SAMESITE` ao ambiente:
```python
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

---

### BUG-02 — `precisa_cuidado()` usa qualquer tipo de cuidado como referência de rega

**Arquivo:** `models/planta.py` (linhas 52–84)

**Descrição:**  
O método `_data_ultimo_cuidado()` retorna a data do cuidado mais recente **independente do tipo** (rega, adubação, poda). No entanto, o atributo que controla o intervalo é `frequencia_rega`. Isso faz com que uma poda ou adubação "zere" o contador de rega incorretamente: uma planta que recebeu adubação ontem, mas não é regada há 15 dias, aparecerá como "OK" se `frequencia_rega = 7`.

**Trecho problemático:**
```python
def _data_ultimo_cuidado(self) -> Optional[date]:
    if not self.historico_cuidados:
        return None
    return max(c.data for c in self.historico_cuidados)  # qualquer tipo
```

**Correção sugerida:**  
Filtrar apenas registros do tipo `"rega"` ao calcular a data de referência para rega.

---

## 🟠 Alta Prioridade

### BUG-03 — Frequência de rega aceita valores zero ou negativos

**Arquivos:** `controllers/planta_controller.py` (linhas 70–73) e `controllers/planta_controller.py` (linhas 132–138)

**Descrição:**  
O backend converte `frequencia_rega` para `int` mas não valida se o valor é maior que zero. Se alguém enviar `frequencia_rega=0` (burlando o `min="1"` do HTML), a condição `dias >= 0` em `precisa_cuidado()` será sempre `True`, marcando a planta como urgente para sempre. Valores negativos também são aceitos silenciosamente.

**Trecho problemático (nova planta):**
```python
try:
    frequencia = int(frequencia_raw)
except ValueError:
    frequencia = 7
# sem checagem de frequencia <= 0
```

**Correção sugerida:**  
Adicionar `if frequencia <= 0: frequencia = 7` (ou retornar erro ao usuário).

---

### BUG-04 — Hashing de senha sem salt (SHA-256 puro)

**Arquivo:** `models/usuario.py` (linhas 31–41)

**Descrição:**  
As senhas são armazenadas como `hashlib.sha256(senha.encode()).hexdigest()`, sem salt. Isso torna o sistema vulnerável a ataques de rainbow table: qualquer hash de senha comum pode ser revertido consultando tabelas pré-computadas publicamente disponíveis.

**Trecho problemático:**
```python
return hashlib.sha256(senha.encode("utf-8")).hexdigest()
```

**Correção sugerida:**  
Usar `werkzeug.security.generate_password_hash` / `check_password_hash`, que já inclui salt e algoritmo moderno (PBKDF2/scrypt).

---

### BUG-05 — Chave secreta da sessão hardcoded no código-fonte

**Arquivo:** `app.py` (linha 14)

**Descrição:**  
`app.secret_key = "chave-secreta-dev"` está embutida diretamente no código. Qualquer pessoa com acesso ao repositório consegue forjar ou decodificar cookies de sessão Flask.

**Correção sugerida:**  
```python
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
```

---

## 🟡 Média Prioridade

### BUG-06 — Busca de espécie retorna catálogo completo sem indicar ausência de resultados

**Arquivo:** `services/especie_service.py` (linhas 179–193)

**Descrição:**  
Quando o termo buscado não corresponde a nenhuma espécie do catálogo local, `_buscar_fallback` retorna **todas as 5 espécies** silenciosamente, sem nenhuma mensagem de "nenhum resultado encontrado". O usuário pode acreditar que todos os resultados são relevantes para a busca.

**Trecho problemático:**
```python
return [
    esp for esp in _FALLBACK_ESPECIES
    if termo in esp["nome_comum"].lower() or termo in esp["nome_cientifico"].lower()
] or _FALLBACK_ESPECIES  # retorna tudo se lista vazia
```

**Correção sugerida:**  
Retornar lista vazia quando não há match e exibir mensagem "Nenhuma espécie encontrada" no template.

---

### BUG-07 — Datas futuras são aceitas em registros de cuidado

**Arquivo:** `controllers/registro_controller.py` (linhas 43–49)

**Descrição:**  
O backend não valida se a data informada no formulário é anterior ou igual à data atual. É possível registrar um cuidado com data de amanhã ou qualquer data futura, o que faria `precisa_cuidado()` retornar `False` (planta "OK") para uma planta que ainda não foi cuidada.

**Trecho problemático:**
```python
try:
    data_cuidado = date.fromisoformat(data_str)
except ValueError:
    data_cuidado = date.today()
# sem validação: data_cuidado <= date.today()
```

**Correção sugerida:**  
Adicionar `if data_cuidado > date.today(): data_cuidado = date.today()` ou retornar erro de validação.

---

### BUG-08 — Seleção de espécie perdida ao submeter formulário com erro de validação

**Arquivo:** `controllers/planta_controller.py` (linhas 64–66) + `templates/nova_planta.html`

**Descrição:**  
Quando `acao == "salvar"` falha por nome vazio, o template é renderizado sem a variável `especie_selecionada`:
```python
flash("O nome da planta é obrigatório.", "erro")
return render_template("nova_planta.html")  # sem especie_selecionada
```
A espécie que o usuário havia selecionado na etapa anterior é perdida, forçando-o a repetir o processo de busca e seleção desde o início.

**Correção sugerida:**  
Recuperar a espécie pelo `especie_id` do formulário e passá-la novamente ao template no render de erro.

---

### BUG-09 — Rota `registro.historico` duplicada e inacessível pela interface

**Arquivo:** `controllers/registro_controller.py` (linhas 67–84)

**Descrição:**  
A rota `GET /registros/planta/<planta_id>` renderiza o mesmo template `detalhe_planta.html` que `planta.detalhes`, com lógica praticamente idêntica. Nenhum template tem link para essa rota, tornando-a código morto. A duplicidade pode causar inconsistências futuras se uma das cópias for atualizada sem a outra.

**Correção sugerida:**  
Remover a rota `registro.historico` e centralizar a exibição do histórico em `planta.detalhes`.

---

## 🔵 Baixa Prioridade / Qualidade de Código

### BUG-10 — Acesso direto a método privado `_hash_senha` fora da classe

**Arquivo:** `controllers/colaborador_controller.py` (linha 131)

**Descrição:**  
O perfil do colaborador acessa diretamente o método convencionalmente privado da classe:
```python
colaborador.senha_hash = Colaborador._hash_senha(nova_senha)
```
Isso viola o encapsulamento e acopla o controller a detalhes internos do modelo.

**Correção sugerida:**  
Adicionar um método público `colaborador.set_senha(nova_senha)` na classe `Colaborador`.

---

### BUG-11 — Ausência de proteção CSRF nos formulários

**Arquivos:** todos os templates com `<form method="POST">`

**Descrição:**  
Nenhum formulário utiliza token CSRF. Isso permite ataques Cross-Site Request Forgery — por exemplo, uma página externa pode induzir um usuário autenticado a excluir sua própria conta (`POST /colaborador/excluir`) ou registrar cuidados.

**Correção sugerida:**  
Integrar `Flask-WTF` e usar `{{ form.hidden_tag() }}` nos formulários, ou implementar proteção CSRF manual com token na sessão.

---

## Resumo

| ID      | Severidade | Descrição resumida                                        |
|---------|------------|-----------------------------------------------------------|
| BUG-01  | 🔴 Crítico  | Loop de login — cookie Secure bloqueado em HTTP           |
| BUG-02  | 🔴 Crítico  | `precisa_cuidado()` usa poda/adubação como referência de rega |
| BUG-03  | 🟠 Alta     | Frequência de rega aceita zero ou negativo                |
| BUG-04  | 🟠 Alta     | SHA-256 sem salt para hashing de senhas                   |
| BUG-05  | 🟠 Alta     | Chave secreta hardcoded no código-fonte                   |
| BUG-06  | 🟡 Média    | Busca sem resultado retorna catálogo inteiro sem aviso    |
| BUG-07  | 🟡 Média    | Datas futuras aceitas em registros de cuidado             |
| BUG-08  | 🟡 Média    | Espécie selecionada perdida ao corrigir erro no formulário|
| BUG-09  | 🟡 Média    | Rota `registro.historico` duplicada e inacessível         |
| BUG-10  | 🔵 Baixa    | Acesso direto a método privado `_hash_senha`              |
| BUG-11  | 🔵 Baixa    | Ausência de proteção CSRF nos formulários                 |
