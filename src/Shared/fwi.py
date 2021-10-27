# fwi = Fixed Width Integers
from src.Shared.utils import signed_bin_str_to_int, int_to_sign_extended_bin_str


class FWIOverFlow(Exception):
    """Fixed int passed in with fixed width integer exceeds limits
    """
    pass


class FWI():
    def __init__(self, int: int, width: int = 16) -> None:
        super().__init__()
        self._lower = -2**(width-1)
        self._upper = (2**(width-1))-1
        if self._lower <= int <= self._upper:
            raise FWIOverFlow(
                "Fixed int passed in with fixed width integer exceeds limits")
        self.width = width
        self.int = int

    def bits(self) -> str:
        return int_to_sign_extended_bin_str(self.int, self.width)


class FWI_unsigned():
    def __init__(self) -> None:
        pass
