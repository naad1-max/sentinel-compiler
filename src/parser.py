from dataclasses import dataclass
from lexer import Lexer, Token, TokenType


class ParserError(Exception):
    pass


@dataclass(frozen=True)
class NumberExpr:
    value: int | float


@dataclass(frozen=True)
class BinaryExpr:
    left: object
    operator: TokenType
    right: object


@dataclass(frozen=True)
class Program:
    expressions: list


class Parser:
    def __init__(self, source: str):
        self.tokens = Lexer(source).tokenize()
        self.pos = 0

    def current_token(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        token = self.current_token()
        self.pos += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()

        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {token.type.name} "
                f"at position {token.position}"
            )

        return self.advance()

    def parse(self) -> Program:
        expressions = []

        while self.current_token().type != TokenType.EOF:
            expressions.append(self.expression())

        self.expect(TokenType.EOF)
        return Program(expressions)

    def expression(self):
        left = self.number()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            right = self.number()
            left = BinaryExpr(left, operator.type, right)

        return left

    def number(self):
        token = self.current_token()

        if token.type == TokenType.INT:
            self.advance()
            return NumberExpr(token.value)

        if token.type == TokenType.FLOAT:
            self.advance()
            return NumberExpr(token.value)

        raise ParserError(
            f"Expected number, got {token.type.name} at position {token.position}"
        )


if __name__ == "__main__":
    source = "12 + 3.5 - 7"
    parser = Parser(source)
    ast = parser.parse()
    print(ast)
