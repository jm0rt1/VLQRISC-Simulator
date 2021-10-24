import unittest
from src.Shared.utils import convert_int_bin_str
from src.VLQRISC_Assembler import operations
from src.VLQRISC_Assembler.hw_definitions import convert_reg_common_name_to_number
import src.VLQRISC_Assembler.instructionGenerator as instructionGenerator
import src.VLQRISC_Assembler.parser as parser


class TestInstructionGenerator(unittest.TestCase):
    def test_instruction_is_generated(self):

        line_parser = parser.LineParser("$s4=$s2+$s1")
        line_data = line_parser.parse()

        ir = instructionGenerator.InstructionGenerator(line_data)
        instruction = ir.generate()

        rd = convert_int_bin_str(convert_reg_common_name_to_number("$s4"), 4)
        rs1 = convert_int_bin_str(convert_reg_common_name_to_number("$s2"), 4)
        rs2 = convert_int_bin_str(convert_reg_common_name_to_number("$s1"), 4)

        expected = operations.Operations.ADD_REGS.value.op_code_str + \
            rd+rs1+rs2+("0"*13)

        self.assertEquals(instruction, expected)

        line_parser = parser.LineParser("$s4=$s2&$s1")
        line_data = line_parser.parse()

        ir = instructionGenerator.InstructionGenerator(line_data)
        instruction = ir.generate()

        rd = convert_int_bin_str(convert_reg_common_name_to_number("$s4"), 4)
        rs1 = convert_int_bin_str(convert_reg_common_name_to_number("$s2"), 4)
        rs2 = convert_int_bin_str(convert_reg_common_name_to_number("$s1"), 4)

        expected = operations.Operations.AND_REGS.value.op_code_str + \
            rd+rs1+rs2+("0"*13)
