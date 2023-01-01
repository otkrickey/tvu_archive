import numpy as np


def npint_power(x: np.integer) -> tuple[int, int]:
    """Calculates the power of an integer.

    Parameters
    ----------
    x : np.integer
        The integer to be calculated.

    Returns
    -------
    tuple[np.integer, int]
        The power of the integer.

    """
    if x == 0:
        return (0, 0)
    e = 0
    while x % 10 == 0:
        x //= 10
        e += 1
    return (int(x), e)
