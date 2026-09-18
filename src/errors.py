from typing import Optional


class LexicalError(Exception):
    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        source_line: Optional[str] = None,
    ):
        self.message = message
        self.line = line
        self.column = column
        self.source_line = source_line
        super().__init__(self.format_error())

    def format_error(self) -> str:
        header = f"Lexical Error [Line {self.line}, Col {self.column}]: {self.message}"
        if self.source_line is not None:
            clean_line = self.source_line.rstrip("\r\n").replace("\t", "    ")
            pointer_offset = max(0, self.column - 1)
            pointer = " " * pointer_offset + "^"
            line_num_str = f"{self.line:4d} | "
            spacer = " " * len(line_num_str)
            return f"\n{header}\n{spacer}\n{line_num_str}{clean_line}\n{spacer}{pointer}\n"
        return header
