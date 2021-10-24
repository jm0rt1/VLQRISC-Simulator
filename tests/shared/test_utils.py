import unittest
from src.Shared.utils import convert_int_bin_str


class testUtils(unittest.TestCase):
    def test_convert_int_bin_str(self):
        out_string = convert_int_bin_str(1, 20)
        expected = "0"*19+"1"
        self.assertEquals(out_string, expected)

        out_string = convert_int_bin_str(2, 10)
        expected = "0"*8+"1"+"0"
        self.assertEquals(out_string, expected)

        out_string = convert_int_bin_str(1, 10)
        expected = "0"*9+"1"
        self.assertEquals(out_string, expected)

        out_string = convert_int_bin_str(20, 32)
        expected = "0"*27 + "10100"
        self.assertEquals(out_string, expected)
