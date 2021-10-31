from dataclasses import dataclass
from typing import Optional
import unittest
from src.Shared.utils import convert_int_bin_str

from src.VLQRISC_Simulator.system import Operations, OpTypes

from src.VLQRISC_Simulator.hw_definitions import convert_reg_common_name_to_number
import src.VLQRISC_Assembler.instructionGenerator as instructionGenerator
import src.VLQRISC_Assembler.parser as parser


class TestInstructionGenerator(unittest.TestCase):

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
            if scheme.immediate_operand:
                immediate_str = convert_int_bin_str(
                    scheme.immediate_operand, 19)

            opcode = scheme.op_code_str

            if line_data.type == OpTypes.UNCOND_BRANCH:
                pass
            if line_data.type == OpTypes.GPR_GPR:
                expected_instruction = opcode+rd+rs1+rs2+"0"*15  # type:ignore
                expected_segments = [opcode, rd,  # type:ignore
                                     rs1, rs2, "0"*15]  # type:ignore
            elif line_data.type == OpTypes.NUM_GPR:
                expected_instruction = opcode+rd+rs1+immediate_str  # type:ignore
                expected_segments = [opcode, rd, rs1,  # type:ignore
                                     immediate_str]  # type:ignore
            else:
                raise Exception("Type not found")

            self.assertEqual(len(expected_instruction), 32)

            self.assertEqual(instruction.fwi.bits, expected_instruction)
            for i, segment in enumerate(expected_segments):
                self.assertEqual(instruction.segments[i].bits, segment)


@ dataclass(frozen=True)
class Scheme():
    """a docstring"""
    input: str
    rd: Optional[str]
    rs1: Optional[str]
    rs2: Optional[str]
    op_code_str: str
    immediate_operand: Optional[int]


io_schemes = [
    Scheme("$s4=$s2+300", "$s4", "$s2", None,
           Operations.ADD_REG_TO_NUM.value.op_code_str, 300),
    Scheme("$s4=$s2+$s1", "$s4", "$s2", "$s1",
           Operations.ADD_REGS.value.op_code_str, None),
    Scheme("$s3=$t2  | $t3", "$s3", "$t2",
           "$t3", Operations.OR_REGS.value.op_code_str, None),

]
