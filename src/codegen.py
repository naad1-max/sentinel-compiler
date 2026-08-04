from parser import Parser, Program, NumberExpr, BinaryExpr
from lexer import TokenType


class CodeGenError(Exception):
    pass


class CCodeGenerator:
    def generate(self, program: Program) -> str:
        lines = []

        for expr in program.expressions:
            expression_code = self.expression(expr)
            lines.append(f'    printf("%g\\n", (double){expression_code});')

        body = "\n".join(lines)

        return f"""#include <stdio.h>

int main(void) {{
{body}
    return 0;
}}
"""

    def expression(self, expr) -> str:
        if isinstance(expr, NumberExpr):
            return self.number(expr)

        if isinstance(expr, BinaryExpr):
            return self.binary(expr)

        raise CodeGenError(f"Unknown expression node: {expr!r}")

    def number(self, expr: NumberExpr) -> str:
        return repr(expr.value)

    def binary(self, expr: BinaryExpr) -> str:
        left = self.expression(expr.left)
        right = self.expression(expr.right)
        operator = self.operator(expr.operator)

        return f"({left} {operator} {right})"

    def operator(self, token_type: TokenType) -> str:
        if token_type == TokenType.PLUS:
            return "+"

        if token_type == TokenType.MINUS:
            return "-"

        raise CodeGenError(f"Unknown binary operator: {token_type}")


if __name__ == "__main__":
    source = """12 + 3 - 5
13 + 4 - 6
"""

    parser = Parser(source)
    program = parser.parse()

    generator = CCodeGenerator()
    c_code = generator.generate(program)

    print(c_code)
