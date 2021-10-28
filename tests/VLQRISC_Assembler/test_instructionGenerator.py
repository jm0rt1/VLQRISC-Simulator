from dataclasses import dataclass
from typing import Optional
import unittest
from src.Shared.utils import convert_int_bin_str

from src.VLQRISC_Assembler.operations import Operations, OpTypes

from src.VLQRISC_Simulator.hw_definitions import convert_reg_common_name_to_number
import src.VLQRISC_Assembler.instructionGenerator as instructionGenerator
import src.VLQRISC_Assembler.parser as parser


class TestInstructionGenerator(unittest.TestCase):
    def test_GPR_GPR_instruction_is_generated(self):

        line_parser = parser.LineParser("$s4=$s2+$s1")
        line_data = line_parser.parse()

        ir = instructionGenerator.InstructionGenerator(line_data)
        instruction = ir.generate()

        rd = convert_int_bin_str(convert_reg_common_name_to_number("$s4"), 4)
        rs1 = convert_int_bin_str(convert_reg_common_name_to_number("$s2"), 4)
        rs2 = convert_int_bin_str(convert_reg_common_name_to_number("$s1"), 4)

        expected = Operations.ADD_REGS.value.op_code_str + \
            rd+rs1+rs2+("0"*13)

        self.assertEqual(instruction, expected)

        line_parser = parser.LineParser("$t0=$t2&$s0")
        line_data = line_parser.parse()

        ir = instructionGenerator.InstructionGenerator(line_data)
        instruction = ir.generate()

        rd = convert_int_bin_str(convert_reg_common_name_to_number("$t0"), 4)
        rs1 = convert_int_bin_str(convert_reg_common_name_to_number("$t2"), 4)
        rs2 = convert_int_bin_str(convert_reg_common_name_to_number("$s0"), 4)

        expected = Operations.AND_REGS.value.op_code_str + \
            rd+rs1+rs2+("0"*13)

        self.assertEqual(instruction, expected)

        line_parser = parser.LineParser("$t0=$t2|$s1")
        line_data = line_parser.parse()

        ir = instructionGenerator.InstructionGenerator(line_data)
        instruction = ir.generate()

        rd = convert_int_bin_str(convert_reg_common_name_to_number("$t0"), 4)
        rs1 = convert_int_bin_str(convert_reg_common_name_to_number("$t2"), 4)
        rs2 = convert_int_bin_str(convert_reg_common_name_to_number("$s1"), 4)

        expected = Operations.OR_REGS.value.op_code_str + \
            rd+rs1+rs2+("0"*13)

        self.assertEqual(instruction, expected)

    def test_loop(self):

        for scheme in io_schemes:

            line_parser = parser.LineParser(scheme.input)
            line_data = line_parser.parse()

            ir = instructionGenerator.InstructionGenerator(line_data)
            instruction = ir.generate()
            if scheme.rd:
                rd = convert_int_bin_str(
                    convert_reg_common_name_to_number(scheme.rd), 4)
            if scheme.rs1:
                rs1 = convert_int_bin_str(
                    convert_reg_common_name_to_number(scheme.rs1), 4)
            if scheme.rs2:
                rs2 = convert_int_bin_str(
                    convert_reg_common_name_to_number(scheme.rs2), 4)

            opcode = scheme.op_code_str

            if line_data.type == OpTypes.UNCOND_BRANCH:
                pass
            if line_data.type == OpTypes.GPR_GPR:
                expected_instruction = opcode+rd+rs1+rs2+"0"*13
            else:
                raise Exception("Type not found")

            self.assertEqual(instruction, expected_instruction)


@ dataclass(frozen=True)
class Scheme():
    """a docstring"""
    input: str
    rd: Optional[str]
    rs1: Optional[str]
    rs2: Optional[str]
    op_code_str: str


io_schemes = [
    Scheme("$s4=$s2+$s1", "$s4", "$s2", "$s1",
           Operations.ADD_REGS.value.op_code_str),
    Scheme("$s3=$t2  | $t3", "$s3", "$t2",
           "$t3", Operations.OR_REGS.value.op_code_str)
]
