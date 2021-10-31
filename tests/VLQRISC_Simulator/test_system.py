from dataclasses import dataclass
from typing import Optional
import unittest
from src.VLQRISC_Assembler.instructionGenerator import InstructionGenerator
from src.VLQRISC_Simulator.system import Operations, VLQRISC_System
from src.VLQRISC_Assembler.parser import LineParser


class Test_VLQRISC_System(unittest.TestCase):
    def test_execute(self):

        for scheme in io_schemes:

            line_parser = LineParser(scheme.input)
            line_data = line_parser.parse()

            ir = InstructionGenerator(line_data)
            instruction = ir.generate()
            system = VLQRISC_System()
            system.execute(instruction)


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
