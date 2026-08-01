from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

@dataclass(frozen=True)
class Span:
    start: int
    end: int
    line: int
    column: int

class BinaryOp(str, Enum):
    ADD = "+"
    SUB = "-"

@dataclass(frozen=True)
class NumberLiteral:
    value: float
    raw: Optional[str] = None
    span: Optional[Span] = None

@dataclass(frozen=True)
class BinaryExpr:
    op: BinaryOp
    left: "Expr"
    right: "Expr"
    span: Optional[Span] = None

Expr = Union[NumberLiteral, BinaryExpr]

@dataclass(frozen=True)
class Program:
    expr: Expr
    span: Optional[Span] = None
