from __future__ import annotations
import enum
from typing import Any, Callable, Union
from src.VLQRISC_Simulator.hw_definitions import MEMORY_SIZE, REGISTER_NAMES
from src.Shared.fwi import FWI, FWI_unsigned


class IncompatibleOpCode(Exception):
    pass


class VLQRISC_System():
    class REGISTER():
        def __init__(self, name: str, number: int):
            self.NAME = name
            self.NUMBER = number
            self.s = FWI(0, 32)
            self.u = FWI_unsigned(0, 32)

        def set_unsigned(self, u_value: FWI_unsigned):
            self.s = FWI.from_unsigned(u_value)
            self.u = u_value

        def set_signed(self, s_value: FWI):
            self.s = s_value
            self.u = FWI_unsigned.from_signed(s_value)

        def set_automatic(self, value: Union[FWI, FWI_unsigned]):
            if isinstance(value, FWI):
                self.set_signed(value)
            else:
                self.set_unsigned(value)

    class ALU():
        def __init__(self):
            self.a = None  # input
            self.b = None  # input
            self.c = None

        def set_operands(self, a: Union[FWI, FWI_unsigned], b: Union[FWI, FWI_unsigned]):
            self.a = a  # input
            self.b = b  # input

        def ADD(self, a: FWI, b: FWI) -> FWI:
            self.set_operands(a, b)
            return a+b

        def ADD_UNSIGNED(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            return a+b

        def AND(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            string = ""
            for i, bit in enumerate(a.bits):
                if bit == 1 and b.bits[i] == 1:
                    string += "1"
                else:
                    string += "0"
            return FWI_unsigned.from_binary_str(string)

        def OR(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            string = ""
            for i, bit in enumerate(a.bits):
                if (bit == 1 and b.bits[i] == 1) or bit != b.bits[i]:
                    string += "1"
                else:
                    string += "0"
            return FWI_unsigned.from_binary_str(string)

        def XOR(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            string = ""
            for i, bit in enumerate(a.bits):
                if bit != b.bits[i]:
                    string += "1"
                else:
                    string += "0"
            return FWI_unsigned.from_binary_str(string)

    def __init__(self):
        self.memory_table = []
        self.memory_table = [FWI_unsigned(0, 8)] * MEMORY_SIZE

        self.register_table: list[VLQRISC_System.REGISTER] = []
        for i, name in enumerate(REGISTER_NAMES):
            self.register_table.append(
                self.REGISTER(name, i))

        self.alu = self.ALU()

    @property
    def register_table_bits(self) -> list[tuple[str, str]]:
        register_table_bits: list[tuple[str, str]] = []
        for reg in self.register_table:
            register_table_bits.append((reg.NAME, reg.u.bits))
        return register_table_bits

    def execute(self, instruction: Instruction):

        segments = instruction.segments
        _ = instruction.fwi.bits
        opcode = segments[0]

        for op in Operations.__members__.values():
            if op.value.op_code == opcode.int:
                cpu_operation: Callable[[VLQRISC_System.ALU, FWI, FWI],
                                        FWI] = op.value.cpu_operation

                break
        else:
            raise IncompatibleOpCode(
                f"Provided opcode cannot be executed: {opcode.int}/0b{opcode.bits} ")
        if instruction.type == OpTypes.GPR_GPR:
            rd = self.register_table[segments[1].int]
            rs1 = self.register_table[segments[2].int]
            rs2 = self.register_table[segments[3].int]
            rd.set_automatic(cpu_operation(self.alu, rs1.s, rs2.s))
        elif instruction.type == OpTypes.NUM_GPR:
            rd = self.register_table[segments[1].int]
            rs1 = self.register_table[segments[2].int]
            immediate = segments[3]
            rd.set_automatic(cpu_operation(self.alu, rs1.s, immediate))
        pass


class ReplacementTokens(str, enum.Enum):
    GPR = "GPR"  # General Purpose Register (GPR)
    NUM = "NUM"
    ADDRESS = "ADDR"


class OpTypes(str, enum.Enum):
    GPR_GPR = "register_with_register"
    NUM_GPR = "num_with_register"  # number with GPR
    COMP_BRANCH = "comparison_branch"
    UNCOND_BRANCH = "unconditional_branch"


class Operation():
    def __init__(self, name: str,  syntax_tokens: list[list[str]], type: OpTypes, op_code: int, cpu_operation: Any = None):
        self.name = name
        self.syntax_tokens = syntax_tokens
        self.type = type
        self.op_code = op_code
        self.cpu_operation = cpu_operation

    @property
    def op_code_str(self):
        string = bin(self.op_code)
        return string[2:].zfill(5)

    @property
    def op_code_fwi(self):
        return FWI_unsigned(self.op_code, 5)

    def __str__(self):
        return f"""{self.name}: Opcode = {self.op_code_str} {self.syntax_tokens}"""


class Operations(enum.Enum):

    ADD_REGS = Operation("ADD_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                             "+", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00000, VLQRISC_System.ALU.ADD)

    ADD_REG_TO_NUM = Operation("ADD_REG_TO_NUM",
                               [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "+", ReplacementTokens.NUM],
                                [ReplacementTokens.GPR, "=", ReplacementTokens.NUM, "+", ReplacementTokens.GPR]],
                               OpTypes.NUM_GPR,
                               0b00001, VLQRISC_System.ALU.ADD)

    AND_REGS = Operation("AND_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                             "&", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00010, VLQRISC_System.ALU.AND)

    AND_REG_W_NUM = Operation("AND_REG_W_NUM",
                              [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM],
                               [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM]],
                              OpTypes.NUM_GPR, 0b00011, VLQRISC_System.ALU.AND)

    OR_REGS = Operation("OR_REGS",
                        [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR], [
                            ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR]],
                        OpTypes.GPR_GPR,
                        0b00100, VLQRISC_System.ALU.OR)

    OR_REG_W_NUM = Operation("OR_REG_WITH_NUM",
                             [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM],
                                 [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM]],
                             OpTypes.GPR_GPR,
                             0b00101, VLQRISC_System.ALU.OR)

    BRANCH_IF_EQUAL = Operation("BRANCH_IF_EQUAL", [
                                ["if", '(', ReplacementTokens.GPR, "==", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00110)

    BRANCH_IF_NOT_EQUAL = Operation("BRANCH_IF_NOT_EQUAL", [
        ["if", '(', ReplacementTokens.GPR,  "!=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00111)

    BRANCH_GT_OR_EQUAL = Operation("BRANCH_IF_GREATER_THAN_OR_EQUAL", [[
                                   "if", '(', ReplacementTokens.GPR,  ">=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01000)

    BRANCH_GT = Operation("BRANCH_IF_GREATER_THAN", [[
        "if", '(', ReplacementTokens.GPR,  ">", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01001)

    BRANCH_LT_OR_EQUAL = Operation("BRANCH_IF_LESS_THAN_OR_EQUAL", [[
        "if", '(', ReplacementTokens.GPR,  "<=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01010)

    BRANCH_LT = Operation("BRANCH_IF_LESS_THAN", [[
        "if", '(', ReplacementTokens.GPR,  "<", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01011)

    JUMP = Operation("JUMP", [
        ["j", ReplacementTokens.ADDRESS]], OpTypes.UNCOND_BRANCH, 0b01100)


operators: list[str] = []
for op in Operations:
    tokens = op.value.syntax_tokens
    for list in tokens:
        for token in list:
            if token not in operators and token not in ReplacementTokens:
                operators.append(token)


class Instruction():
    def __init__(self, fwi: FWI_unsigned, type: OpTypes):
        self.fwi: FWI_unsigned = fwi
        self.type = type

    @property
    def segments(self) -> list[FWI_unsigned]:
        if self.type == OpTypes.GPR_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[15:18], self.fwi[0:14]]
        elif self.type == OpTypes.NUM_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], FWI.from_unsigned(self.fwi[0:18])]

        else:
            return [self.fwi]
