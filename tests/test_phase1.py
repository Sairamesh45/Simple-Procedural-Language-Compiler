import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import Lexer
from src.tokens import TokenType
from src.errors import LexicalError
from src.symbol_table import SymbolTable


def run_test_t1():
    code = "int count = 25;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected = [
        (TokenType.KEYWORD_INT, "int"),
        (TokenType.IDENTIFIER, "count"),
        (TokenType.ASSIGN, "="),
        (TokenType.INT_LITERAL, "25"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]
    actual = [(t.type, t.lexeme) for t in tokens]
    assert actual == expected, f"T1 Failed: Expected {expected}, got {actual}"
    return "T1 (Normal Declaration) Passed"


def run_test_t2():
    code = "count = count + 5 * 2 <= 100;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    token_types = [t.type for t in tokens]
    assert TokenType.PLUS in token_types, "T2 Failed: PLUS operator missing"
    assert TokenType.STAR in token_types, "T2 Failed: STAR operator missing"
    assert TokenType.LE in token_types, "T2 Failed: LE operator missing"
    return "T2 (Expression with Operators) Passed"


def run_test_t3():
    code = 'string msg = "hello world"; char grade = \'A\';'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    str_tok = next(t for t in tokens if t.type == TokenType.STRING_LITERAL)
    char_tok = next(t for t in tokens if t.type == TokenType.CHAR_LITERAL)

    assert str_tok.value == "hello world"
    assert str_tok.lexeme == '"hello world"'
    assert char_tok.value == "A"
    assert char_tok.lexeme == "'A'"
    return "T3 (String and Character Literals) Passed"


def run_test_t4():
    code = """// Line 1 single-line comment
int x = 10; /* multi-line
comment spanning lines */
int y = 20;"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    tok_y = next(t for t in tokens if t.lexeme == "y")
    assert tok_y.line == 4, f"T4 Failed: Expected y at line 4, got line {tok_y.line}"
    assert all(t.type != TokenType.SLASH for t in tokens)
    return "T4 (Comments and Line Number Tracking) Passed"


def run_test_t5():
    code = "int x = 10 @ 5;"
    lexer = Lexer(code)
    try:
        lexer.tokenize()
        assert False, "T5 Failed: Expected LexicalError for '@'"
    except LexicalError as e:
        assert "@" in e.message or "Invalid symbol" in e.message
        assert e.line == 1
    return "T5 (Invalid Symbol Detection) Passed"


def run_test_t6():
    code = "int x = 25abc;"
    lexer = Lexer(code)
    try:
        lexer.tokenize()
        assert False, "T6 Failed: Expected LexicalError for malformed number '25abc'"
    except LexicalError as e:
        assert "Malformed number" in e.message
    return "T6 (Invalid Number Detection) Passed"


def run_test_t7():
    code = "int integer = 42;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.KEYWORD_INT
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].lexeme == "integer"
    return "T7 (Keyword vs Identifier Disambiguation) Passed"


def run_all_tests():
    print("=" * 65)
    print("  SPL COMPILER - PHASE 1 VERIFICATION TEST MATRIX (T1 - T7)")
    print("=" * 65)
    tests = [
        run_test_t1,
        run_test_t2,
        run_test_t3,
        run_test_t4,
        run_test_t5,
        run_test_t6,
        run_test_t7,
    ]

    all_passed = True
    for test in tests:
        try:
            result = test()
            print(f" [PASS] {result}")
        except Exception as err:
            print(f" [FAIL] {err}")
            all_passed = False

    print("=" * 65)
    if all_passed:
        print(" ALL 7 PHASE 1 TEST MATRIX CASES PASSED SUCCESSFULLY!")
    else:
        print(" SOME TESTS FAILED. PLEASE REVIEW.")
    print("=" * 65)
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
