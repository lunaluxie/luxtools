from .partial import partial


def test_function_with_keyword_arguments():
    @partial
    def test(a,b,c,d=5):
        return a+b+c+d

    assert test(1,2,3) == 11, "Should be 11"