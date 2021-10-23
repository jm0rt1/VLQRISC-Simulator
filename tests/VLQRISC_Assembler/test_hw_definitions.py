import unittest
import src.VLQRISC_Assembler.hw_definitions as hw_definitions


class TestHWDefinitions(unittest.TestCase):
    def test_hw_definitions(self):
        length = len(hw_definitions.RegisterNames)
        if length >= 16:
            raise Exception(
                f"Can only support 16 Registers with design -- you have {length}")
