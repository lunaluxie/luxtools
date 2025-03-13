from luxtools.scientific import NumericResult


def test_numeric_result():
    unit = ""

    additional_tests = [
        (1e-4, 1e-5, "(1.0 +/- 0.1)*10^(-4)"),
        (1, 0.1, "(1.0 +/- 0.1)"),
        (1.234, 0.193, "(1.2 +/- 0.2)"),
        (0.1, 1, "(0 +/- 1)"),
        (234.23424,10, "(2.3 +/- 0.1)*10^(2)"),
        (0, 0, "(0.0 +/- 0)"), # should really be (0 +/- 0)
        (10, 0, "(1 +/- 0)*10^(1)"), # should really be (1.0 +/- 0)*10^(1)
        (0, 10, "(0 +/- 1)*10^(1)"),
        (0.123456789, 0.987654321, "(1 +/- 10)*10^(-1)"),
        (123456789, 987654321, "(1 +/- 10)*10^(8)"),
        (1.23456789e-9, 9.87654321e-11, "(1.23 +/- 0.10)*10^(-9)"),
    ]

    for value, uncertainty, expected in additional_tests:
        result = NumericResult(value, uncertainty, unit)
        print(result)
        assert result.safe_str() == expected, f"Expected {expected} but got {result.safe_str()}"


def test_numeric_result_with_zero_uncertainty():
    value, uncertainty, expected = (123.456789e-9, 0, "(1.23456789 +/- 0)*10^(-7)")
    result = NumericResult(value, uncertainty, "")
    assert result.safe_str() == expected, f"Expected {expected} but got {result.safe_str()}"