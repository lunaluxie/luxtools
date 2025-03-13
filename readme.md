# Funkypy

A collection of functional programming utilities for Python.


```
partial
```

Okay so i think I understand the problem of multiple partial:
- @partial return a function, and it's that function we edit to apply it. 
- It should return the function we get to return the function that can the be partialled every time we try again. 
    - maybe upon successful call 
    - or maybe should give up and use functools.partial. 



# Significant Figures

## Installation
Navigate to the root directory of the repository and run the following command:

```bash
pip install -e . 
```

## Usage
```python
from significant_figures import NumericResult

result = NumericResult(value=1.2345, uncertainty=0.01, unit='m')

print(result)
# Output: (1.23 ± 0.01) m

print(result.latex(delimiter=""))
# Output: (1.23 \\pm 0.01) m
```


## Examples
```Python
Value, Uncertainty, expected result. 
(1e-4, 1e-5, "(1.0 +/- 0.1)*10^(-4)"),
(1, 0.1, "(1.0 +/- 0.1)"),
(1.234, 0.193, "(1.2 +/- 0.2)"),
(0.1, 1, "(0 +/- 1)"),
(234.23424,10, "(2.3 +/- 0.1)*10^(2)"),
(0, 0, "(0 +/- 0)"),
(10, 0, "(1.0 +/- 0.0)*10^(1)"),
(0, 10, "(0 +/- 1)*10^(1)"),
(0.123456789, 0.987654321, "(1 +/- 10)*10^(-1)"),
(123456789, 987654321, "(1 +/- 10)*10^(8)"),
(1.23456789e-9, 9.87654321e-11, "(1.23 +/- 0.10)*10^(-9)"),
```