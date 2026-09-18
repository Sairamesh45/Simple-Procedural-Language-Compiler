# SPL Compiler (Simple Procedural Language)

**Compiler Design Laboratory Project - Phase 1 (25%-30% Milestone)**  
**Student:** Devaguptapu V S Sai Ramesh (Reg No: 24BKT0117)  
**Supervisor:** Dr. Ranjith Kumar S  

---

## Project Overview
This repository contains the Phase 1 implementation of a compiler for **SPL (Simple Procedural Language)**, a statically-typed procedural language with C-like syntax designed for educational compiler pipelines.

Phase 1 completes the **Language Specification + Lexical Analyzer Prototype + Lexical Diagnostics + Initial Symbol Table Stub**, fulfilling the 25%-30% requirement of the course curriculum.

---

## Quick Start (Demonstration for Faculty)

### 1. Run Official SPL Program (Section 8.4)
```bash
python main.py samples/sample.spl
```
*Outputs source preview, tabular token stream, proposal Section 12.3 token format, initial symbol table stub, and token statistics.*

### 2. Run Prototype Example (Section 12.3)
```bash
python main.py samples/counter.spl
```
*Verifies exact token stream parity against Section 12.3 of the submitted proposal.*

### 3. Demonstrate Lexical Error Handling & Position Pointer (Section 15)
```bash
python main.py samples/error_invalid_char.spl
python main.py samples/error_unterminated_str.spl
python main.py samples/error_malformed_num.spl
```
*Demonstrates visual caret (`^`) pointing to the offending character with exact line and column numbers.*

### 4. Run Automated Test Matrix (Section 12.4, T1 through T7)
```bash
python main.py --test
```
or
```bash
python tests/test_phase1.py
```

---

## Project Architecture

```
d:/Projects/compiler/
|-- src/
|   |-- tokens.py
|   |-- lexer.py
|   |-- errors.py
|   `-- symbol_table.py
|-- samples/
|   |-- sample.spl
|   |-- counter.spl
|   |-- error_invalid_char.spl
|   |-- error_unterminated_str.spl
|   `-- error_malformed_num.spl
|-- tests/
|   `-- test_phase1.py
|-- main.py
`-- README.md
```

---

## Phase 1 Test Matrix Coverage (Section 12.4)

| Test Case | Description | Test Verification | Status |
|---|---|---|---|
| **T1** | Normal declaration | Correct token types for `int count = 25;` | **PASS** |
| **T2** | Expression with operators | Identification of `+`, `*`, `<=`, etc. | **PASS** |
| **T3** | String / Character literal | Preserves quotes and unescaped values | **PASS** |
| **T4** | Comments and whitespace | Comments ignored, line/col tracking preserved | **PASS** |
| **T5** | Invalid symbol | Catches `@`, `$`, etc. with line/col pointer | **PASS** |
| **T6** | Malformed number | Catches invalid digits / trailing letters | **PASS** |
| **T7** | Unrecognized word | Disambiguates keywords vs identifiers | **PASS** |

---

## Viva Q&A Cheat Sheet for Faculty

### Q1: "Did you use regular expressions or a manual scanner?"
> **Answer:** We implemented a **manual character-by-character scanner (deterministic finite state machine)** with `peek()`, `peek_next()`, `advance()`, and `match()` methods in [lexer.py](file:///d:/Projects/compiler/src/lexer.py). This avoids regex backtracking overhead and gives fine-grained control over multi-line comments and exact column counting.

### Q2: "How does the lexer distinguish between `=` and `==`, or `+` and `+=`?"
> **Answer:** Using a 1-character lookahead (`peek()` / `match()`). For example, when encountering `=`, the lexer calls `match('=')`. If the next character is `=`, it consumes it and emits `TokenType.EQ` (`==`); otherwise it emits `TokenType.ASSIGN` (`=`).

### Q3: "How does the lexer handle comments and track line numbers?"
> **Answer:** Single-line comments (`//`) discard characters until a newline `\n` is reached. Multi-line comments (`/* ... */`) discard characters until the closing `*/` delimiter, while actively incrementing line counters on each newline encountered. If EOF is reached before `*/`, a lexical error is raised.

### Q4: "What is the role of the Symbol Table stub in Phase 1?"
> **Answer:** The Symbol Table stub in [symbol_table.py](file:///d:/Projects/compiler/src/symbol_table.py) scans the token stream to catalog all unique identifiers, their initial scope (`global`), declaration line, and role (`variable` vs `function`), laying the groundwork for Phase 2/3 semantic and type-checking passes.
