import ast
import operator as op
from typing import Union

# Allowed operators
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}
_UNARY_OPS = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}

class CalcError(ValueError):
    """Invalid or unsupported expression."""

def evaluate(expr: str) -> Union[int, float]:
    """
    Safely evaluate a math expression with numbers and + - * / // % ** and parentheses.
    Raises CalcError or ZeroDivisionError on errors.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise CalcError("Empty expression")

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise CalcError("Invalid syntax") from e

    return _eval_node(tree.body)

def _eval_node(node) -> Union[int, float]:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        # Optional safety for very large exponents
        if isinstance(node.op, ast.Pow):
            if abs(right) > 100 or abs(left) > 1e6:
                raise CalcError("Exponent too large")

        return _BIN_OPS[type(node.op)](left, right)

    # Disallow names, calls, attributes, etc.
    raise CalcError("Unsupported expression")
