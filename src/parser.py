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
class StringExpr:
    value: str


@dataclass(frozen=True)
class PutsStmt:
    value: object


@dataclass(frozen=True)
class Program:
    statements: list[object]


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
        statements = []

        while self.current_token().type != TokenType.EOF:
            statements.append(self.statement())

        self.expect(TokenType.EOF)
        return Program(statements)

    def statement(self):
        if self.current_token().type == TokenType.PUTS:
            return self.puts_statement()

        return self.expression()

    def puts_statement(self):
        self.expect(TokenType.PUTS)

        if self.current_token().type == TokenType.STRING:
            token = self.advance()
            return PutsStmt(StringExpr(token.value))

        return PutsStmt(self.expression())

    def expression(self):
        left = self.term()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            right = self.term()
            self.validate_numeric_binary(left, right, operator)
            left = BinaryExpr(left, operator.type, right)

        return left

    def term(self):
        left = self.primary()

        while self.current_token().type in (
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.MOD,
        ):
            operator = self.advance()
            right = self.primary()

            if operator.type == TokenType.MOD:
                self.validate_modulus(left, right, operator)

            left = BinaryExpr(left, operator.type, right)

        return left

    def validate_numeric_binary(self, left, right, operator: Token):
        if isinstance(left, StringExpr) or isinstance(right, StringExpr):
            raise ParserError(
                f"Operator {operator.value!r} requires numeric operands "
                f"at position {operator.position}"
            )

    def primary(self):
        token = self.current_token()

        if token.type == TokenType.INT:
            self.advance()
            return NumberExpr(token.value)

        if token.type == TokenType.FLOAT:
            self.advance()
            return NumberExpr(token.value)

        if token.type == TokenType.STRING:
            self.advance()
            return StringExpr(token.value)

        raise ParserError(
            f"Expected expression, got {token.type.name} at position {token.position}"
        )

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

    def validate_modulus(self, left, right, operator: Token):
        if not self.is_integer_expr(left) or not self.is_integer_expr(right):
            raise ParserError(
                f"Modulus operator requires integer operands at position "
                f"{operator.position}"
            )

    def is_integer_expr(self, expr) -> bool:
        if isinstance(expr, NumberExpr):
            return isinstance(expr.value, int)

        if isinstance(expr, BinaryExpr):
            return (
                expr.operator == TokenType.MOD
                and self.is_integer_expr(expr.left)
                and self.is_integer_expr(expr.right)
            )

        return False


if __name__ == "__main__":
    source = """12 + 3 % 2 - 5
13 + 4 % 3 - 6
"""

    parser = Parser(source)
    ast = parser.parse()
    print(ast)
