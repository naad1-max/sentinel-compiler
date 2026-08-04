from parser import (
    Parser,
    Program,
    NumberExpr,
    StringExpr,
    VariableExpr,
    BinaryExpr,
    PutsStmt,
    ExitStmt,
    LetStmt,
)
from lexer import TokenType


class CodeGenError(Exception):
    pass


class CCodeGenerator:
    def __init__(self):
        self.variables = {}

    def generate(self, program: Program) -> str:
        lines = []

        for statement in program.statements:
            lines.append(self.statement(statement))

        if not program.statements or not isinstance(program.statements[-1], ExitStmt):
            lines.append("    return 0;")

        body = "\n".join(lines)

        return f"""#include <stdio.h>

int main(void) {{
{body}
}}
"""

    def expression(self, expr) -> str:
        if isinstance(expr, NumberExpr):
            return self.number(expr)

        if isinstance(expr, StringExpr):
            return f'"{self.c_string(expr.value)}"'

        if isinstance(expr, VariableExpr):
            return self.variable(expr)

        if isinstance(expr, BinaryExpr):
            return self.binary(expr)

        raise CodeGenError(f"Unknown expression node: {expr!r}")

    def variable(self, expr: VariableExpr) -> str:
        if expr.name not in self.variables:
            raise CodeGenError(f"Unknown variable: {expr.name!r}")

        return expr.name

    def number(self, expr: NumberExpr) -> str:
        return repr(expr.value)

    def binary(self, expr: BinaryExpr) -> str:
        left = self.expression(expr.left)
        right = self.expression(expr.right)

        if expr.operator == TokenType.SLASH:
            return f"((double)({left}) / (double)({right}))"

        if expr.operator == TokenType.MOD:
            return f"((int)({left}) % (int)({right}))"

        operator = self.operator(expr.operator)
        return f"({left} {operator} {right})"

    def operator(self, token_type: TokenType) -> str:
        if token_type == TokenType.PLUS:
            return "+"

        if token_type == TokenType.MINUS:
            return "-"

        if token_type == TokenType.STAR:
            return "*"

        raise CodeGenError(f"Unknown binary operator: {token_type}")

    def statement(self, statement) -> str:
        if isinstance(statement, LetStmt):
            return self.let(statement)

        if isinstance(statement, PutsStmt):
            return self.puts(statement)

        if isinstance(statement, ExitStmt):
            return self.exit(statement)

        expression_code = self.expression(statement)
        return f'    printf("%g\\n", (double)({expression_code}));'

    def let(self, statement: LetStmt) -> str:
        value_type = self.resolve_type(statement.value)
        self.variables[statement.name] = value_type

        value_code = self.expression(statement.value)

        if value_type == "string":
            return f'    const char *{statement.name} = {value_code};'

        if value_type == "float":
            return f"    double {statement.name} = {value_code};"

        if value_type == "int":
            return f"    int {statement.name} = {value_code};"

        raise CodeGenError(f"Unknown variable type: {value_type}")

    def puts(self, statement: PutsStmt) -> str:
        value_type = self.resolve_type(statement.value)
        value_code = self.expression(statement.value)

        if value_type == "string":
            return f'    printf("%s\\n", {value_code});'

        return f'    printf("%g\\n", (double)({value_code}));'

    def resolve_type(self, expr) -> str:
        if isinstance(expr, NumberExpr):
            if isinstance(expr.value, int):
                return "int"
            return "float"

        if isinstance(expr, StringExpr):
            return "string"

        if isinstance(expr, VariableExpr):
            if expr.name not in self.variables:
                raise CodeGenError(f"Unknown variable: {expr.name!r}")

            return self.variables[expr.name]

        if isinstance(expr, BinaryExpr):
            left_type = self.resolve_type(expr.left)
            right_type = self.resolve_type(expr.right)

            if left_type == "string" or right_type == "string":
                raise CodeGenError("Cannot generate arithmetic for strings")

            if expr.operator == TokenType.MOD:
                return "int"

            if expr.operator == TokenType.SLASH:
                return "float"

            if left_type == "float" or right_type == "float":
                return "float"

            return "int"

        raise CodeGenError(f"Cannot resolve type for expression: {expr!r}")

    def exit(self, statement: ExitStmt) -> str:
        return f"    return {statement.code};"

    def c_string(self, value: str) -> str:
        return (
            value
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\t", "\\t")
        )


if __name__ == "__main__":
    source = """12 + 3 - 5
13 + 4 - 6
"""

    parser = Parser(source)
    program = parser.parse()

    generator = CCodeGenerator()
    c_code = generator.generate(program)

    print(c_code)
