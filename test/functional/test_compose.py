from luxtools.functional import chain


def test_basic_chain():
    def f(x):
        return x + 1

    def g(x):
        return x * 2

    def h(x):
        return x**2

    assert chain([f, g, h], 2) == 9, "Should be 9"


def test_empty_function_list():
    assert chain([], 5) == 5, "Should return input value unchanged"


def test_single_function():
    def double(x):
        return x * 2

    assert chain([double], 3) == 6, "Should be 6"


def test_string_operations():
    def add_hello(x):
        return "Hello " + x

    def add_exclamation(x):
        return x + "!"

    def to_upper(x):
        return x.upper()

    assert chain([to_upper, add_hello, add_exclamation], "world") == "HELLO WORLD!", (
        "Should transform string correctly"
    )


def test_list_operations():
    def add_one(x):
        return [i + 1 for i in x]

    def multiply_two(x):
        return [i * 2 for i in x]

    def square(x):
        return [i**2 for i in x]

    assert chain([add_one, multiply_two, square], [1, 2, 3]) == [3, 9, 19], (
        "Should transform list correctly"
    )


def test_lambda_functions():
    functions = [lambda x: x + 1, lambda x: x * 2, lambda x: x**2]
    assert chain(functions, 2) == 9, "Should work with lambda functions"


def test_error_handling():
    def bad_function(x):
        raise ValueError("Test error")

    try:
        chain([bad_function], 1)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert str(e) == "Test error", "Should propagate original error"


def test_type_conversion():
    def to_str(x):
        return str(x)

    def add_prefix(x):
        return "num_" + x

    def to_upper(x):
        return x.upper()

    assert chain([to_upper, add_prefix, to_str], 42) == "NUM_42", (
        "Should handle type conversions"
    )
