from enum import Enum
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    KEYWORD_INT = "int"
    KEYWORD_FLOAT = "float"
    KEYWORD_BOOL = "bool"
    KEYWORD_CHAR = "char"
    KEYWORD_STRING = "string"
    KEYWORD_IF = "if"
    KEYWORD_ELSE = "else"
    KEYWORD_WHILE = "while"
    KEYWORD_FOR = "for"
    KEYWORD_RETURN = "return"
    KEYWORD_PRINT = "print"

    BOOL_TRUE = "true"
    BOOL_FALSE = "false"

    INT_LITERAL = "INT_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    BOOL_LITERAL = "BOOL_LITERAL"

    IDENTIFIER = "IDENTIFIER"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"

    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQ = "=="
    NE = "!="

    AND = "&&"
    OR = "||"
    NOT = "!"

    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    STAR_ASSIGN = "*="

    SEMICOLON = ";"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    EOF = "EOF"


KEYWORDS = {
    "int": TokenType.KEYWORD_INT,
    "float": TokenType.KEYWORD_FLOAT,
    "bool": TokenType.KEYWORD_BOOL,
    "char": TokenType.KEYWORD_CHAR,
    "string": TokenType.KEYWORD_STRING,
    "if": TokenType.KEYWORD_IF,
    "else": TokenType.KEYWORD_ELSE,
    "while": TokenType.KEYWORD_WHILE,
    "for": TokenType.KEYWORD_FOR,
    "return": TokenType.KEYWORD_RETURN,
    "print": TokenType.KEYWORD_PRINT,
    "true": TokenType.BOOL_TRUE,
    "false": TokenType.BOOL_FALSE,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    value: Any
    line: int
    column: int

    def to_proposal_repr(self) -> str:
        t = self.type
        if t in (
            TokenType.KEYWORD_INT,
            TokenType.KEYWORD_FLOAT,
            TokenType.KEYWORD_BOOL,
            TokenType.KEYWORD_CHAR,
            TokenType.KEYWORD_STRING,
            TokenType.KEYWORD_IF,
            TokenType.KEYWORD_ELSE,
            TokenType.KEYWORD_WHILE,
            TokenType.KEYWORD_FOR,
            TokenType.KEYWORD_RETURN,
            TokenType.KEYWORD_PRINT,
        ):
            return f"KEYWORD({self.lexeme})"
        elif t == TokenType.IDENTIFIER:
            return f"IDENTIFIER({self.lexeme})"
        elif t == TokenType.INT_LITERAL:
            return f"INT_LITERAL({self.lexeme})"
        elif t == TokenType.FLOAT_LITERAL:
            return f"FLOAT_LITERAL({self.lexeme})"
        elif t == TokenType.STRING_LITERAL:
            return f"STRING_LITERAL({self.lexeme})"
        elif t == TokenType.CHAR_LITERAL:
            return f"CHAR_LITERAL({self.lexeme})"
        elif t in (TokenType.BOOL_TRUE, TokenType.BOOL_FALSE, TokenType.BOOL_LITERAL):
            return f"BOOL_LITERAL({self.lexeme})"
        elif t in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT,
        ):
            return f"ARITH_OP({self.lexeme})"
        elif t in (
            TokenType.LT,
            TokenType.GT,
            TokenType.LE,
            TokenType.GE,
            TokenType.EQ,
            TokenType.NE,
        ):
            return f"REL_OP({self.lexeme})"
        elif t in (TokenType.AND, TokenType.OR, TokenType.NOT):
            return f"LOGIC_OP({self.lexeme})"
        elif t in (
            TokenType.ASSIGN,
            TokenType.PLUS_ASSIGN,
            TokenType.MINUS_ASSIGN,
            TokenType.STAR_ASSIGN,
        ):
            return f"ASSIGN({self.lexeme})"
        elif t in (
            TokenType.SEMICOLON,
            TokenType.COMMA,
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.RBRACE,
        ):
            return f"DELIMITER({self.lexeme})"
        elif t == TokenType.EOF:
            return "EOF"
        return f"{self.type.name}({self.lexeme})"

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.lexeme}', val={self.value}, line={self.line}, col={self.column})"
