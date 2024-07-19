from functools import wraps
import inspect
from typing import List, Callable
from typeguard import check_type

def overload(fs:List[Callable], verbose=False) -> Callable:
  """Idea: combine multiple functions with different signatures
  into a single function that dispatches to the correct function
  based on the arguments.

  Args:
      fs (List[Callable]): list of functions to be overloaded
      verbose (bool, optional): Whether to print debug information. Defaults to False.

  Raises:
      TypeError: If none of the overloads matched the given arguments when calling the function

  Returns:
      Callable: The overloaded function
  """
  params = [inspect.signature(f).parameters.copy() for f in fs]

  # matching:
  # step 1 - check if the number of arguments match
  # step 2 - match the given parameters to the function parameters
  # step 3 - check type of each match.

  def match(params, args, kwargs, verbose):
    if len(params) != len(args) + len(kwargs):
        if verbose: print(f"Expected {len(params)} arguments but got {len(args) + len(kwargs)}")
        return False

    # gradually remove parameters that have been matched
    checkable_params = params.copy()

    for i, (k, v) in enumerate(params.items()):
        if i < len(args):
            # match positional arguments to the first params
            if v.annotation == inspect.Parameter.empty:
                # if the parameter has no annotation, we can't check the type
                checkable_params.pop(k)
                continue
            elif not check_type(args[i], v.annotation):
                if verbose: print(f"Expected {v.annotation} but got {type(args[i])}")
                return False

            checkable_params.pop(k)
            continue
        break

    for k, v in kwargs.items():
        matched_param = checkable_params.get(k)
        if matched_param:
            # match keyword arguments to the remaining params
            if matched_param.annotation == inspect.Parameter.empty:
                checkable_params.pop(k)
                continue
            elif not check_type(k, matched_param.annotation):
                if verbose: print(f"Expected {matched_param.annotation} but got {type(k)}")
                return False

            checkable_params.pop(k)
            continue

        else:
            if verbose: print(f"Unexpected keyword argument {k}")
            return False

    if len(checkable_params):
        if verbose: print('Still remaining params, ', checkable_params)
        return False
    else:
        return True

  def wrapper(*args, **kwargs):
    for i, (f, p) in enumerate(zip(fs, params)):
        if verbose:
            print(f"Trying overload ({i}) {f} with params {p}")

        if match(params[i], args, kwargs, verbose=verbose):
            return f(*args, **kwargs)

    raise TypeError(f"None of the overloads matched the given arguments")

  return wrapper


if __name__=="__main__":

  def a(x, y:int):
    return x

  def b(x:List[str], y:int, z, a, b):
    return x

  add = overload([
    a,
    b
  ])

  print(add(["1"], 2))