from luxtools.functional import partial


def test_function_with_keyword_arguments():
    @partial
    def test(a, b, c, d=5):
        return a + b + c + d

    assert test(1, 2, 3) == 11, "Should be 11"


def test_currying_with_positional_args():
    @partial
    def add_three(a, b, c):
        return a + b + c

    assert add_three(1)(2)(3) == 6, "Should curry positional arguments"


def test_currying_with_keyword_args_stored():
    """Tests that if we are overriding the keyword arguments
    we are no trying to execute the function before it's ready.
    """

    @partial
    def greet(name, greeting="Hello", punctuation="!"):
        return f"{greeting} {name}{punctuation}"

    partial_function = greet(greeting="Hi")
    result = partial_function("Alice")

    assert result == "Hi Alice!", "Should curry with keyword arguments"


def test_currying_with_keyword_args_call():
    @partial
    def greet(name, greeting="Hello", punctuation="!"):
        return f"{greeting} {name}{punctuation}"

    assert greet(greeting="Hi")("Alice") == "Hi Alice!", (
        "Should curry with keyword arguments"
    )


def test_currying_twice():
    """Makes sure that we are creating new function pointers
    so the function can be curried multiple times"""

    @partial
    def greet(name, greeting="Hello", punctuation="!"):
        return f"{greeting} {name}{punctuation}"

    # should return a new independent function pointer.
    partial_function = greet(greeting="Heya")
    result = partial_function("Bob")

    assert result == "Heya Bob!", "Should curry with keyword arguments"

    # should also work second time
    # should use the original one.
    assert greet(greeting="Hi")("Alice") == "Hi Alice!", (
        "A curried function should be curried multiple times"
    )


def test_mixed_positional_and_keyword_args():
    @partial
    def calculate(x, y, operation="add"):
        if operation == "add":
            return x + y
        return x * y

    assert calculate(2)(y=3) == 5, (
        "Should handle mixed positional and keyword arguments"
    )
    assert calculate(2)(y=3, operation="multiply") == 6, (
        "Should handle operation override"
    )


def test_error_invalid_argument():
    @partial
    def simple_add(a, b):
        return a + b

    try:
        simple_add(1)(c=2)
        assert False, "Should raise TypeError for invalid argument"
    except TypeError as e:
        assert "unexpected keyword argument" in str(e), (
            "Should have correct error message"
        )


def test_error_too_many_arguments():
    @partial
    def simple_add(a, b):
        return a + b

    try:
        simple_add(1, 2, 3)
        assert False, "Should raise TypeError for too many arguments"
    except TypeError:
        pass