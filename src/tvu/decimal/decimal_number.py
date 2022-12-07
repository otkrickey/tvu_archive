import numpy as np

from .power import decimal_power


class DecimalNumber:
    """
    DecimalNumber is a class that represents a number in decimal form.


    Parameters
    ----------
    x : int | float | np.integer
        The number to be represented in decimal form.

    Attributes
    ----------
    _x : int | float | np.integer
        The number what is given as an argument.
    _dd : int
        The number of decimal digits which is given as an argument.
    s : int
        The sign of the number.
    x : int
        The number in decimal form.
    e : int
        The exponent of the number.

    """
    _x: int | float | np.integer
    s: int
    x: int
    e: int

    @property
    def X(self) -> int | float | np.integer:
        return self.s * self.x * 10 ** self.e

    def __init__(self, x, e=None, s=None) -> None:
        if isinstance(x, DecimalNumber) and e is None and s is None:
            self._x = x.x * 10 ** x.e
            self.s = x.s
            self.x = x.x
            self.e = x.e
        elif isinstance(e, int) and isinstance(x, int | np.integer):
            self._x = x * 10 ** e
            self.s = (1 if x > 0 else -1 if x < 0 else 0) * (1 if s is None else s)
            self.x, self.e = int(abs(x)), e
        elif not isinstance(x, np.floating) and isinstance(x, int | float | np.integer):
            self._x = x
            self.s = 1 if x > 0 else -1 if x < 0 else 0
            self.x, self.e = decimal_power(abs(x))
        else:
            raise TypeError(f"Unsupported type {type(x)}")

    def __repr__(self) -> str:
        s = '-' if self.s == -1 else ''
        e = f'e{self.e}' if self.e != 0 else ''
        return f"DecimalNumber({s}{self.x}{e})"

    def __str__(self) -> str:
        return f"{self.x}e{self.e}"

    def __eq__(self, other) -> bool:
        other = DecimalNumber(other)
        if self.e == other.e:
            return self.s * self.x == other.s * other.x
        elif self.e > other.e:
            return self.s * self.x * 10 ** (self.e - other.e) == other.s * other.x
        else:
            return self.s * self.x == other.s * other.x * 10 ** (other.e - self.e)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        other = DecimalNumber(other)
        if self.e == other.e:
            return self.s * self.x < other.s * other.x
        elif self.e > other.e:
            return self.s * self.x * 10 ** (self.e - other.e) < other.s * other.x
        else:
            return self.s * self.x < other.s * other.x * 10 ** (other.e - self.e)

    def __le__(self, other) -> bool:
        other = DecimalNumber(other)
        return not self.__gt__(other)

    def __gt__(self, other) -> bool:
        other = DecimalNumber(other)
        if self.e == other.e:
            return self.s * self.x > other.s * other.x
        elif self.e > other.e:
            return self.s * self.x * 10 ** (self.e - other.e) > other.s * other.x
        else:
            return self.s * self.x > other.s * other.x * 10 ** (other.e - self.e)

    def __ge__(self, other) -> bool:
        return not self.__lt__(other)

    def __abs__(self) -> 'DecimalNumber':
        return DecimalNumber(self.x, self.e)

    def __add__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        if self.e == other.e:
            return DecimalNumber(self.s * self.x + other.s * other.x, self.e)
        elif self.e > other.e:
            return DecimalNumber(self.s * self.x * 10 ** (self.e - other.e) + other.s * other.x, e=other.e)
        else:
            return DecimalNumber(self.s * self.x + other.s * other.x * 10 ** (other.e - self.e), self.e)

    def __sub__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        if self.e == other.e:
            return DecimalNumber(self.s * self.x - other.s * other.x, self.e)
        elif self.e > other.e:
            return DecimalNumber(self.s * self.x * 10 ** (self.e - other.e) - other.s * other.x, e=other.e)
        else:
            return DecimalNumber(self.s * self.x - other.s * other.x * 10 ** (other.e - self.e), self.e)

    def __mul__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return DecimalNumber(self.s * self.x * other.s * other.x, self.e + other.e)

    def __truediv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return DecimalNumber(int(self.s * self.x / (other.s * other.x)), self.e - other.e)

    def __floordiv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return DecimalNumber(int(self.s * self.x // (other.s * other.x)), self.e - other.e)

    def __mod__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return DecimalNumber(self.s * self.x % (other.s * other.x), self.e - other.e)

    def __pow__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        power = self.e * other.X
        return DecimalNumber(((self.s * self.x) ** other.X) * 10 ** (power - int(power)), int(power))

    def __radd__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__add__(self)

    def __rsub__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__sub__(self)

    def __rmul__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__mul__(self)

    def __rtruediv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__truediv__(self)

    def __rfloordiv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__floordiv__(self)

    def __rmod__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__mod__(self)

    def __rpow__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return other.__pow__(self)

    def __iadd__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__add__(other)

    def __isub__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__sub__(other)

    def __imul__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__mul__(other)

    def __itruediv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__truediv__(other)

    def __ifloordiv__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__floordiv__(other)

    def __imod__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__mod__(other)

    def __ipow__(self, other) -> 'DecimalNumber':
        other = DecimalNumber(other)
        return self.__pow__(other)

    def __neg__(self) -> 'DecimalNumber':
        return DecimalNumber(self.x, self.e, self.s * -1)

    def __pos__(self) -> 'DecimalNumber':
        return DecimalNumber(self.x, self.e, self.s)

    def round(self, ndigits=0) -> 'DecimalNumber':
        min_digits = -ndigits - self.e
        floordiv = DecimalNumber(self.x // (10 ** min_digits), self.e + min_digits)
        mod = DecimalNumber(self.x % (10 ** min_digits), self.e + min_digits - 1)
        return floordiv + DecimalNumber(1 if mod >= DecimalNumber(5) else 0, self.e + min_digits)

    def floor(self, ndigits=0) -> 'DecimalNumber':
        min_digits = -ndigits - self.e
        floordiv = DecimalNumber(self.x // (10 ** min_digits), self.e + min_digits)
        return floordiv

    def ceil(self, ndigits=0) -> 'DecimalNumber':
        min_digits = -ndigits - self.e
        floordiv = DecimalNumber(self.x // (10 ** min_digits), self.e + min_digits)
        mod = DecimalNumber(self.x % (10 ** min_digits), self.e + min_digits - 1)
        return floordiv + DecimalNumber(1 if mod > DecimalNumber(0) else 0, self.e + min_digits)

    def __int__(self) -> int:
        if self.s == 0:
            return 0
        elif self.e > 0:
            return self.s * int(str(self.x * 10 ** self.e))
        elif self.e == 0:
            return self.s * self.x
        else:
            return self.s * int(str(self.x)[:-self.e])

    def __float__(self) -> float:
        return float(self.s * self.x * 10 ** self.e)

    def __bool__(self) -> bool:
        return self.s > 0

    def __format__(self, format_spec) -> str:
        if format_spec == 'console':
            return f'{self.s * self.x * 10 ** self.e}'
        elif format_spec == 'latex':
            return f'{self.s * self.x * 10 ** self.e}'
        else:
            return self.__str__()
