from .ast import Program, NumberLiteral, BinaryExpr, BinaryOp, Span

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.current = tokens[0]

    def advance(self):
        if self.idx < len(self.tokens) - 1:
            self.idx += 1
            self.current = self.tokens[self.idx]

    def error(self, message):
        t = self.current
        raise ParserError(f"{message}\nLine {t.line}, col {t.col}, at idx {t.idx}")

    def expect(self, type_):
        if self.current.type_ != type_:
            self.error(f"Expected {type_}, got {self.current.type_}")
        tok = self.current
        self.advance()
        return tok

    def make_span(self, start_tok, end_tok):
        return Span(
            start=start_tok.idx,
            end=end_tok.idx,
            line=start_tok.line,
            column=start_tok.col,
        )

    def parse_program(self):
        expr = self.parse_expr()
        eof = self.expect("EOF")
        return Program(expr=expr, span=self.make_span(self.tokens[0], eof))

    def parse_expr(self):
        left = self.parse_atom()
        while self.current.type_ in ("PLUS", "MINUS"):
            op_tok = self.current
            self.advance()
            right = self.parse_atom()

            op = BinaryOp.ADD if op_tok.type_ == "PLUS" else BinaryOp.SUB
            span = self.make_span(left.span_start_token, right=right, span=span)
            left = BinaryExpr(op, left, right, span)
        return left

    def parse_atom(self):
        tok = self.current
        if tok.type_ == "INT" or tok.type_ == "FLOAT":
            self.advance()
            value=float(tok.value)
            return NumberLiteral(
                value=value,
                raw=str(tok.value),
                span=Span(tok.idx, tok.idx, tok.line, tok.col),
            )

        self.error(f"Expected number, got {tok.type_}")
