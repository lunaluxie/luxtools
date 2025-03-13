import functools
import inspect
import types
from functools import wraps


def copy_func(f):
    """Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
    g = types.FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g

def partial(f):
    """A wrapper for a user-defined function that allows for currying.

    Example:

    @partial
    def foo(a,b,c):
      return a+b+c

    > foo(b=1)(1)(1) == 1
    > True

    Notes:
    Heavily uses:
    - [Function signatures](https://peps.python.org/pep-0362/)

    Args:
        f (Callable): function to curry

    Returns:
        Callabe: The function itself with any arguments that were passed in curried.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(f)
        total_parameters = len(sig.parameters)

        if not hasattr(f, "_pargs"):
            f._pargs = {}  # initialize empty if none

        bind = sig.bind_partial(*args, **{**f._pargs, **kwargs})
        bind.apply_defaults()

        applied_arguments = len(bind.arguments)

        do_currying = applied_arguments < total_parameters
        if do_currying:
            fn = copy_func(f)
            fn._pargs = bind.arguments.copy()
            return partial(fn)

        return f(*bind.args, **bind.kwargs)

    return wrapper