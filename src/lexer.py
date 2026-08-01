from dataclasses import dataclass
from typing import Any


@dataclass
class Token:
    type_: str
    line: int
    col: int
    idx: int
    value: Any = None

    def __repr__(self):
        if self.value is None:
            return f"'{self.type_}'Line {self.line}, col {self.col}, at idx {self.idx}"
        return f"'{self.type_}:{self.value}' Line {self.line}, col {self.col}, at idx {self.idx}"


@dataclass
class Position:
    line: int = 1
    col: int = 0
    idx: int = -1

    def advance(self, char):
        self.idx += 1
        self.col += 1

        if char == "\n":
            self.line += 1
            self.col = 1


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = Position()
        self.char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.char)

        if self.pos.idx < len(self.source):
            self.char = self.source[self.pos.idx]
        else:
            self.char = None

    def error(self, message):
        raise LexerError(
            f"{message}\nLine {self.pos.line}, col {self.pos.col}, at idx {self.pos.idx}"
        )

    def tokenize_number(self):
        start_line = self.pos.line
        start_col = self.pos.col
        start_idx = self.pos.idx

        num = []
        dots = 0

        while self.char is not None and (self.char.isdigit() or self.char == "."):
            if self.char == ".":
                dots += 1
                if dots > 1:
                    self.error("You cannot have more than one dot in a number")

            num.append(self.char)
            self.advance()

        text = "".join(num)

        if dots == 0:
            return Token("INT", start_line, start_col, start_idx, int(text))
        return Token("FLOAT", start_line, start_col, start_idx, float(text))

    def tokenize(self):
        tokens = []

        try:
            while self.char is not None:
                if self.char.isspace():
                    self.advance()
                elif self.char.isdigit():
                    tokens.append(self.tokenize_number())
                elif self.char == "+":
                    tokens.append(Token("PLUS", self.pos.line, self.pos.col, self.pos.idx))
                    self.advance()
                elif self.char == "-":
                    tokens.append(Token("MINUS", self.pos.line, self.pos.col, self.pos.idx))
                    self.advance()
                else:
                    self.error(f"Unexpected character {self.char!r}")

            tokens.append(Token("EOF", self.pos.line, self.pos.col, self.pos.idx))
            return tokens, 0

        except LexerError as err:
            print(f"ERROR: {err}")
            return [], 1


def lexer_main(source):
    lexer = Lexer(source)
    tokens, exit_code = lexer.tokenize()
    if exit_code:
        exit(exit_code)
    return tokens
