# JavaScript / Node.js — Terminal Output Style Reference

No external dependencies needed — uses only `process.stdout` and template literals.

## ANSI constants

```js
const RESET    = "\x1b[0m";
const BOLD     = "\x1b[1m";
const VERDE    = "\x1b[32m";
const AMARELO  = "\x1b[33m";
const AZUL     = "\x1b[34m";
const CIANO    = "\x1b[36m";
const VERMELHO = "\x1b[31m";
const CINZA    = "\x1b[90m";
```

## Helper functions

```js
function cabecalho(titulo) {
  const w = 52;
  const linha = "═".repeat(w);
  const pad = " ".repeat(Math.max(0, Math.floor((w - titulo.length) / 2)));
  console.log();
  console.log(`${CIANO}${BOLD}╔${linha}╗${RESET}`);
  console.log(`${CIANO}${BOLD}║${RESET}${BOLD}${pad}${titulo.padEnd(w)}${RESET}${CIANO}${BOLD}║${RESET}`);
  console.log(`${CIANO}${BOLD}╚${linha}╝${RESET}`);
}

function secao(nome) {
  const tracas = "─".repeat(Math.max(0, 44 - nome.length));
  console.log(`\n${AZUL}${BOLD}┌─ ${nome} ${tracas}${RESET}`);
}

const ok       = (msg) => console.log(`${VERDE}  ✔ ${RESET}${msg}`);
const aviso    = (msg) => console.log(`${AMARELO}  ⚠  ${RESET}${msg}`);
const erro     = (msg) => console.log(`${VERMELHO}  ✖ ${RESET}${msg}`);
const separador = ()   => console.log(`${CINZA}  ${"·".repeat(48)}${RESET}`);

function info(rotulo, valor) {
  console.log(`${CINZA}  ${(rotulo + ":").padEnd(22)}${RESET}${AZUL}${valor}${RESET}`);
}
```

## Visualizing a linked list

```js
function visualizar(lista) {
  const partes = [];
  let atual = lista.primeiro;
  while (atual !== null) {
    partes.push(`${BOLD}${atual.valor}${RESET}`);
    atual = atual.proximo;
  }
  const interior = partes.join(`${CINZA} → ${RESET}`);
  return `${CIANO}  [ ${RESET}${interior}${CINZA} → null${RESET}${CIANO} ]${RESET}`;
}
```

## Exception pattern

```js
aviso("Testando índice inválido...");
try {
  lista.inserirNoIndex(99, 999);
  erro("Nenhuma exceção lançada — comportamento inesperado!");
} catch (e) {
  ok(`${e.constructor.name} capturada: "${e.message}"`);
}
```

## Module structure

```js
// ansi constants
// helper functions
// visualize function(s)

function main() {
  cabecalho("Subject");
  // sections...
}

main();
```
