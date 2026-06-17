# Prompt de Redesign de UI — Monitor de Plantas

> Copie este documento inteiro e cole no chat do Replit Agent.

---

## Contexto

Este é um sistema web Flask com Jinja2 chamado **Monitor de Plantas**. O sistema está funcional (MVP completo), mas a interface precisa ser completamente reestilizada. Não altere nenhuma lógica Python, rotas, variáveis Jinja2 (`{{ }}`, `{% %}`), nomes de formulários, métodos de formulário ou URLs. **Apenas a camada visual (HTML/CSS) deve ser modificada.**

---

## Estilo visual alvo

**Frutiger Aero com Liquid Glass.**

Características obrigatórias:
- Fundo com gradiente suave em tons de verde e azul-água (exemplo: `#a8edca → #c3f0d8 → #e8f8f5`)
- Painéis e cards com efeito glassmorphism: `background: rgba(255,255,255,0.18)`, `backdrop-filter: blur(24px)`, borda `rgba(255,255,255,0.35)`
- Navbar translúcida com blur
- Bordas arredondadas generosas (`border-radius: 1.25rem` a `1.5rem`)
- Sombras suaves (`box-shadow: 0 8px 32px rgba(31,38,135,0.12)`)
- Tipografia limpa: fonte `Inter` via Google Fonts, ou `system-ui` como fallback
- Paleta de acentos em verde-esmeralda (`#10b981`, `#059669`) e branco translúcido

**Referência visual:** iOS 26 Liquid Glass, Frutiger Aero (Windows Vista era), glassmorphism.

---

## Dependências a adicionar

### No `<head>` do `base.html`:

```html
<!-- Tailwind CSS via CDN (sem build step) -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Google Fonts: Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Remover:
- Qualquer `<link>` para `style.css` estático existente (substituído por Tailwind + estilos inline no `base.html`)

---

## Classes CSS customizadas

Adicione este bloco `<style>` dentro do `base.html`, **antes do `</head>`**:

```css
<style>
  * { font-family: 'Inter', system-ui, sans-serif; }

  body {
    background: linear-gradient(135deg, #a8edca 0%, #c3f0d8 40%, #e0f7f0 100%);
    min-height: 100vh;
    background-attachment: fixed;
  }

  .glass-card {
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 1.25rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.12);
  }

  .glass-nav {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.4);
    position: sticky;
    top: 0;
    z-index: 50;
  }

  .glass-btn-primary {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border-radius: 0.75rem;
    padding: 0.5rem 1.25rem;
    font-weight: 600;
    transition: opacity 0.2s;
    border: none;
    cursor: pointer;
  }
  .glass-btn-primary:hover { opacity: 0.85; }

  .glass-btn-secondary {
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.75rem;
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    color: #065f46;
    transition: background 0.2s;
    cursor: pointer;
  }
  .glass-btn-secondary:hover { background: rgba(255, 255, 255, 0.5); }

  .glass-input {
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.75rem;
    padding: 0.5rem 1rem;
    width: 100%;
    outline: none;
    transition: border-color 0.2s;
  }
  .glass-input:focus {
    border-color: #10b981;
    background: rgba(255, 255, 255, 0.5);
  }

  .status-ok {
    background: rgba(16, 185, 129, 0.15);
    color: #065f46;
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 9999px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .status-alerta {
    background: rgba(245, 158, 11, 0.15);
    color: #92400e;
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 9999px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
  }
</style>
```

---

## Estrutura do `base.html`

Reescreva o `base.html` com esta estrutura, mantendo os blocos Jinja2 existentes (`{% block content %}`, `{% block title %}`, etc.):

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Monitor de Plantas{% endblock %}</title>
  <!-- [Tailwind CDN aqui] -->
  <!-- [Google Fonts aqui] -->
  <!-- [Bloco <style> com classes glass aqui] -->
</head>
<body>

  <!-- NAVBAR -->
  <nav class="glass-nav px-6 py-3 flex items-center justify-between">
    <span class="text-green-800 font-bold text-lg">🌿 Monitor de Plantas</span>
    <div class="flex gap-4 items-center">
      <a href="/plantas/" class="text-green-700 font-medium hover:text-green-900 transition-colors">Minhas Plantas</a>
      <a href="/alertas/" class="text-amber-700 font-medium hover:text-amber-900 transition-colors">⚠ Alertas</a>
      <a href="/colaborador/logout" class="glass-btn-secondary text-sm">Sair</a>
    </div>
  </nav>

  <!-- CONTEÚDO PRINCIPAL -->
  <main class="max-w-5xl mx-auto px-4 py-8">
    {% block content %}{% endblock %}
  </main>

</body>
</html>
```

---

## Instruções por template

Ao refatorar cada template abaixo, siga estas regras:
1. Envolva o conteúdo principal em `<div class="glass-card p-6 mb-6">`
2. Use `glass-input` em todos os `<input>` e `<select>` e `<textarea>`
3. Use `glass-btn-primary` em botões de ação principal (salvar, cadastrar, registrar)
4. Use `glass-btn-secondary` em botões secundários (cancelar, voltar)
5. Use `status-ok` e `status-alerta` nos badges de status das plantas
6. Use Tailwind para espaçamentos, grid e tipografia (não CSS puro)
7. **Nunca remova ou altere variáveis Jinja2, `action=`, `method=`, `name=` de inputs**

### `login.html` e `cadastro.html`
- Card centralizado: `max-w-sm mx-auto mt-20 glass-card p-8`
- Título com ícone de planta
- Campos com `glass-input` e labels acima

### `plantas.html`
- Grid responsivo: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4`
- Cada planta em um `glass-card p-4`
- Badge de status (`status-ok` / `status-alerta`) no canto superior direito do card
- Botão "Nova Planta" no topo direito com `glass-btn-primary`

### `nova_planta.html` e `editar_planta.html`
- Formulário em `glass-card p-6 max-w-xl mx-auto`
- Seção de busca de espécie destacada com `glass-card` interno aninhado

### `detalhe_planta.html`
- Header com nome da planta e badge de status
- Seção de histórico de cuidados como lista dentro de `glass-card`
- Cada registro de cuidado como `glass-card p-3 mb-2`

### `novo_registro.html`
- Formulário compacto em `glass-card p-6 max-w-md mx-auto`
- `<select>` de tipo de cuidado com `glass-input`

### `alertas.html`
- Lista de plantas em alerta em grid `grid-cols-1 sm:grid-cols-2 gap-4`
- Cada card com borda de destaque: `border-amber-300`
- Botão de rega rápida com `glass-btn-primary` dentro do card

---

## Responsividade

- Navbar: em telas pequenas, oculte os textos dos links e mostre apenas ícones, ou empilhe verticalmente com `flex-col sm:flex-row`
- Grids: sempre `grid-cols-1` como base, expandindo em `sm:` e `lg:`
- Padding do `<main>`: `px-4 sm:px-6 lg:px-8`

---

## O que NÃO fazer

- ❌ Não altere nenhum arquivo `.py`
- ❌ Não mude nomes de rotas ou URLs
- ❌ Não remova atributos `name=""` dos inputs de formulário
- ❌ Não substitua `{% block %}`, `{% for %}`, `{% if %}` do Jinja2
- ❌ Não adicione JavaScript que altere comportamento de formulários
- ❌ Não use Bootstrap — apenas Tailwind + as classes `.glass-*` definidas acima
