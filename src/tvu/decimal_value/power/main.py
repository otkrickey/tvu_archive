import numpy as np
from .float_power import float_power
from .int_power import int_power
from .npint_power import npint_power


def decimal_power(x: int | float | np.integer) -> tuple[int, int]:
    """Calculates the power of the number.

    Parameters
    ----------
    x : int | float
        The number to be calculated.

    Returns
    -------
    tuple[int, int]
        The power of the number.

    """
    if isinstance(x, int):
        return int_power(abs(x))
    elif isinstance(x, float):
        return float_power(abs(x))
    elif isinstance(x, np.integer):
        return npint_power(np.abs(x))
    else:
        raise TypeError(f"Unsupported type {type(x)}")
