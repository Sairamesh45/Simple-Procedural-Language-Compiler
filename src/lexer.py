from typing import List, Optional
from src.tokens import Token, TokenType, KEYWORDS
from src.errors import LexicalError


class Lexer:
    def __init__(self, source: str):
        self.source: str = source
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1
        self.tokens: List[Token] = []
        self._source_lines = source.splitlines(keepends=True)

    def _get_source_line(self, line_number: int) -> str:
        if 1 <= line_number <= len(self._source_lines):
            return self._source_lines[line_number - 1]
        return ""

    def is_at_end(self) -> bool:
        return self.pos >= len(self.source)

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.pos]

    def peek_next(self) -> str:
        if self.pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.pos + 1]

    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.pos] != expected:
            return False
        self.advance()
        return True

    def tokenize(self) -> List[Token]:
        self.tokens = []
        while not self.is_at_end():
            self._scan_token()

        self.tokens.append(
            Token(
                type=TokenType.EOF,
                lexeme="",
                value=None,
                line=self.line,
                column=self.col,
            )
        )
        return self.tokens

    def _scan_token(self) -> None:
        ch = self.peek()

        if ch in (" ", "\t", "\r"):
            self.advance()
            return
        if ch == "\n":
            self.advance()
            return

        token_line = self.line
        token_col = self.col

        if ch == "/":
            if self.peek_next() == "/":
                self.advance()
                self.advance()
                while not self.is_at_end() and self.peek() != "\n":
                    self.advance()
                return
            elif self.peek_next() == "*":
                start_line = self.line
                start_col = self.col
                self.advance()
                self.advance()
                closed = False
                while not self.is_at_end():
                    if self.peek() == "*" and self.peek_next() == "/":
                        self.advance()
                        self.advance()
                        closed = True
                        break
                    self.advance()
                if not closed:
                    raise LexicalError(
                        "Unterminated multi-line comment",
                        start_line,
                        start_col,
                        self._get_source_line(start_line),
                    )
                return
            else:
                self.advance()
                self.tokens.append(
                    Token(TokenType.SLASH, "/", "/", token_line, token_col)
                )
                return

        if ch == '"':
            self._scan_string(token_line, token_col)
            return

        if ch == "'":
            self._scan_char(token_line, token_col)
            return

        if ch.isdigit():
            self._scan_number(token_line, token_col)
            return

        if ch.isalpha() or ch == "_":
            self._scan_identifier(token_line, token_col)
            return

        self.advance()

        if ch == "+":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.PLUS_ASSIGN, "+=", "+=", token_line, token_col)
                )
            else:
                self.tokens.append(
                    Token(TokenType.PLUS, "+", "+", token_line, token_col)
                )
        elif ch == "-":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.MINUS_ASSIGN, "-=", "-=", token_line, token_col)
                )
            else:
                self.tokens.append(
                    Token(TokenType.MINUS, "-", "-", token_line, token_col)
                )
        elif ch == "*":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.STAR_ASSIGN, "*=", "*=", token_line, token_col)
                )
            else:
                self.tokens.append(
                    Token(TokenType.STAR, "*", "*", token_line, token_col)
                )
        elif ch == "%":
            self.tokens.append(
                Token(TokenType.PERCENT, "%", "%", token_line, token_col)
            )
        elif ch == "=":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.EQ, "==", "==", token_line, token_col)
                )
            else:
                self.tokens.append(
                    Token(TokenType.ASSIGN, "=", "=", token_line, token_col)
                )
        elif ch == "!":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.NE, "!=", "!=", token_line, token_col)
                )
            else:
                self.tokens.append(
                    Token(TokenType.NOT, "!", "!", token_line, token_col)
                )
        elif ch == "<":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.LE, "<=", "<=", token_line, token_col)
                )
            else:
                self.tokens.append(Token(TokenType.LT, "<", "<", token_line, token_col))
        elif ch == ">":
            if self.match("="):
                self.tokens.append(
                    Token(TokenType.GE, ">=", ">=", token_line, token_col)
                )
            else:
                self.tokens.append(Token(TokenType.GT, ">", ">", token_line, token_col))
        elif ch == "&":
            if self.match("&"):
                self.tokens.append(
                    Token(TokenType.AND, "&&", "&&", token_line, token_col)
                )
            else:
                raise LexicalError(
                    "Unexpected '&'. Expected logical AND '&&'",
                    token_line,
                    token_col,
                    self._get_source_line(token_line),
                )
        elif ch == "|":
            if self.match("|"):
                self.tokens.append(
                    Token(TokenType.OR, "||", "||", token_line, token_col)
                )
            else:
                raise LexicalError(
                    "Unexpected '|'. Expected logical OR '||'",
                    token_line,
                    token_col,
                    self._get_source_line(token_line),
                )
        elif ch == ";":
            self.tokens.append(
                Token(TokenType.SEMICOLON, ";", ";", token_line, token_col)
            )
        elif ch == ",":
            self.tokens.append(Token(TokenType.COMMA, ",", ",", token_line, token_col))
        elif ch == "(":
            self.tokens.append(
                Token(TokenType.LPAREN, "(", "(", token_line, token_col)
            )
        elif ch == ")":
            self.tokens.append(
                Token(TokenType.RPAREN, ")", ")", token_line, token_col)
            )
        elif ch == "{":
            self.tokens.append(
                Token(TokenType.LBRACE, "{", "{", token_line, token_col)
            )
        elif ch == "}":
            self.tokens.append(
                Token(TokenType.RBRACE, "}", "}", token_line, token_col)
            )
        else:
            raise LexicalError(
                f"Invalid symbol '{ch}'",
                token_line,
                token_col,
                self._get_source_line(token_line),
            )

    def _scan_string(self, start_line: int, start_col: int) -> None:
        start_pos = self.pos
        self.advance()
        chars: List[str] = []

        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == "\n":
                raise LexicalError(
                    "Unterminated string literal (newline before closing quote)",
                    start_line,
                    start_col,
                    self._get_source_line(start_line),
                )
            ch = self.advance()
            if ch == "\\":
                if self.is_at_end():
                    raise LexicalError(
                        "Unterminated escape sequence in string",
                        start_line,
                        start_col,
                        self._get_source_line(start_line),
                    )
                esc = self.advance()
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == "r":
                    chars.append("\r")
                elif esc == "\\":
                    chars.append("\\")
                elif esc == '"':
                    chars.append('"')
                else:
                    chars.append(esc)
            else:
                chars.append(ch)

        if self.is_at_end():
            raise LexicalError(
                "Unterminated string literal (reached end of file)",
                start_line,
                start_col,
                self._get_source_line(start_line),
            )

        self.advance()
        val = "".join(chars)
        raw_lexeme = self.source[start_pos : self.pos]
        self.tokens.append(
            Token(
                type=TokenType.STRING_LITERAL,
                lexeme=raw_lexeme,
                value=val,
                line=start_line,
                column=start_col,
            )
        )

    def _scan_char(self, start_line: int, start_col: int) -> None:
        start_pos = self.pos
        self.advance()
        if self.is_at_end() or self.peek() == "'":
            raise LexicalError(
                "Empty or malformed character literal",
                start_line,
                start_col,
                self._get_source_line(start_line),
            )

        ch = self.advance()
        val = ch
        if ch == "\\":
            if self.is_at_end():
                raise LexicalError(
                    "Unterminated character escape sequence",
                    start_line,
                    start_col,
                    self._get_source_line(start_line),
                )
            esc = self.advance()
            if esc == "n":
                val = "\n"
            elif esc == "t":
                val = "\t"
            elif esc == "r":
                val = "\r"
            elif esc == "\\":
                val = "\\"
            elif esc == "'":
                val = "'"
            else:
                val = esc

        if self.is_at_end() or self.peek() != "'":
            raise LexicalError(
                "Unterminated character literal",
                start_line,
                start_col,
                self._get_source_line(start_line),
            )

        self.advance()
        raw_lexeme = self.source[start_pos : self.pos]
        self.tokens.append(
            Token(
                type=TokenType.CHAR_LITERAL,
                lexeme=raw_lexeme,
                value=val,
                line=start_line,
                column=start_col,
            )
        )

    def _scan_number(self, start_line: int, start_col: int) -> None:
        start_pos = self.pos
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

            if self.peek() == ".":
                raise LexicalError(
                    "Malformed floating-point number: multiple decimal points",
                    self.line,
                    self.col,
                    self._get_source_line(self.line),
                )

            if self.peek().isalpha() or self.peek() == "_":
                bad_char = self.peek()
                raise LexicalError(
                    f"Malformed number: unexpected character '{bad_char}' after number",
                    self.line,
                    self.col,
                    self._get_source_line(self.line),
                )

            lexeme = self.source[start_pos : self.pos]
            self.tokens.append(
                Token(
                    type=TokenType.FLOAT_LITERAL,
                    lexeme=lexeme,
                    value=float(lexeme),
                    line=start_line,
                    column=start_col,
                )
            )
        elif self.peek() == "." and not self.peek_next().isdigit():
            raise LexicalError(
                "Malformed floating-point number: expected digits after decimal point",
                self.line,
                self.col,
                self._get_source_line(self.line),
            )
        else:
            if self.peek().isalpha() or self.peek() == "_":
                bad_char = self.peek()
                raise LexicalError(
                    f"Malformed number: unexpected character '{bad_char}' after number",
                    self.line,
                    self.col,
                    self._get_source_line(self.line),
                )

            lexeme = self.source[start_pos : self.pos]
            self.tokens.append(
                Token(
                    type=TokenType.INT_LITERAL,
                    lexeme=lexeme,
                    value=int(lexeme),
                    line=start_line,
                    column=start_col,
                )
            )

    def _scan_identifier(self, start_line: int, start_col: int) -> None:
        start_pos = self.pos
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        lexeme = self.source[start_pos : self.pos]

        if lexeme in KEYWORDS:
            token_type = KEYWORDS[lexeme]
            if token_type == TokenType.BOOL_TRUE:
                self.tokens.append(
                    Token(
                        type=TokenType.BOOL_TRUE,
                        lexeme=lexeme,
                        value=True,
                        line=start_line,
                        column=start_col,
                    )
                )
            elif token_type == TokenType.BOOL_FALSE:
                self.tokens.append(
                    Token(
                        type=TokenType.BOOL_FALSE,
                        lexeme=lexeme,
                        value=False,
                        line=start_line,
                        column=start_col,
                    )
                )
            else:
                self.tokens.append(
                    Token(
                        type=token_type,
                        lexeme=lexeme,
                        value=lexeme,
                        line=start_line,
                        column=start_col,
                    )
                )
        else:
            self.tokens.append(
                Token(
                    type=TokenType.IDENTIFIER,
                    lexeme=lexeme,
                    value=lexeme,
                    line=start_line,
                    column=start_col,
                )
            )
