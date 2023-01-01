import math
from dataclasses import dataclass
from decimal import Decimal
from typing import Type, TypeAlias

import numpy as np


@dataclass
class tvu:
    v: int | float | np.floating | Decimal
    e: int | float | np.floating | Decimal
    d: int = 0
    s: int = 0


class TypicalValueWithUncertainty:
    """
    StandardWithUncertainty
    =======================

    Provides a class that represents a typical value with uncertainty.

    Attributes
    ----------
    v: np.float64
        Typical value.
        Preferred type: np.float64, positive
    e: np.float64
        Uncertainty.
        Preferred type: np.float64, positive
    d: int, default 0
        Decimal digit.
        Preferred type: int
    s: int, default 1
        Symbol of Typical value.
        1: positive
        0: zero
        -1: negative
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a StandardWithUncertainty object.

        Examples
        --------
        >>> StandardWithUncertainty([1, 2, 3, ...])
        >>> su1 = StandardWithUncertainty(1.234, 0.001, 2)
        >>> su1
        (1.234 ± 0.001) × 10^2
        >>> su2 = StandardWithUncertainty(su1)
        >>> su2
        (1.234 ± 0.001) × 10^2
        >>> su3 = StandardWithUncertainty(1.234, 0.001, 2, -1)
        >>> su3
        -(1.234 ± 0.001) × 10^2
        """

        self.dtype = self.__dtype(kwargs.get('dtype', np.float64))
        self.v: np.floating
        self.e: np.floating
        self.d: int
        self.s: int

        # check args
        _ = tvu(0, 0, 0, 0)
        if len(args) == 1 and isinstance(args[0], tvu): _: tvu = args[0]
        elif len(args) == 1 and isinstance(args[0], np.ndarray):
            if args[0].ndim != 1: raise ValueError('np.ndarray must be 1-dim')
            array = np.array(args[0], dtype=self.dtype)
            _.v = self.dtype(np.average(array))
            _.e = self.dtype(np.std(array, ddof=1, dtype=self.dtype) / np.sqrt(len(array), dtype=self.dtype))
        elif len(args) == 1 and isinstance(args[0], TypicalValueWithUncertainty):
            _.v = args[0].v
            _.e = args[0].e
            _.d = args[0].d
            _.s = args[0].s
        elif len(args) >= 1:
            if not self.__floating(args[0]): raise TypeError('Typical value must be int, float, np.floating or Decimal')
            _.v = self.dtype(args[0])
            if len(args) >= 2 and not self.__floating(args[1]): raise TypeError('Uncertainty must be int, float, np.floating or Decimal')
            _.e = self.dtype(args[1]) if len(args) >= 2 else self.dtype(0)
            if len(args) >= 3 and not isinstance(args[2], int): raise TypeError('Decimal digit must be int')
            _.d = args[2] if len(args) >= 3 else 0
            if len(args) >= 4 and not isinstance(args[3], int): raise TypeError('Symbol of Typical value must be int')
            _.s = args[3] if len(args) >= 4 else 0
        else: raise ValueError('Invalid arguments')

        # validate args
        if _.v < 0:
            _.v = abs(_.v)
            _.s *= -1
        elif _.v == 0: _.s = 0
        if _.e < 0: _.e = abs(_.e)

        # set attributes
        self.v = self.dtype(_.v)
        self.e = self.dtype(_.e)
        self.d = _.d
        self.s = _.s

    def __dtype(self, T) -> Type[np.float16 | np.float32 | np.float64 | np.float128]:
        if T in [np.float16, np.float32, np.float64, np.float128]: return T
        else: return np.float64

    def __floating(self, x): return isinstance(x, int | float | np.floating | Decimal)

    @property
    def V(self) -> int | float | np.floating: return self.s * self.v * 10 ** self.d

    @property
    def E(self) -> int | float | np.floating: return self.e * 10 ** self.d

    @property
    def V_d(self) -> int: return 0 if self.v == 0 else math.floor(np.log10(self.v)) + self.d

    @property
    def E_d(self) -> int: return 0 if self.e == 0 else math.floor(np.log10(self.e)) + self.d

    def __add__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = self.V + other
            e = self.E
        elif isinstance(other, TypicalValueWithUncertainty):
            v = self.V + other.V
            e = math.sqrt(self.E ** 2 + other.E ** 2)
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e, dtype=self.dtype)

    def __sub__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = self.V - other
            e = self.E
        elif isinstance(other, TypicalValueWithUncertainty):
            v = self.V - other.V
            e = math.sqrt(self.E ** 2 + other.E ** 2)
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e)

    def __mul__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = self.V * other
            e = self.E * other
        elif isinstance(other, TypicalValueWithUncertainty):
            v = self.V * other.V
            e = math.sqrt((self.E / self.V) ** 2 + (other.E / other.V) ** 2) * v
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e)

    def __truediv__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = self.V / other
            e = self.E / other
        elif isinstance(other, TypicalValueWithUncertainty):
            v = self.V / other.V
            e = math.sqrt((self.E / self.V) ** 2 + (other.E / other.V) ** 2) * v
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e)

    def __pow__(self, other, modulo=None) -> 'TypicalValueWithUncertainty':
        if modulo is not None: raise NotImplementedError
        if self.s == -1: raise NotImplementedError
        elif self.s == 0: return TypicalValueWithUncertainty(0, self.e, self.d)
        else:
            if isinstance(other, int | float | np.floating):
                self.reset_digit_v(0)
                _d = self.d * other
                _d_float = 10 ** (_d - math.floor(_d))
                v = _d_float * self.v ** other
                e = v * other * self.e / self.v
                d = math.floor(_d)
                return TypicalValueWithUncertainty(v, e, d)
            elif isinstance(other, TypicalValueWithUncertainty):
                # will add later
                raise NotImplementedError
            else: raise NotImplementedError

    def __radd__(self, other) -> 'TypicalValueWithUncertainty': return self.__add__(other)

    def __rsub__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = other - self.V
            e = self.E
        elif isinstance(other, TypicalValueWithUncertainty):
            v = other.V - self.V
            e = math.sqrt(self.E ** 2 + other.E ** 2)
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e)

    def __rmul__(self, other) -> 'TypicalValueWithUncertainty': return self.__mul__(other)

    def __rtruediv__(self, other) -> 'TypicalValueWithUncertainty':
        if isinstance(other, int | float | np.floating):
            v = other / self.V
            e = other / self.V * self.E / self.V
        elif isinstance(other, TypicalValueWithUncertainty):
            v = other.V / self.V
            e = math.sqrt((other.E / other.V) ** 2 + (self.E / self.V) ** 2) * v
        else: raise NotImplementedError
        return TypicalValueWithUncertainty(v, e)

    # def __rpow__(self, other, modulo=None):
    #     if modulo is not None: raise NotImplementedError
    #     # will add later
    #     pass

    def __abs__(self) -> 'TypicalValueWithUncertainty':
        if self.s == -1: return TypicalValueWithUncertainty(self.v, self.e, self.d)
        else: return self

    def __str__(self) -> str:
        base = f'{"-"if self.s == -1 else ""}{self.v} ± {self.e}'
        exp = f'× 10^{self.d}' if self.d != 0 else ''
        return f'{base} {exp}'

    # Utils
    # def change_digit(self, d: int) -> None:
    #     """
    #     Change the decimal digit.

    #     Parameters
    #     ----------
    #     d: int
    #         Decimal digit.
    #         Preferred type: int
    #     """
    #     self.v = self.v * 10 ** (self.d - d)
    #     self.e = self.e * 10 ** (self.d - d)
    #     self.d = d

    def reset_digit_v(self, digit: int = 0) -> None:
        """
        Change the digit of StandardWithUncertainty to the digit of typical value.

        Examples
        --------
        >>> su = StandardWithUncertainty(123.456, 0.011)
        >>> su.reset_digit_v(0)
        >>> su.v, su.e, su.d
        (1.23456, 0.00011, 2)

        Parameters
        ----------
        digit: int, default 0
            Decimal digit.
            Restricted type: int
        """
        v = self.v * 10**(digit - self.V_d)
        e = self.e * 10**(digit - self.V_d)
        d = self.d - (digit - self.V_d)
        self.v = v
        self.e = e
        self.d = d

    def reset_digit_e(self, digit: int = 0) -> None:
        """
        Change the digit of StandardWithUncertainty to the digit of uncertainty.

        Examples
        --------
        >>> su = StandardWithUncertainty(123.456, 0.011)
        >>> su.reset_digit_e(0)
        >>> su.v, su.e, su.d
        (12345.6, 1.1, -2)

        Parameters
        ----------
        digit: int, default 0
            Decimal digit.
            Restricted type: int
        """
        v = self.v
        e = self.e * 10**(digit - self.E_d)
        d = self.d - (digit - self.E_d)
        self.v = v
        self.e = e
        self.d = d

    def quantize_v(self, digit: int = 0) -> tvu:
        """
        Quantize the StandardWithUncertainty to the digit of typical value.

        Examples
        --------
        >>> su = StandardWithUncertainty(123.456, 0.011)
        >>> su.quantize_v(2)
        >>> su.v, su.e, su.d
        (120, 0, 0)

        Parameters
        ----------
        digit: int, default 0
            Decimal digit.
            Restricted type: int
        """
        v = Decimal(str(self.v)).quantize(Decimal(str(10 ** (self.V_d - digit))))
        e = Decimal(str(self.e)).quantize(Decimal(str(10 ** (self.V_d - digit))))
        return tvu(v, e)

    def quantize_e(self, digit: int = 1) -> tvu:
        """
        Quantize the StandardWithUncertainty to the digit of uncertainty.

        Examples
        --------
        >>> su = StandardWithUncertainty(123.456, 0.011)
        >>> su.quantize_e(1)
        >>> su.v, su.e, su.d
        (123.5, 0.01, 0)

        Parameters
        ----------
        digit: int, default 1
            Decimal digit.
            Restricted type: int
        """
        v = Decimal(str(self.v)).quantize(Decimal(str(10 ** (self.E_d - digit))))
        e = Decimal(str(self.e)).quantize(Decimal(str(10 ** (self.E_d - digit))))
        return tvu(v, e)

    def texd(self, digit: int = 0, initial: bool = False) -> str:
        self.reset_digit_v()
        v = Decimal(str(self.v)).quantize(Decimal(str(10 ** (self.E_d - digit - self.d))))
        e = Decimal(str(self.e)).quantize(Decimal(str(10 ** (self.E_d - digit - self.d))))
        exponent = f'\\cdot 10^{{{self.d}}}' if self.d != 0 else ''
        return f'{"-" if self.s == -1 else "" if initial else "+"}({v} \\pm {e}){exponent}'


def main():
    I = TypicalValueWithUncertainty(60.642, 0.04)
    print(I)
    I.reset_digit_v(2)
    print(I)


if __name__ == '__main__': main()
