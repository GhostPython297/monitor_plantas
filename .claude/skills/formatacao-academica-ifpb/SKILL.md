---
name: formatacao-academica-ifpb
description: >
  Formata documentos acadêmicos no estilo preferido do usuário: cabeçalho simples com nome do instituto
  e campus, títulos em negrito sem numeração e sem cor, corpo em Times New Roman 12pt justificado com
  espaçamento 1,5, listas com marcadores ou numeradas conforme o conteúdo. Estilo limpo inspirado em
  Markdown renderizado — sem ornamentos visuais, tabelas decorativas ou cores. Use esta skill sempre
  que o usuário pedir para formatar, organizar ou padronizar um documento de atividade, trabalho ou
  relatório acadêmico, mesmo que não mencione IFPB explicitamente.
---

# Formatação Acadêmica — Estilo Pessoal

## Contexto

Este é o estilo preferido do usuário para documentos acadêmicos entregues no IFPB Campus Esperança,
curso de Análise e Desenvolvimento de Sistemas. O objetivo é um visual limpo e legível, próximo de
um Markdown bem formatado — sem excessos visuais.

---

## Estrutura do Documento

### 1. Cabeçalho

Simples, centralizado, no topo da página, sem logo:

```
Instituto Federal de Educação, Ciência e Tecnologia da Paraíba  [negrito]
Campus Esperança
```

Seguido de uma **linha horizontal** (`BorderStyle.SINGLE`, espessura 6, preta) separando o cabeçalho
do corpo.

Em seguida, o **título do trabalho** centralizado e em negrito (tamanho 32).

### 2. Página

- Tamanho: **A4** (11906 × 16838 DXA)
- Margens: topo 3 cm (1701), esquerda 3 cm (1701), direita/baixo 2 cm (1134)

### 3. Tipografia do corpo

- Fonte: **Times New Roman**
- Tamanho: **12pt (size: 24)**
- Espaçamento entre linhas: **1,5 (line: 360)**
- Alinhamento: **justificado**
- Recuo de primeira linha: **720 DXA** (0,5 polegada)
- Espaço após parágrafo: **160 DXA**

### 4. Títulos

- **H1**: Times New Roman, 14pt (size: 28), negrito, preto — sem numeração, sem cor
- **H2**: Times New Roman, 12pt (size: 24), negrito, preto — sem numeração, sem cor
- Espaçamento H1: `before: 320, after: 120`
- Espaçamento H2: `before: 200, after: 80`

> ⚠️ Nunca adicionar numeração automática nem cor diferente de preto nos títulos.

### 5. Listas

Usar `LevelFormat.BULLET` para listas com marcador (•) e `LevelFormat.DECIMAL` para numeradas.
**Nunca usar caracteres unicode de bullet diretamente.**

- Indent: `left: 720, hanging: 360`
- Espaçamento: `after: 100, line: 320`

Quando um item de lista tiver **termo em destaque seguido de explicação**, usar bold apenas no termo:
```javascript
[run("Termo: ", true), run("explicação normal.")]
```

---

## Fluxo de Trabalho

1. Ler o conteúdo do arquivo enviado com `pandoc` ou descompactando o `.odt`/`.docx`
2. Identificar a estrutura: título principal, seções (H1), subseções (H2), parágrafos, listas
3. Gerar o `.docx` com `docx` (npm), seguindo exatamente as especificações acima
4. Validar com `python scripts/office/validate.py`
5. Entregar em `/mnt/user-data/outputs/` com o mesmo nome do arquivo original

---

## O que NÃO fazer

- ❌ Não adicionar logo ou imagem no cabeçalho
- ❌ Não usar cores nos títulos (apenas preto)
- ❌ Não numerar títulos automaticamente (ex: "1. Introdução")
- ❌ Não usar tabelas decorativas no cabeçalho
- ❌ Não usar fonte diferente de Times New Roman no corpo
- ❌ Não usar `\n` — sempre criar `Paragraph` separados
- ❌ Não usar unicode bullets — usar `LevelFormat.BULLET`
