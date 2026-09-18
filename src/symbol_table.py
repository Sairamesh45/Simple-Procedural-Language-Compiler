from dataclasses import dataclass
from typing import Dict, List, Optional
from src.tokens import Token, TokenType


@dataclass
class SymbolEntry:
    name: str
    symbol_type: str
    scope: str
    line: int
    role: str

    def __repr__(self) -> str:
        return f"SymbolEntry(name='{self.name}', type='{self.symbol_type}', scope='{self.scope}', line={self.line}, role='{self.role}')"


class SymbolTable:
    def __init__(self, scope_name: str = "global"):
        self.scope_name: str = scope_name
        self.symbols: Dict[str, SymbolEntry] = {}

    def insert_from_tokens(self, tokens: List[Token]) -> None:
        for i, token in enumerate(tokens):
            if token.type == TokenType.IDENTIFIER:
                name = token.lexeme
                if name not in self.symbols:
                    inferred_type = "unknown"
                    role = "variable"
                    if i > 0 and tokens[i - 1].type in (
                        TokenType.KEYWORD_INT,
                        TokenType.KEYWORD_FLOAT,
                        TokenType.KEYWORD_BOOL,
                        TokenType.KEYWORD_CHAR,
                        TokenType.KEYWORD_STRING,
                    ):
                        inferred_type = tokens[i - 1].lexeme

                    if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LPAREN:
                        role = "function"

                    self.symbols[name] = SymbolEntry(
                        name=name,
                        symbol_type=inferred_type,
                        scope=self.scope_name,
                        line=token.line,
                        role=role,
                    )

    def get(self, name: str) -> Optional[SymbolEntry]:
        return self.symbols.get(name)

    def all_entries(self) -> List[SymbolEntry]:
        return list(self.symbols.values())
