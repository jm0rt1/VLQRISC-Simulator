# fwi = Fixed Width Integers
from __future__ import annotations
from src.Shared.utils import convert_int_bin_str, int_to_sign_extended_bin_str, signed_bin_str_to_int, unsigned_bin_str_to_int
import copy


class FWIOverFlow(Exception):
    """Fixed int passed in with fixed width integer exceeds limits
    """
    pass


class FWISliceError(Exception):
    pass


class FWIOperationError(Exception):
    pass


class FWIbc():
    """
    Base class for the fixed width integer 
    """

    def __init__(self, int: int, width: int = 16) -> None:
        self.width = width
        self.int = int

    @classmethod
    def from_binary_str(cls, binary_string: str):
        return cls(unsigned_bin_str_to_int(binary_string), len(binary_string))

    def __getitem__(self, key):
        if isinstance(key, slice):

            if key.step != 1 and key.step is not None:
                raise FWISliceError("Slice cannot be obtained: step != 1 ")

            reversed_bits = copy.copy(self.bits)
            reversed_bits = reversed_bits[::-1]

            # Get the start, stop, and step from the slice
            if key.stop is not None and key.start is not None:

                least_significant = key.stop+1
                most_significant = key.start

                if 0 <= most_significant < least_significant < self.width:
                    string = reversed_bits[most_significant:least_significant][::-1]
                elif 0 <= most_significant < least_significant == self.width:
                    string = reversed_bits[most_significant:][::-1]
                else:
                    raise FWISliceError(
                        "Slice not formatted correctly")

            else:

                if key.stop is None and key.start is None:
                    string = self.bits[:]
                elif key.stop is None and key.start is not None:
                    most_significant = key.start
                    string = reversed_bits[most_significant:][::-1]
                else:
                    least_significant = key.stop
                    string = reversed_bits[:least_significant][::-1]

            return FWI.from_binary_str(string)

        elif isinstance(key, int):
            if key < 0:  # Handle negative indices
                key += len(self)
            if 0 <= key < self.width:
                return self.bits[key]  # Get the data from elsewhere
        else:
            raise TypeError("Invalid argument type.")


class FWI(FWIbc):
    def __init__(self, int: int, width: int = 16) -> None:
        super().__init__(int, width)
        self._lower = -2**(width-1)
        self._upper = (2**(width-1))-1
        if not(self._lower <= int <= self._upper):
            raise FWIOverFlow(
                "Fixed int passed in with fixed width integer exceeds limits")

    def __add__(self, other: FWI):
        if self.width != other.width:
            raise FWIOperationError(
                "Addition of numbers that are different widths is not allowed, please convert before adding")
        return FWI(other.int+self.int, self.width)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        raise FWIOperationError("Subtraction on left not allowed")

    @property
    def bits(self) -> str:
        return int_to_sign_extended_bin_str(self.int, self.width)

    @classmethod
    def from_binary_str(cls, binary_string: str):

        return cls(signed_bin_str_to_int(binary_string), len(binary_string))


class FWI_unsigned(FWIbc):
    def __init__(self, int: int, width: int = 16) -> None:
        super().__init__(int, width)
        self._lower = 0
        self._upper = (2**(width))-1
        if not(self._lower <= int <= self._upper):
            raise FWIOverFlow(
                "Fixed int passed in with fixed width integer exceeds limits")
        self.width = width
        self.int = int

    @property
    def bits(self) -> str:
        return convert_int_bin_str(self.int, self.width)

    @classmethod
    def from_binary_str(cls, binary_string: str):
        return cls(unsigned_bin_str_to_int(binary_string), len(binary_string))

    @classmethod
    def from_signed(cls, fwi: FWI):
        return cls().from_binary_str(fwi.bits)
