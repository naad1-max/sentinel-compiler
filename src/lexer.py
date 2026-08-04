from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MOD = auto()
    EQUAL = auto()
    PUTS = auto()
    EXIT = auto()
    LET = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: object
    position: int


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0

    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def number(self):
        start = self.pos
        dots = 0

        while self.current_char() is not None:
            ch = self.current_char()

            if ch.isdigit():
                self.advance()
            elif ch == ".":
                dots += 1
                if dots > 1:
                    raise LexerError(f"Invalid number at position {self.pos}")
                self.advance()
            else:
                break

        text = self.source[start:self.pos]

        if text.endswith("."):
            raise LexerError(f"Invalid float at position {start}")

        if dots == 1:
            return Token(TokenType.FLOAT, float(text), start)

        return Token(TokenType.INT, int(text), start)

    def next_token(self):
        self.skip_whitespace()

        ch = self.current_char()

        if ch is None:
            return Token(TokenType.EOF, None, self.pos)

        if ch.isdigit():
            return self.number()

        if ch == "+":
            token = Token(TokenType.PLUS, ch, self.pos)
            self.advance()
            return token

        if ch == "-":
            token = Token(TokenType.MINUS, ch, self.pos)
            self.advance()
            return token

        if ch == "*":
            token = Token(TokenType.STAR, ch, self.pos)
            self.advance()
            return token

        if ch == "/":
            token = Token(TokenType.SLASH, ch, self.pos)
            self.advance()
            return token

        if ch == "%":
            token = Token(TokenType.MOD, ch, self.pos)
            self.advance()
            return token

        if ch.isalpha() or ch == "_":
            return self.identifier()

        if ch == '"' or ch == "'":
            return self.string()

        if ch == "=":
            token = Token(TokenType.EQUAL, ch, self.pos)
            self.advance()
            return token

        raise LexerError(f"Unexpected character {ch!r} at position {self.pos}")

    def identifier(self):
        start = self.pos

        while self.current_char() is not None and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            self.advance()

        text = self.source[start:self.pos]

        keywords = {
            "puts": TokenType.PUTS,
            "exit": TokenType.EXIT,
            "let": TokenType.LET,
        }

        token_type = keywords.get(text, TokenType.IDENTIFIER)
        return Token(token_type, text, start)

    def string(self):
        quote = self.current_char()
        start = self.pos
        self.advance()

        value = ""

        while self.current_char() is not None and self.current_char() != quote:
            ch = self.current_char()

            if ch == "\\":
                self.advance()
                escaped = self.current_char()

                if escaped is None:
                    raise LexerError(f"Unterminated string at position {start}")

                if escaped == "n":
                    value += "\n"
                elif escaped == "t":
                    value += "\t"
                elif escaped == quote:
                    value += quote
                elif escaped == "\\":
                    value += "\\"
                else:
                    raise LexerError(
                        f"Unknown escape sequence \\{escaped} at position {self.pos}"
                    )

                self.advance()
            else:
                value += ch
                self.advance()

        if self.current_char() != quote:
            raise LexerError(f"Unterminated string at position {start}")

        self.advance()
        return Token(TokenType.STRING, value, start)

    def tokenize(self):
        tokens = []

        while True:
            token = self.next_token()
            tokens.append(token)

            if token.type == TokenType.EOF:
                break

        return tokens


if __name__ == "__main__":
    source = "12 * 3 / 2 % 5"
    lexer = Lexer(source)

    for token in lexer.tokenize():
        print(token)
