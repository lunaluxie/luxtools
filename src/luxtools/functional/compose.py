from typing import Any, Callable, List


def chain(functions: List[Callable], x: Any) -> Any:
    """Chain multiple functions together, applying them from right to left.

    Example:
        >>> def f(x): return x + 1
        >>> def g(x): return x * 2
        >>> def h(x): return x ** 2
        >>> chain([f, g, h], 2)  # equivalent to f(g(h(2)))
        9

    Args:
        functions (List[Callable]): List of functions to apply in reverse order
        x (Any): The initial input value

    Returns:
        Any: The result after applying all functions in sequence
    """
    result = x
    for f in reversed(functions):
        result = f(result)
    return result
