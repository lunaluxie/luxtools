from functools import wraps
import inspect
from typing import List, Callable

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

  @wraps(f)
  def wrapper(*args,**kwargs):
    required_parameters = len([0 for _, param in f._pargs.items() if param.default == inspect.Parameter.empty])
    given_parameters = len(args) + len(kwargs)

    do_currying = required_parameters > given_parameters

    # update positional arguments
    for i,arg in enumerate(args):
      try:
        key = next(k for k, v in f._pargs.items() if v.default == inspect.Parameter.empty)
        f._pargs[key] = inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default=arg)
      except StopIteration:
        # handle *args parameter
        if hasattr(f,"_args"):
          f._args.extend(args[i:])
          break
        else:
          raise TypeError(f"{f.__name__}() takes {required_parameters} positional arguments but {given_parameters} were given")


    # update keyword arguments
    for key, value in kwargs.items():
      #handle **kwargs parameter
      if key not in f._pargs:
        if hasattr(f,"_kwargs"):
          f._kwargs[key] = value
        else:
          raise TypeError(f"{f.__name__}() got an unexpected keyword argument '{key}'")

      f._pargs[key] = inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default=value)

    if do_currying:
      # do I even need c here, or can I just return partial(f)?
      c = lambda *args, **kwargs: f(*args, **kwargs)
      c._pargs = f._pargs
      if hasattr(f,"_args"): c._args = f._args
      if hasattr(f,"_kwargs"): c._kwargs = f._kwargs

      # copy over attributes not handled by wraps
      c.__doc__ = f.__doc__
      c.__name__ = f.__name__

      return partial(c)

    if not hasattr(f,"_args"): f._args = []
    if not hasattr(f,"_kwargs"): f._kwargs = {}

    # TODO: find a way to apply args to the function.
    return f(**{**{key: value.default for key, value in f._pargs.items()}, **f._kwargs})

  if not hasattr(f,"_pargs"):
    sig = inspect.signature(f)
    f._pargs = sig.parameters.copy()

    if f._pargs.get("args"):
      raise ValueError("We currently don't support *args in function as we convert all arguments to keyword only arguments.")
      f._pargs.pop("args")
      f._args = []
    if f._pargs.get("kwargs"):
      f._pargs.pop("kwargs")
      f._kwargs = {}

  return wrapper
