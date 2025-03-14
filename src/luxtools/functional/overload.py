import inspect
from functools import wraps
from typing import Callable

from trycast import isassignable


def overload(scope=None) -> Callable:
    def inner_overload(function) -> Callable:
        """Idea: combine multiple functions with different signatures
        into a single function that dispatches to the correct function
        based on the arguments.
        Args:
            function (Callable): the function being decorated
        Raises:
            TypeError: If none of the overloads matched the given arguments when calling the function
        Returns:
            Callable: The overloaded function
        """
        verbose = False  # you can change this for debugging.

        # save the old function to a list, so we can avoid overwriting them
        # and access them later during dispatch.
        function.overloads = [function]
        if scope is None:
            old_function = globals().get(function.__name__)
        else:
            old_function = scope.get(function.__name__)

        # if one is true, both should always be true
        if old_function and hasattr(old_function, "overloads"):
            function.overloads.extend(old_function.overloads)

        # matching:
        # step 1 - check if the number of arguments match
        # step 2 - pair the given parameters to the function parameters
        # step 3 - check type of each pair.
        def match(params, args, kwargs, verbose=False) -> bool:
            if len(params) != len(args) + len(kwargs):
                if verbose:
                    print(
                        f"Expected {len(params)} arguments but got {len(args) + len(kwargs)}"
                    )
                return False

            # gradually remove parameters that have been matched
            checkable_params = params.copy()

            # first match positional arguments
            for i, (k, v) in enumerate(params.items()):
                if i < len(args):
                    # match positional arguments to the first params
                    if v.annotation == inspect.Parameter.empty:
                        # if the parameter has no annotation, we can't check the type
                        # and assume that the type is correct
                        checkable_params.pop(k)
                        continue
                    elif not isassignable(args[i], v.annotation):
                        if verbose:
                            print(f"Expected {v.annotation} but got {type(args[i])}")
                        return False

                    checkable_params.pop(k)
                    continue
                # break when we have matched all positional arguments
                break

            # match keyword arguments to the remaining params
            for k, v in kwargs.items():
                matched_param = checkable_params.get(k)
                if matched_param:
                    # match keyword arguments to the remaining params
                    if matched_param.annotation == inspect.Parameter.empty:
                        checkable_params.pop(k)
                        continue
                    elif not isassignable(v, matched_param.annotation):
                        if verbose:
                            print(
                                f"Expected {matched_param.annotation} but got {type(k)}"
                            )
                        return False

                    checkable_params.pop(k)
                    continue

                else:
                    if verbose:
                        print(f"Unexpected keyword argument {k}")
                    return False

            if len(checkable_params):
                if verbose:
                    print("Still remaining params, ", checkable_params)
                return False
            else:
                # return True only if all parameters have been matched
                return True

        # the wraps decorator copies the name and docstring
        # and other special attributes of the original function
        @wraps(function)
        def wrapper(*args, **kwargs):
            if verbose:
                print("Dispatching to one of ", function.overloads)

            # get the parameters of each overloaded function
            params = [
                inspect.signature(f).parameters.copy() for f in function.overloads
            ]

            # loop through each function candidate and check if it's callable
            # with the given arguments. Eagerly call and return the first callable function.
            for i, (f, p) in enumerate(zip(function.overloads, params)):
                if verbose:
                    print(f"Trying overload ({i}) {f} with params {p}")

                if match(params[i], args, kwargs, verbose=verbose):
                    return f(*args, **kwargs)

            raise TypeError("None of the overloads matched the given arguments")

        # keep the previous functions (overloaded) as we return the wrapper
        # is not updated by wraps.
        wrapper.overloads = function.overloads

        return wrapper

    return inner_overload