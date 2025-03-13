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

        # Initialize stored args if not present
        if not hasattr(f, "_stored_args"):
            f._stored_args = []
        if not hasattr(f, "_stored_kwargs"):
            f._stored_kwargs = {}

        # Combine stored and new arguments
        all_args = f._stored_args + list(args)
        all_kwargs = {**f._stored_kwargs, **kwargs}

        bind = sig.bind_partial(*all_args, **all_kwargs)
        bind.apply_defaults()

        do_currying = len(bind.arguments) < total_parameters
        if do_currying:
            fn = copy_func(f)
            fn._stored_args = all_args
            fn._stored_kwargs = all_kwargs
            return partial(fn)

        return f(*all_args, **all_kwargs)

    return wrapper