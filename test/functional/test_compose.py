from luxtools.functional import chain, chain_eager
from luxtools.functional.compose import chain_safe

"""
Chain
"""


def test_basic_chain():
    def f(x: int) -> int:
        return x + 1

    def g(x: int) -> int:
        return x * 2

    def h(x: int) -> int:
        return x**2

    # Lazy
    c = chain([f, g, h])
    assert c(2) == 9, f"Expected 9, got {c(2)}"

    # Eager
    assert chain([f, g, h], 2) == 9


def test_type_conversion():
    def to_str(x: int) -> str:
        return str(x)

    def add_prefix(x: str) -> str:
        return "num_" + x

    def to_upper(x: str) -> str:
        return x.upper()

    # This is what the user wanted: int -> str -> str -> str
    c = chain([to_upper, add_prefix, to_str])
    result = c(42)
    assert result == "NUM_42", f"Expected NUM_42, got {result}"

    # Eager
    assert chain([to_upper, add_prefix, to_str], 42) == "NUM_42"


def test_empty_eager():
    expect = 5
    assert chain_safe([], expect) == expect


def test_empty_lazy():
    expect = 5
    assert chain_safe([])(expect) == expect


"""
Chain Eager
"""


def test_basic_chain_eager():
    def f(x):
        return x + 1

    def g(x):
        return x * 2

    def h(x):
        return x**2

    assert chain_eager([f, g, h], 2) == 9, "Should be 9"


def test_empty_function_list_eager():
    assert chain_eager([], 5) == 5, "Should return input value unchanged"


def test_single_function_eager():
    def double(x):
        return x * 2

    assert chain_eager([double], 3) == 6, "Should be 6"


def test_string_operations_egaer():
    def add_hello(x):
        return "Hello " + x

    def add_exclamation(x):
        return x + "!"

    def to_upper(x):
        return x.upper()

    assert chain([to_upper, add_hello, add_exclamation], "world") == "HELLO WORLD!", (
        "Should transform string correctly"
    )


def test_list_operations_eager():
    def add_one(x):
        return [i + 1 for i in x]

    def multiply_two(x):
        return [i * 2 for i in x]

    def square(x):
        return [i**2 for i in x]

    assert chain([add_one, multiply_two, square], [1, 2, 3]) == [3, 9, 19], (
        "Should transform list correctly"
    )


def test_lambda_functions_eager():
    functions = [lambda x: x + 1, lambda x: x * 2, lambda x: x**2]
    assert chain_eager(functions, 2) == 9, "Should work with lambda functions"


def test_error_handling_eager():
    def bad_function(x):
        raise ValueError("Test error")

    try:
        chain_eager([bad_function], 1)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert str(e) == "Test error", "Should propagate original error"


def test_type_conversion_eager():
    def to_str(x):
        return str(x)

    def add_prefix(x):
        return "num_" + x

    def to_upper(x):
        return x.upper()

    assert chain_eager([to_upper, add_prefix, to_str], 42) == "NUM_42", (
        "Should handle type conversions"
    )