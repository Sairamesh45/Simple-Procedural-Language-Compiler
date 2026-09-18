import sys
import os
import argparse
from typing import List

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.lexer import Lexer
from src.tokens import Token, TokenType
from src.errors import LexicalError
from src.symbol_table import SymbolTable


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"


def print_banner():
    banner = f"""{Color.CYAN}{Color.BOLD}
========================================================================
       SPL COMPILER - SIMPLE PROCEDURAL LANGUAGE (PHASE 1)
   Lexical Analyzer, Token Classification & Symbol Table Stub
========================================================================{Color.RESET}"""
    print(banner)


def print_source(source_text: str):
    print(f"\n{Color.BOLD}{Color.YELLOW}[1] SOURCE CODE INPUT:{Color.RESET}")
    print(f"{Color.DIM}------------------------------------------------------------------------{Color.RESET}")
    lines = source_text.splitlines()
    for idx, line in enumerate(lines, start=1):
        print(f" {Color.CYAN}{idx:3d} |{Color.RESET} {line}")
    print(f"{Color.DIM}------------------------------------------------------------------------{Color.RESET}")


def print_token_table(tokens: List[Token]):
    print(f"\n{Color.BOLD}{Color.GREEN}[2] TOKEN STREAM TABLE:{Color.RESET}")
    header = f" {'LOC':^9} | {'TOKEN TYPE':^20} | {'LEXEME':^18} | {'VALUE':^14}"
    divider = f" {'-'*9}-+-{'-'*20}-+-{'-'*18}-+-{'-'*14}"
    print(Color.BOLD + header + Color.RESET)
    print(divider)

    for tok in tokens:
        loc = f"L{tok.line}:C{tok.column}"
        ttype = tok.type.name
        val_str = str(tok.value) if tok.value is not None else "-"
        lex_disp = tok.lexeme.replace("\n", "\\n")
        if len(lex_disp) > 16:
            lex_disp = lex_disp[:13] + "..."
        if len(val_str) > 12:
            val_str = val_str[:9] + "..."

        color = Color.WHITE
        if "KEYWORD" in ttype:
            color = Color.MAGENTA
        elif "LITERAL" in ttype:
            color = Color.YELLOW
        elif ttype == "IDENTIFIER":
            color = Color.CYAN
        elif "OP" in ttype or ttype in ("PLUS", "MINUS", "STAR", "SLASH", "PERCENT", "ASSIGN"):
            color = Color.GREEN
        elif ttype == "EOF":
            color = Color.DIM

        print(f" {loc:<9} | {color}{ttype:<20}{Color.RESET} | {lex_disp:<18} | {val_str:<14}")
    print(divider)


def print_proposal_stream(tokens: List[Token]):
    print(f"\n{Color.BOLD}{Color.MAGENTA}[3] TOKEN STREAM (Proposal Section 12.3 Format):{Color.RESET}")
    print(f"{Color.DIM}------------------------------------------------------------------------{Color.RESET}")
    filtered = [t for t in tokens if t.type != TokenType.EOF]
    for tok in filtered:
        print(f"  {Color.CYAN}{tok.to_proposal_repr()}{Color.RESET}")
    print(f"{Color.DIM}------------------------------------------------------------------------{Color.RESET}")


def print_symbol_table(symbol_table: SymbolTable):
    print(f"\n{Color.BOLD}{Color.BLUE}[4] INITIAL SYMBOL TABLE STUB (Phase 1):{Color.RESET}")
    header = f" {'IDENTIFIER':^18} | {'INFERRED TYPE':^15} | {'SCOPE':^10} | {'LINE':^6} | {'ROLE':^12}"
    divider = f" {'-'*18}-+-{'-'*15}-+-{'-'*10}-+-{'-'*6}-+-{'-'*12}"
    print(Color.BOLD + header + Color.RESET)
    print(divider)

    entries = symbol_table.all_entries()
    if not entries:
        print("  (No user-defined identifiers discovered)")
    else:
        for sym in entries:
            print(f" {sym.name:<18} | {sym.symbol_type:<15} | {sym.scope:<10} | {sym.line:^6} | {sym.role:<12}")
    print(divider)


def print_statistics(tokens: List[Token]):
    keywords = sum(1 for t in tokens if "KEYWORD" in t.type.name)
    identifiers = sum(1 for t in tokens if t.type == TokenType.IDENTIFIER)
    literals = sum(1 for t in tokens if "LITERAL" in t.type.name or t.type in (TokenType.BOOL_TRUE, TokenType.BOOL_FALSE))
    operators = sum(1 for t in tokens if t.type in (
        TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
        TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE, TokenType.EQ, TokenType.NE,
        TokenType.AND, TokenType.OR, TokenType.NOT, TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
        TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN
    ))
    delimiters = sum(1 for t in tokens if t.type in (
        TokenType.SEMICOLON, TokenType.COMMA, TokenType.LPAREN, TokenType.RPAREN,
        TokenType.LBRACE, TokenType.RBRACE
    ))

    print(f"\n{Color.BOLD}[5] LEXICAL METRICS:{Color.RESET}")
    print(f"  Total Tokens: {Color.BOLD}{len(tokens)-1}{Color.RESET} (excl. EOF)")
    print(f"  - Keywords:    {Color.MAGENTA}{keywords}{Color.RESET}")
    print(f"  - Identifiers: {Color.CYAN}{identifiers}{Color.RESET}")
    print(f"  - Literals:    {Color.YELLOW}{literals}{Color.RESET}")
    print(f"  - Operators:   {Color.GREEN}{operators}{Color.RESET}")
    print(f"  - Delimiters:  {delimiters}")
    print(f"{Color.CYAN}========================================================================{Color.RESET}\n")


def process_source(source_text: str, filename: str = "<stdin>") -> bool:
    print_source(source_text)
    lexer = Lexer(source_text)

    try:
        tokens = lexer.tokenize()
    except LexicalError as err:
        print(f"\n{Color.RED}{Color.BOLD}[!] LEXICAL ANALYSIS FAILED:{Color.RESET}")
        print(f"{Color.RED}{err}{Color.RESET}")
        print(f"{Color.YELLOW}Execution stopped at first invalid character as per Phase 1 error policy.{Color.RESET}\n")
        return False

    print_token_table(tokens)
    print_proposal_stream(tokens)

    sym_table = SymbolTable(scope_name="global")
    sym_table.insert_from_tokens(tokens)
    print_symbol_table(sym_table)

    print_statistics(tokens)
    return True


def main():
    parser = argparse.ArgumentParser(description="SPL Compiler - Phase 1 Lexical Analyzer")
    parser.add_argument("filename", nargs="?", help="Path to .spl source file to compile")
    parser.add_argument("--test", action="store_true", help="Run automated Phase 1 test suite (T1-T7)")
    args = parser.parse_args()

    print_banner()

    if args.test:
        from tests.test_phase1 import run_all_tests
        run_all_tests()
        return

    file_path = args.filename
    if not file_path:
        default_file = os.path.join(os.path.dirname(__file__), "samples", "sample.spl")
        if os.path.exists(default_file):
            print(f"{Color.YELLOW}No input file specified. Running demonstration with default: samples/sample.spl{Color.RESET}")
            file_path = default_file
        else:
            print(f"{Color.RED}Error: No input file provided. Usage: python main.py <file.spl>{Color.RESET}")
            sys.exit(1)

    if not os.path.exists(file_path):
        print(f"{Color.RED}Error: File not found '{file_path}'{Color.RESET}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    success = process_source(source, file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
