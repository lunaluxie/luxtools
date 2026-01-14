from beartype.claw import (
    beartype_this_package,
)

beartype_this_package()

from .functional import (
    cascade_filter,
    cascade_filter_safe,
    chain,
    chain_eager,
    first,
    first_safe,
    fnot,
    head,
    identity,
    isempty,
    overload,
    partial,
)
from .scientific.error_propagation import get_error
from .scientific.printing import NumericResult