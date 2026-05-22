# Java — Terminal Output Style Reference

## ANSI constants (always declare at the top of the class)

```java
static final String RESET    = "\u001B[0m";
static final String BOLD     = "\u001B[1m";
static final String VERDE    = "\u001B[32m";
static final String AMARELO  = "\u001B[33m";
static final String AZUL     = "\u001B[34m";
static final String CIANO    = "\u001B[36m";
static final String VERMELHO = "\u001B[31m";
static final String CINZA    = "\u001B[90m";
```

## Helper methods (copy and adapt as needed)

```java
static void cabecalho(String titulo) {
    int w = 52;
    String linha = "═".repeat(w);
    System.out.println();
    System.out.println(CIANO + BOLD + "╔" + linha + "╗" + RESET);
    int pad = (w - titulo.length()) / 2;
    String p = " ".repeat(Math.max(0, pad));
    System.out.printf(CIANO + BOLD + "║" + RESET + BOLD + "%s%-" + w + "s" + RESET + CIANO + BOLD + "║%n" + RESET, p, titulo);
    System.out.println(CIANO + BOLD + "╚" + linha + "╝" + RESET);
}

static void secao(String nome) {
    System.out.println();
    System.out.println(AZUL + BOLD + "┌─ " + nome + " " + "─".repeat(Math.max(0, 44 - nome.length())) + RESET);
}

static void ok(String msg)              { System.out.println(VERDE   + "  ✔ " + RESET + msg); }
static void aviso(String msg)           { System.out.println(AMARELO + "  ⚠  " + RESET + msg); }
static void erro(String msg)            { System.out.println(VERMELHO+ "  ✖ " + RESET + msg); }
static void separador()                 { System.out.println(CINZA + "  " + "·".repeat(48) + RESET); }

static void info(String rotulo, Object valor) {
    System.out.printf(CINZA + "  %-22s" + RESET + AZUL + "%s" + RESET + "%n", rotulo + ":", valor);
}
```

## Visualizing a linked list

```java
static String visualizar(MinhaLinkedList lista) {
    StringBuilder sb = new StringBuilder();
    sb.append(CIANO).append("  [ ").append(RESET);
    No atual = lista.primeiro;
    while (atual != null) {
        sb.append(BOLD).append(atual.valor).append(RESET);
        if (atual.proximo != null) sb.append(CINZA).append(" → ").append(RESET);
        atual = atual.proximo;
    }
    sb.append(CINZA).append(" → null").append(RESET);
    sb.append(CIANO).append(" ]").append(RESET);
    return sb.toString();
}
```

Adapt the traversal logic for other structures (tree, stack, queue).

## Exception pattern

```java
aviso("Testando índice fora dos limites...");
try {
    lista.inserirNoIndex(99, 999);
    erro("Nenhuma exceção lançada — comportamento inesperado!");
} catch (RuntimeException e) {
    ok("RuntimeException capturada: \"" + e.getMessage() + "\"");
} catch (NullPointerException e) {
    aviso("NullPointerException: " + e.getMessage());
}
```

## Class structure

```java
public class Main {
    // 1. ANSI constants
    // 2. Helper methods (cabecalho, secao, ok, aviso, erro, separador, info, visualizar)
    // 3. public static void main(String[] args) {
    //      cabecalho("Subject");
    //      // sections...
    //    }
}
```

No instance fields needed — keep everything `static`.
