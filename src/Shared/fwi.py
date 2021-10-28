# fwi = Fixed Width Integers
from src.Shared.utils import convert_int_bin_str, int_to_sign_extended_bin_str, signed_bin_str_to_int, unsigned_bin_str_to_int


class FWIOverFlow(Exception):
    """Fixed int passed in with fixed width integer exceeds limits
    """
    pass


class FWI():
    def __init__(self, int: int, width: int = 16) -> None:
        super().__init__()
        self._lower = -2**(width-1)
        self._upper = (2**(width-1))-1
        if not(self._lower <= int <= self._upper):
            raise FWIOverFlow(
                "Fixed int passed in with fixed width integer exceeds limits")
        self.width = width
        self.int = int

    @property
    def bits(self) -> str:
        return int_to_sign_extended_bin_str(self.int, self.width)

    @classmethod
    def from_binary_str(cls, binary_string: str):

        return cls(signed_bin_str_to_int(binary_string), len(binary_string))


class FWI_unsigned():
    def __init__(self, int: int, width: int = 16) -> None:
        super().__init__()
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
