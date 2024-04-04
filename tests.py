def func(x):
    """Add 1 to x."""
    return x + 1

def func2(x):
    """Add 2 to x."""
    return func.__name__

print(func2(4))