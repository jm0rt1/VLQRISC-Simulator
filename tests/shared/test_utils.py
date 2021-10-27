import unittest
from src.Shared.utils import convert_int_bin_str, int_to_sign_extended_bin_str, signed_bin_str_to_int


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

        out_string = convert_int_bin_str(20, 32)
        expected = "0"*27 + "10100"
        self.assertEquals(out_string, expected)

        out_string = int_to_sign_extended_bin_str(-12, 32)
        expected = "11111111111111111111111111110100"
        self.assertEquals(out_string, expected)

        integer = signed_bin_str_to_int(out_string)
        self.assertEquals(integer, -12)

        out_string = int_to_sign_extended_bin_str(20, 32)
        expected = "00000000000000000000000000010100"
        self.assertEquals(out_string, expected)

        out_string = int_to_sign_extended_bin_str(-400, 32)
        expected = "11111111111111111111111001110000"
        self.assertEquals(out_string, expected)

    def test_all_numbers(self):
        bits = 16

        lower = -2**(bits-1)
        upper = (2**(bits-1))-1

        for i in range(lower, upper+1):
            signed_binary_str: str = int_to_sign_extended_bin_str(i, bits)
            int_out = signed_bin_str_to_int(signed_binary_str)
            self.assertEquals(int_out, i)
