import functools
import inspect
import types
from copy import deepcopy
from functools import wraps
from typing import Callable, List


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

    Args:
        f (Callable): function to curry

    Returns:
        Callabe: The function itself with any arguments that were passed in curried.
    """
    # f = copy_func(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        fn = copy_func(f)

        # Create a new function instance with its own state
        required_parameters = len(
            [
                0
                for _, param in fn._pargs.items()
                if param.default == inspect.Parameter.empty
            ]
        )
        given_parameters = len(args) + len(kwargs)

        remaining_params = required_parameters

        # update positional arguments
        for i, arg in enumerate(args):
            try:
                key = next(
                    k
                    for k, v in fn._pargs.items()
                    if v.default == inspect.Parameter.empty
                )
                fn._pargs[key] = inspect.Parameter(
                    key, inspect.Parameter.KEYWORD_ONLY, default=arg
                )
            except StopIteration:
                # handle *args parameter
                if hasattr(fn, "_args"):
                    fn._args.extend(args[i:])
                    break
                else:
                    raise TypeError(
                        f"{fn.__name__}() takes {required_parameters} positional arguments but {given_parameters} were given"
                    )

            remaining_params -= 1

        # update keyword arguments
        for key, value in kwargs.items():
            # handle **kwargs parameter
            if key not in fn._pargs:
                if hasattr(fn, "_kwargs"):
                    fn._kwargs[key] = value
                else:
                    raise TypeError(
                        f"{fn.__name__}() got an unexpected keyword argument '{key}'"
                    )

            if fn._pargs[key].default == inspect.Parameter.empty:
                # only update required args if we are adding new arguments instead of overriding existing ones.
                remaining_params -= 1

            # handle keyword arguments that are already matched
            fn._pargs[key] = inspect.Parameter(
                key, inspect.Parameter.KEYWORD_ONLY, default=value
            )

        # need to check that the given parameters are not keyword parameters that are already matched
        do_currying = remaining_params != 0

        if do_currying:
            # do I even need c here, or can I just return partial(f)?
            c = lambda *args, **kwargs: f(*args, **kwargs)  # noqa: E731
            c._pargs = fn._pargs
            if hasattr(fn, "_args"):
                c._args = fn._args
            if hasattr(f, "_kwargs"):
                c._kwargs = fn._kwargs

            # copy over attributes not handled by wraps
            c.__doc__ = fn.__doc__
            c.__name__ = fn.__name__

            return partial(c)

        if not hasattr(fn, "_args"):
            fn._args = []
        if not hasattr(fn, "_kwargs"):
            fn._kwargs = {}

        return fn(
            **{
                **{key: value.default for key, value in fn._pargs.items()},
                **fn._kwargs,
            }
        )

    # smuggle my monkey patched variables
    if not hasattr(f, "_pargs"):
        sig = inspect.signature(f)
        f._pargs = sig.parameters.copy()

        if f._pargs.get("args"):
            raise ValueError(
                "We currently don't support *args in function as we convert all arguments to keyword only arguments."
            )
            f._pargs.pop("args")
            f._args = []
        if f._pargs.get("kwargs"):
            f._pargs.pop("kwargs")
            f._kwargs = {}

    return copy_func(wrapper)
