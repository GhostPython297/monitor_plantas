---
name: terminal-output-style
description: >
  Apply this skill whenever the user asks to create a Main, entry point, test runner,
  or demo script that prints structured output to the terminal — in Java, Python, or
  JavaScript/Node.js. Triggers include: "formatar saída no terminal", "saída bonita no
  terminal", "output formatado", "deixar o terminal com aparência legal", "criar Main
  com testes", "demo com saída colorida", "output estilizado", "terminal output style",
  "pretty print terminal", or any request to produce a runnable script whose purpose is
  to demonstrate, test, or display a data structure / algorithm with readable output.
  Always use this skill when the task involves creating a script that reports results to
  stdout — even if the user doesn't explicitly say "formatted" or "colorido".
---

# Terminal Output Style

Produce a runnable entry-point script (Main, main.py, main.js, etc.) that exercises an
algorithm or data structure and prints results to the terminal with a clear, consistent
visual style — using ANSI escape codes for color and box-drawing characters for structure.

The output must be readable at a glance: section headers, per-operation feedback, visual
list representation, and exception/error handling that surfaces bugs clearly.

---

## Core visual language

Every script you produce follows this hierarchy:

```
╔══════════════════════════════════════╗
║         Big title / subject          ║
╚══════════════════════════════════════╝

┌─ Section name ──────────────────────
  ✔  operation succeeded
  ⚠  warning / edge case note
  ✖  exception or error caught
  label:                value
  [ 10 → 20 → 30 → null ]   ← visual structure
  ··········· separator ···········

  Estado final da estrutura
```

Keep the total line width ≤ 56 characters for the box, and ≤ 54 for content lines so it
renders well in narrow terminals.

---

## What every script must contain

1. **Cabecalho** — a double-line Unicode box with the subject name.
2. **Sections** — one per operation or group of related operations (`inserirNoFinal`,
   `remover`, etc.), opened with `┌─ nome ───`.
3. **Per-operation feedback** — `✔` for success, `⚠` for warnings, `✖` for caught exceptions.
4. **Visual representation** of the data structure after each meaningful mutation (e.g.
   linked list as `[ A → B → C → null ]`, tree as indented lines, stack as `[ top | … ]`).
5. **Size/metadata line** after each visualization (`tamanho = N`, `altura = N`, etc.).
6. **Exception tests** — always test at least one invalid input and one boundary condition;
   catch the exception and print `✖` with the message.
7. **Estado final** section at the end.

---

## Language-specific instructions

Read the reference file for the target language before writing any code:

| Language          | Reference file                          |
|-------------------|-----------------------------------------|
| Java              | `references/java.md`                    |
| Python            | `references/python.md`                  |
| JavaScript / Node | `references/javascript.md`              |

If the user's language is ambiguous, ask before proceeding.

---

## Tone

Write the output as if it were a live test report: terse labels, no full sentences in the
terminal output itself, but enough context that someone reading the raw stdout immediately
understands what passed and what didn't.

Bug notes (like a parameter name mismatch spotted while reading the code) belong in `⚠`
lines inside the relevant section — not in comments buried in the code.
