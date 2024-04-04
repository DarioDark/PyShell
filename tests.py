from typing import Literal
import inspect

def func(x: Literal["-h", "-v"]):
    """Add 1 to x."""
    return x

sig = inspect.signature(func)
params = sig.parameters

for name, param in params.items():
    try:
        is_literal = param.annotation.__origin__ == Literal
    except AttributeError:
        is_literal = False
    print(f"Is the annotation of parameter '{name}' a Literal? {is_literal}")
