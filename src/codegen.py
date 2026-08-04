from parser import (
    Parser,
    Program,
    NumberExpr,
    StringExpr,
    BinaryExpr,
    PutsStmt,
    ExitStmt,
)
from lexer import TokenType


class CodeGenError(Exception):
    pass


class CCodeGenerator:
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
            raise CodeGenError("String expressions can only be used with puts")

        if isinstance(expr, BinaryExpr):
            return self.binary(expr)

        raise CodeGenError(f"Unknown expression node: {expr!r}")

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
        if isinstance(statement, PutsStmt):
            return self.puts(statement)

        if isinstance(statement, ExitStmt):
            return self.exit(statement)

        expression_code = self.expression(statement)
        return f'    printf("%g\\n", (double)({expression_code}));'

    def puts(self, statement: PutsStmt) -> str:
        if isinstance(statement.value, StringExpr):
            value = self.c_string(statement.value.value)
            return f'    printf("%s\\n", "{value}");'

        expression_code = self.expression(statement.value)
        return f'    printf("%g\\n", (double)({expression_code}));'

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
