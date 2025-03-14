# LuxTools
> A collection of tools and utilities that I often use in my work.

## Features

- **[Scientific](#scientific)**
  - [Error propagation](#error-propagation) for numerical calculations
  - [Pretty printing](#numeric-result-formatting) of numerical results with uncertainties
- **[Functional](#functional)**
  - [Function composition](#function-composition) utilities
  - [Partial function](#partial-application) application
  - [Overload function](#overload-function-definitions) definitions

## Installation

```bash
pip install luxtools
```

## Usage

### Scientific

#### Error Propagation

```python
import torch
from luxtools import get_error

# Create tensors with uncertainties
x = torch.tensor([1.0, 3.0], dtype=torch.float32, requires_grad=True)
x.sigma = torch.tensor([0.1, 0.2], dtype=torch.float32)

y = torch.tensor([2.0, 4.0], dtype=torch.float32, requires_grad=True)
y = Variable(y, torch.tensor([0.2, 0.3]))

# Perform calculations
f = x * y

# Get propagated error
error = get_error(f)
# tensor([0.2828, 1.2042])
```

#### Numeric Result Formatting

```python
from luxtools import NumericResult

# Create a measurement with uncertainty
result = NumericResult(1.234, 0.193)
print(result)
# (1.2 ± 0.2)

# Scientific notation
result = NumericResult(234.23424, 10)
print(result)
# (2.3 ± 0.1)*10^(2)

# LaTeX output
print(result.latex())
# (2.3 \pm 0.1)\cdot 10^{2}
```

### Functional

#### Function Composition

```python
from luxtools import chain

# Compose functions
f = lambda x: x + 1
g = lambda x: x * 2
h = lambda x: x ** 2

# Create a new function that applies f, then g, then h
composed = chain(f, g, h)

result = composed(3)  # ((3 + 1) * 2) ** 2 = 64
```

#### Partial Application
Allows you to partially apply arguments to a function, creating a new function with fewer arguments. See [article](https://lunalux.io/functional-programming-in-python/better-currying-in-python/) for discussion.

```python
from luxtools import partial

@partial
def greet(greeting, name):
    return f"{greeting}, {name}!"

# Create a new function with 'Hello' fixed as the greeting
say_hello = greet("Hello")

result = say_hello("World")  # "Hello, World!"
```

#### Overload function definitions

Allows you to have multiple function definitions for the same function name. 
It uses typehints to determine which function to call. See [article](https://lunalux.io/functional-programming-in-python/overloading-functions-in-python/) for discussion.

```python
from luxtools import overload

class Email:
    def __init__(self, email: str):
        self.email = email

    def __str__(self) -> str:
        return self.email


class PhoneNumber:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def __str__(self) -> str:
        return self.phone_number


@overload
def get_user(email: Email):
    print("Email:", email)
    return email


@overload
def get_user(phone_number: PhoneNumber):
    print("Phone:", phone_number)
    return phone_number

get_user(Email("test@example.com"))  # prints: Email: test@example.com
get_user(PhoneNumber("123-456-789"))  # prints: Phone: 123-456-789
```

Caveat, if the function is defined in a non-global scope such as a class, or inside a function, then you need to pass the local scope to the decorator. 

```python
def local_scope():
    @overload(scope=locals())
    def get_user(email: Email):
        print("Email:", email)

    @overload(scope=locals())
    def get_user(phone_number: PhoneNumber):
        print("Phone:", phone_number)
```

This is necessary because the parent stack frame doesn't exist inside the `overload` function, so it has to be passed explicitly. See [tests](test/functional/test_overload.py).