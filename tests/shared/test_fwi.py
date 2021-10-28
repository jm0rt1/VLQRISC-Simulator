import unittest
from src.Shared.fwi import FWI


class testFWI(unittest.TestCase):
    def test_fwi(self):
        fwi = FWI(12, 5)
        expected_bits = "01100"
        self.assertEqual(fwi.bits, expected_bits)

    def test_slice(self):
        pass

    def test_from_string(self):
        fwi = FWI.from_binary_str("01100")
        expected_int = 12
        expected_bits = "01100"
        self.assertEqual(expected_int, fwi.int)
        self.assertEqual(expected_bits, fwi.bits)
