# Python — Terminal Output Style Reference

## ANSI constants

```python
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERDE    = "\033[32m"
AMARELO  = "\033[33m"
AZUL     = "\033[34m"
CIANO    = "\033[36m"
VERMELHO = "\033[31m"
CINZA    = "\033[90m"
```

## Helper functions

```python
def cabecalho(titulo: str) -> None:
    w = 52
    linha = "═" * w
    print()
    print(f"{CIANO}{BOLD}╔{linha}╗{RESET}")
    pad = " " * max(0, (w - len(titulo)) // 2)
    print(f"{CIANO}{BOLD}║{RESET}{BOLD}{pad}{titulo:<{w}}{RESET}{CIANO}{BOLD}║{RESET}")
    print(f"{CIANO}{BOLD}╚{linha}╝{RESET}")

def secao(nome: str) -> None:
    print()
    tracas = "─" * max(0, 44 - len(nome))
    print(f"{AZUL}{BOLD}┌─ {nome} {tracas}{RESET}")

def ok(msg: str)      -> None: print(f"{VERDE}  ✔ {RESET}{msg}")
def aviso(msg: str)   -> None: print(f"{AMARELO}  ⚠  {RESET}{msg}")
def erro(msg: str)    -> None: print(f"{VERMELHO}  ✖ {RESET}{msg}")
def separador()       -> None: print(f"{CINZA}  {'·' * 48}{RESET}")

def info(rotulo: str, valor) -> None:
    print(f"{CINZA}  {rotulo + ':':<22}{RESET}{AZUL}{valor}{RESET}")
```

## Visualizing a linked list

```python
def visualizar(lista) -> str:
    partes = []
    atual = lista.primeiro
    while atual is not None:
        partes.append(f"{BOLD}{atual.valor}{RESET}")
        atual = atual.proximo
    interior = f"{CINZA} → {RESET}".join(partes)
    return f"{CIANO}  [ {RESET}{interior}{CINZA} → None{RESET}{CIANO} ]{RESET}"
```

## Exception pattern

```python
aviso("Testando índice inválido...")
try:
    lista.inserir_no_index(99, 999)
    erro("Nenhuma exceção lançada — comportamento inesperado!")
except (IndexError, ValueError) as e:
    ok(f"Exceção capturada: \"{e}\"")
except Exception as e:
    aviso(f"{type(e).__name__}: {e}")
```

## Module structure

```python
# ansi constants
# helper functions
# visualize function(s)

def main():
    cabecalho("Subject")
    # sections...

if __name__ == "__main__":
    main()
```
