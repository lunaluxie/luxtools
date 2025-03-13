from .functional.compose import chain
from .functional.partial import partial
from .scientific.error_propagation import get_error, Variable
from .scientific.printing import NumericResult

__all__ = ['chain', 'partial', 'get_error', 'Variable', 'NumericResult']