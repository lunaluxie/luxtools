from functools import reduce
from typing import Any, Callable, List, TypeVar, overload

from .basics import identity

T_in = TypeVar("T_in")
T_out = TypeVar("T_out")


@overload
def chain(functions: List[Callable[[Any], Any]]) -> Callable[[T_in], T_out]: ...


@overload
def chain(functions: List[Callable[[Any], Any]], x: T_in) -> T_out: ...


_SENTINEL = object()


def chain_lazy(functions: List[Callable[[Any], Any]]) -> Callable[[T_in], T_out]:
    return lambda x: reduce(
        lambda f, g: g(f), reversed(functions[:-1] + [functions[-1](x)])
    )


def chain_eager(functions: List[Callable], x: Any) -> Any:
    """Chain multiple functions together, applying them from right to left.

    Example:
        >>> def f(x): return x + 1
        >>> def g(x): return x * 2
        >>> def h(x): return x ** 2
        >>> chain([f, g, h], 2)  # equivalent to f(g(h(2)))
        9

    Arg,s:
        functions (List[Callable]): List of functions to apply in reverse order
        x (Any): The initial input value

    Returns:
        Any: The result after applying all functions in sequence
    """
    result = x
    for f in reversed(functions):
        result = f(result)
    return result


def chain(functions: List[Callable[[Any], Any]], x: Any = _SENTINEL) -> Any:
    """Chain multiple functions together

    The inputs must be compatible such that each successive function accepts
    the output of the previous one.

    Example:
        >>> def f(x): return x + 1
        >>> def g(x): return x * 2
        >>> def h(x): return x ** 2
        >>> chain([f, g, h])(2)  # equivalent to f(g(h(2)))
        9
        >>> chain([f, g, h], 2)  # eager evaluation
        9

    Args:
        functions: List of functions to apply in reverse order (f_n ∘ ... ∘ f_1)
        x: Optional initial input value for eager evaluation

    Returns:
        A function that computes the chained result, or the result if x is provided
    """
    if len(functions) == 0:
        if x is not _SENTINEL:
            return x
        return identity

    if x is not _SENTINEL:
        return chain_eager(functions, x)
    else:
        return lambda val: chain_eager(functions, val)


def chain_safe(functions: List[Callable[[Any], Any]], x: Any = _SENTINEL) -> Any:
    if len(functions) == 0:
        functions = [identity]

    return chain(functions, x)


if __name__ == "__main__":

    def f(x):
        return x + 1

    def g(x):
        return x * 2

    def h(x):
        return x**2

    # iterations = 0
    # def chained_function():

    #     def the_chained_function(x):

    #         def reduce_function(f, g):
    #             global iterations
    #             print(f"step {iterations}:", f, g)
    #             iterations += 1
    #             return g(f)

    #         return reduce(reduce_function, reversed([f, g, h(x)]))

    #     return the_chained_function

    # print(chain2([f, g, h])(3))

    # print(chain2([f, g, h])(2))  # equivalent to f(g(h(2)))