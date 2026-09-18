# SPL Compiler (Simple Procedural Language)

**Compiler Design Laboratory Project — Phase 1 (25%-30% Milestone)**  
**Student:** Devaguptapu V S Sai Ramesh (Reg No: 24BKT0117)  
**Supervisor:** Dr. Ranjith Kumar S  

---

## Project Overview

This repository contains the Phase 1 implementation of a compiler for **SPL (Simple Procedural Language)** — a statically-typed procedural programming language with C-like syntax developed for educational compiler engineering.

Phase 1 establishes the front-end foundation:
- **Language Specification & Lexical Rules** for keywords, identifiers, literals, operators, and delimiters.
- **Deterministic Lexical Analyzer (Scanner)** with single-character lookahead.
- **Lexical Error Diagnostics** featuring exact line/column tracking and visual caret (`^`) indicators.
- **Initial Symbol Table Stub** cataloging user-defined identifiers, scope, declaration line, and inferred types.

---

## Key Implementation Highlights

- **Manual Character Scanner (DFA):** Implemented using pointer progression (`advance()`, `peek()`, `match()`) rather than regular expressions, ensuring deterministic performance and exact column tracking.
- **Lookahead Disambiguation:** Resolves multi-character operators (e.g., `=` vs `==`, `+` vs `+=`, `<` vs `<=`) using 1-character lookahead.
- **Comment Stripping & Line Tracking:** Handles both single-line (`//`) and multi-line (`/* ... */`) comments while accurately tracking line numbers and unterminated comment errors.
- **Detailed Diagnostics:** Reports clear error messages with source line previews and caret pointers for unrecognized characters, unterminated strings, and malformed numbers.
- **Symbol Table Stub:** Parses the token stream to populate identifier names, types, scope (`global`), and roles (`variable` / `function`) for subsequent semantic phases.

---

## Repository Structure

```
compiler/
├── src/
│   ├── tokens.py         # Token definitions, TokenType enum, keywords
│   ├── lexer.py          # Character-by-character scanner and tokenizer
│   ├── errors.py         # LexicalError class with visual caret formatting
│   └── symbol_table.py   # Symbol table stub and SymbolEntry model
├── samples/
│   ├── sample.spl              # Standard SPL sample program
│   ├── counter.spl             # Loop and arithmetic prototype sample
│   ├── error_invalid_char.spl  # Lexical error: invalid character (@)
│   ├── error_unterminated_str.spl # Lexical error: unclosed string
│   └── error_malformed_num.spl # Lexical error: malformed number (25abc)
├── tests/
│   └── test_phase1.py    # Automated test suite (T1 - T7)
├── main.py               # CLI entry point and pipeline runner
└── README.md             # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.8 or higher (no external third-party libraries required)

### Running the Compiler on a Sample Program
```bash
python main.py samples/sample.spl
```
This runs lexical analysis on the input file and displays:
1. Source code preview with line numbers
2. Structured token stream table (Type, Lexeme, Value, Location)
3. Proposal token stream representation
4. Populated Phase 1 Symbol Table
5. Token distribution metrics

### Demonstrating Lexical Error Handling
```bash
python main.py samples/error_invalid_char.spl
python main.py samples/error_unterminated_str.spl
python main.py samples/error_malformed_num.spl
```
Each demonstrates visual error pinpointing with exact line and column numbers.

### Running Automated Test Suite
To verify the complete Phase 1 test matrix (T1 to T7):
```bash
python main.py --test
```
*(or run `python tests/test_phase1.py`)*

---

## Phase 1 Test Matrix Coverage

| Test Case | Description | Verification Target | Status |
|---|---|---|---|
| **T1** | Normal Declaration | Correct tokenization of type, identifier, assignment, literal, delimiter | **PASS** |
| **T2** | Expressions & Operators | Disambiguation of arithmetic, relational, and assignment operators | **PASS** |
| **T3** | String & Character Literals | Escape preservation and string/char token value extraction | **PASS** |
| **T4** | Comments & Newlines | Single-line and multi-line comments ignored; line counters preserved | **PASS** |
| **T5** | Invalid Symbol Detection | Rejection of unauthorized characters (`@`, `$`) with caret pointer | **PASS** |
| **T6** | Malformed Numbers | Rejection of invalid numeric formats (e.g., `25abc`) | **PASS** |
| **T7** | Keyword vs Identifier | Accurate distinction between language keywords and user identifiers | **PASS** |
