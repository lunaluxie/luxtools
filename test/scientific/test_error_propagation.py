import torch

from luxtools import get_error

eps = 1e-4


def test_single():
    x = torch.tensor([1.0], dtype=torch.float32, requires_grad=True)
    x.sigma = torch.tensor([0.1], dtype=torch.float32)

    y = torch.tensor([2.0], dtype=torch.float32, requires_grad=True)
    y.sigma = torch.tensor([0.2], dtype=torch.float32)

    f = x * y

    error = get_error(f)

    assert error.shape == (1,), f"Shape should be (1,), actual {error.shape}"

    assert error - 0.2828 < eps, "Error is not correct"


def test_basic():
    x = torch.tensor([1.0, 3.0], dtype=torch.float32, requires_grad=True)
    x.sigma = torch.tensor([0.1, 0.2], dtype=torch.float32)

    y = torch.tensor([2.0, 4.0], dtype=torch.float32, requires_grad=True)
    y.sigma = torch.tensor([0.2, 0.3], dtype=torch.float32)

    f = x * y

    error = get_error(f)

    assert torch.all(error - torch.tensor([0.2828, 1.2042]) < eps), (
        "Error is not correct"
    )


def test_zero_grad():
    x = torch.tensor([1.0, 3.0], dtype=torch.float32, requires_grad=True)
    x.sigma = torch.tensor([0.1, 0.2], dtype=torch.float32)
    y = torch.tensor([2.0, 4.0], dtype=torch.float32, requires_grad=True)
    y.sigma = torch.tensor([0.2, 0.3], dtype=torch.float32)

    f = x * y

    # compute gradients of f, without zeroing out the gradients
    get_error(f, zero_grad=False)

    g = f * x
    error_g_no_zero = get_error(g, zero_grad=True)

    f = x * y
    g = f * x
    error_g_with_zero = get_error(g)

    assert torch.all(error_g_no_zero - error_g_with_zero > eps), (
        "The errors should be different"
    )

    expected_correct_error = torch.tensor([0.4472, 5.5073])
    assert torch.all(error_g_with_zero - expected_correct_error < eps), (
        "Error with zero gradient should be correct",
        "got:",
        error_g_with_zero,
        "Expected:",
        expected_correct_error,
    )
