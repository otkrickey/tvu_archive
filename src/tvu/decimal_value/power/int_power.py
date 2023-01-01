def int_power(x: int) -> tuple[int, int]:
    """Calculates the power of an integer.

    Parameters
    ----------
    x : int
        The integer to be calculated.

    Returns
    -------
    tuple[int, int]
        The power of the integer.

    """
    if x == 0:
        return (0, 0)
    e = 0
    while x % 10 == 0:
        x //= 10
        e += 1
    return (x, e)
