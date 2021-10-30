import unittest
from src.Shared.fwi import FWI, FWISliceError


class testFWI(unittest.TestCase):
    def test_fwi(self):
        fwi = FWI(12, 5)

        expected_bits = "01100"
        self.assertEqual(fwi.bits, expected_bits)

        fwi = FWI(8, 16)
        self.assertEqual(fwi.bits, "0000000000001000")

    def test_slice(self):
        """Needed to rewrite the python slice functions such that 0 is the least significant bit and """
        fwi = FWI(8, 16)
        sliced_fwi = fwi[0:5]
        self.assertEqual(sliced_fwi.bits, "001000")
        sliced_fwi = fwi[1:5]
        self.assertEqual(sliced_fwi.bits, "00100")
        sliced_fwi = fwi[1:4]
        self.assertEqual(sliced_fwi.bits, "0100")
        sliced_fwi = fwi[2:4]
        self.assertEqual(sliced_fwi.bits, "010")
        sliced_fwi = fwi[2:3]
        self.assertEqual(sliced_fwi.bits, "10")

        fwi = FWI.from_binary_str("11101110111111")
        sliced_fwi = fwi[5:8]
        self.assertEqual(sliced_fwi.bits, "1101")

        sliced_fwi = fwi[:]
        self.assertEqual(sliced_fwi.bits, "11101110111111")

        fwi = FWI.from_binary_str("101010101010101011")
        sliced_fwi = fwi[0:4]
        self.assertEqual(sliced_fwi.bits, "01011")

        with self.assertRaises(FWISliceError):
            sliced_fwi = fwi[0:25]
            self.assertEqual(sliced_fwi.bits, "01011")
        with self.assertRaises(FWISliceError):
            sliced_fwi = fwi[-20:40]
        with self.assertRaises(FWISliceError):
            sliced_fwi = fwi[0:-1]
        with self.assertRaises(FWISliceError):
            sliced_fwi = fwi[1:0]

    def test_from_string(self):
        fwi = FWI.from_binary_str("01100")
        expected_int = 12
        expected_bits = "01100"
        self.assertEqual(expected_int, fwi.int)
        self.assertEqual(expected_bits, fwi.bits)
