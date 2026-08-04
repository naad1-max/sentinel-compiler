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
class ExitStmt:
    code: int


@dataclass(frozen=True)
class Program:
    statements: list[object]


@dataclass(frozen=True)
class VariableExpr:
    name: str


@dataclass(frozen=True)
class LetStmt:
    name: str
    value: object


class Parser:
    def __init__(self, source: str):
        self.tokens = Lexer(source).tokenize()
        self.pos = 0
        self.variables = {}

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
        if self.current_token().type == TokenType.LET:
            return self.let_statement()

        if self.current_token().type == TokenType.PUTS:
            return self.puts_statement()

        if self.current_token().type == TokenType.EXIT:
            return self.exit_statement()

        return self.expression()

    def let_statement(self):
        self.expect(TokenType.LET)

        name_token = self.current_token()

        if name_token.type != TokenType.IDENTIFIER:
            raise ParserError(
                f"Expected variable name after let, got {name_token.type.name} "
                f"at position {name_token.position}"
            )

        name = self.advance().value

        self.expect(TokenType.EQUAL)

        if self.current_token().type in (TokenType.PUTS, TokenType.EXIT, TokenType.LET):
            token = self.current_token()
            raise ParserError(
                f"Expected value after '=', got statement keyword {token.value!r} "
                f"at position {token.position}"
            )

        value = self.expression()
        value_type = self.resolve_type(value)

        self.variables[name] = value_type

        return LetStmt(name, value)

    def exit_statement(self):
        self.expect(TokenType.EXIT)

        token = self.current_token()

        if token.type != TokenType.INT:
            raise ParserError(
                f"Expected integer exit code, got {token.type.name} "
                f"at position {token.position}"
            )

        code = self.advance().value

        if self.current_token().type != TokenType.EOF:
            token = self.current_token()
            raise ParserError(
                f"Unexpected token after exit statement: {token.type.name} "
                f"at position {token.position}"
            )

        return ExitStmt(code)

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

            self.validate_numeric_binary(left, right, operator)

            if operator.type == TokenType.MOD:
                self.validate_modulus(left, right, operator)

            left = BinaryExpr(left, operator.type, right)

        return left

    def validate_numeric_binary(self, left, right, operator: Token):
        left_type = self.resolve_type(left)
        right_type = self.resolve_type(right)

        if left_type == "string" or right_type == "string":
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

        if token.type == TokenType.IDENTIFIER:
            self.advance()

            if token.value not in self.variables:
                raise ParserError(
                    f"Unknown variable {token.value!r} at position {token.position}"
                )

            return VariableExpr(token.value)

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
        if self.resolve_type(left) != "int" or self.resolve_type(right) != "int":
            raise ParserError(
                f"Modulus operator requires integer operands at position "
                f"{operator.position}"
            )

    def resolve_type(self, expr) -> str:
        if isinstance(expr, NumberExpr):
            if isinstance(expr.value, int):
                return "int"
            return "float"

        if isinstance(expr, StringExpr):
            return "string"

        if isinstance(expr, VariableExpr):
            return self.variables[expr.name]

        if isinstance(expr, BinaryExpr):
            left_type = self.resolve_type(expr.left)
            right_type = self.resolve_type(expr.right)

            if expr.operator == TokenType.MOD:
                return "int"

            if expr.operator == TokenType.SLASH:
                return "float"

            if left_type == "float" or right_type == "float":
                return "float"

            return "int"

        raise ParserError(f"Cannot resolve type for expression: {expr!r}")

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
