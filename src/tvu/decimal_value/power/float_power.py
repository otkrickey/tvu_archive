def float_power(x: float) -> tuple[int, int]:
    """Calculates the power of a float.

    Parameters
    ----------
    x : float
        The float to be calculated.

    Returns
    -------
    tuple[int, int]
        The power of the float.

    Examples
    --------
    >>> float_power(1.2)
    (12, -1)

    """
    if x == 0:
        return 0, 0
    else:
        e = len(str(x).split(".")[1])
        return int(x * 10 ** e), -e


if __name__ == "__main__":
    x = 1.2
    print(float_power(x))
