import unittest
import src.VLQRISC_Simulator.hw_definitions as hw_definitions


class TestHWDefinitions(unittest.TestCase):
    def test_hw_definitions(self):
        length = len(hw_definitions.REGISTER_NAMES)
        if length > 18:
            raise Exception(
                f"Can only support 16 General Purpose Registers with design -- you have {length}")
