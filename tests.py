import inspect
from typing import Literal

def func(x: Literal["-h", "-p"]):
    """Add 1 to x."""
    return x

sig = inspect.signature(func)
params = sig.parameters

for name, param in params.items():
    # convert the tuple to a beautiful string
    print(type(param.annotation))
    print(param.annotation.__args__.__str__().replace("(", "").replace(")", "").replace("'", ""))
