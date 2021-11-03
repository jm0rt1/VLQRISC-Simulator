from __future__ import annotations
import enum
from typing import Callable, Optional, Union
from src.VLQRISC_Simulator import hw_definitions
from src.VLQRISC_Simulator.hw_definitions import MEMORY_SIZE, REGISTER_NAMES
from src.Shared.fwi import FWI, FWI_unsigned


class IncompatibleOpCode(Exception):
    pass


class OperationNotImplemented(Exception):
    pass


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

    def LT(self, a: FWI, b: FWI) -> bool:
        return a < b

    def GT(self, a: FWI, b: FWI) -> bool:
        return a > b

    def LE(self, a: FWI, b: FWI) -> bool:
        return a <= b

    def GE(self, a: FWI, b: FWI) -> bool:
        return a >= b

    def XOR(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
        self.set_operands(a, b)
        string = ""
        for i, bit in enumerate(a.bits):
            if bit != b.bits[i]:
                string += "1"
            else:
                string += "0"
        return FWI_unsigned.from_binary_str(string)

    def EQ(self, a: FWI, b: FWI):
        return a == b

    def NEQ(self, a: FWI, b: FWI):
        return a != b


class MMU():
    """
    Memory management unit -- Big endian
    """

    def __init__(self) -> None:

        self.memory_table: list[list[FWI_unsigned]] = [
            [FWI_unsigned(0, 8)] * 4]*int(MEMORY_SIZE/4)

        pass

    def STORE_WORD(self, address: FWI_unsigned, register: REGISTER):
        if address.int % 4 != 0:
            raise Exception("Word addresses must be divisible by 4")
        else:
            segments = [register.u[24:31], register.u[16:23],
                        register.u[8:15], register.u[0:7]]
            self.memory_table[int(address.int/4)] = segments

    def LOAD_WORD(self, address: FWI_unsigned, register: REGISTER):
        if address.int % 4 != 0:
            raise Exception("Word addresses must be divisible by 4")
        else:
            row: list[FWI_unsigned] = self.memory_table[int(address.int/4)]
            bin_str = ""
            for item in row:
                bin_str += item.bits

            register.set_automatic(FWI_unsigned.from_binary_str(bin_str))

    def LOAD_HALF_WORD_UNSIGNED(self, address: FWI_unsigned, register: REGISTER):
        offset = address.int % 4
        word_address = address.int//4

        if offset == 3:
            most_sig_byte = self.memory_table[word_address][offset]
            least_sig_byte = self.memory_table[word_address + 1][offset]

        else:
            most_sig_byte = self.memory_table[word_address][offset]
            least_sig_byte = self.memory_table[word_address][offset+1]

        fwi = FWI_unsigned.from_binary_str(
            most_sig_byte.bits + least_sig_byte.bits)
        fwi_32 = FWI_unsigned.new_width(fwi, 32)
        register.set_automatic(fwi_32)


class REGISTER():
    def __init__(self, name: str, number: int):
        self.NAME = name
        self.NUMBER = number
        if self.NAME != "$sp" and self.NAME != "$pc":
            self.s = FWI(0, 32)
            self.u = FWI_unsigned(0, 32)
        else:
            self.s = FWI(0, 16)
            self.u = FWI_unsigned(0, 16)

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


signed_alu_op_callable = Callable[[ALU, FWI, FWI],
                                  Union[bool, FWI]]

unsigned_alu_op_callable = Callable[[ALU, FWI_unsigned, FWI_unsigned],
                                    Union[bool, FWI_unsigned]]
mmu_op_callable = Callable[[MMU, FWI_unsigned, REGISTER], None]


class VLQRISC_System():

    class PROGRAM_CONTROL():
        def __init__(self):
            self.a = None  # input
            self.b = None  # input
            self.c = None

        def set_operands(self, a: Union[FWI, FWI_unsigned], b: Union[FWI, FWI_unsigned]):
            self.a = a  # input
            self.b = b  # input

        def update_pc(self, new_address: FWI_unsigned, program_counter: REGISTER):

            program_counter.set_automatic(new_address)

    def __init__(self):

        self.register_table: list[REGISTER] = []
        for i, name in enumerate(REGISTER_NAMES):

            self.register_table.append(
                REGISTER(name, i))

        self.alu = ALU()
        self.mmu = MMU()
        self.program_control = self.PROGRAM_CONTROL()

    @ property
    def register_table_bits(self) -> list[tuple[str, str]]:
        register_table_bits: list[tuple[str, str]] = []
        for reg in self.register_table:
            register_table_bits.append((reg.NAME, reg.u.bits))
        return register_table_bits

    @ property
    def memory_table_bits(self) -> list[tuple[str, str, str, str]]:
        memory_table_bits: list[tuple[str, str]] = []
        entry: FWI_unsigned
        for i, entry in enumerate(self.mmu.memory_table):
            bits = [hex(4*i)]
            bits.extend([item.bits for item in entry])
            memory_table_bits.append(bits)
        return memory_table_bits

    def execute(self, instruction: Instruction):

        OTER = OpTypeExecutionRegistration
        registrations: list[OTER] = [OTER(OpTypes.GPR_GPR,
                                          VLQRISC_System.__GPR_GPR),
                                     OTER(OpTypes.NUM_GPR,
                                          VLQRISC_System.__NUM_GPR),
                                     OTER(OpTypes.UNCOND_BRANCH,
                                          VLQRISC_System.__UNCOND_BRANCH),
                                     OTER(OpTypes.COMP_BRANCH,
                                          VLQRISC_System.__COMP_BRANCH),
                                     OTER(OpTypes.MEMORY, VLQRISC_System.__MEMORY)]

        # Get micro operations
        opcode = instruction.segments[0]
        for op in Operations.__members__.values():
            if op.value.op_code == opcode.int:
                alu_op_s: Optional[signed_alu_op_callable] = op.value.alu_op_s
                alu_op_u: Optional[unsigned_alu_op_callable] = op.value.alu_op_u
                mmu_op: Optional[mmu_op_callable] = op.value.mmu_op
                break
        else:
            raise IncompatibleOpCode(
                f"Provided opcode cannot be executed: {opcode.int}/0b{opcode.bits} ")

        reg: OTER
        for reg in registrations:
            if reg.type == instruction.type:
                reg.to_execute(self, instruction, alu_op_s, alu_op_u, mmu_op)

    def __GPR_GPR(self, instruction: Instruction, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):
        rd: REGISTER = self.register_table[instruction.segments[1].int]
        rs1: REGISTER = self.register_table[instruction.segments[2].int]
        rs2: REGISTER = self.register_table[instruction.segments[3].int]

        if alu_op_s:
            result = alu_op_s(self.alu, rs1.s, rs2.s)
            if not isinstance(result, bool):
                rd.set_automatic(result)
        elif alu_op_u:
            result = alu_op_u(self.alu, rs1.u, rs2.u)
            if not isinstance(result, bool):
                rd.set_automatic(result)

    def __NUM_GPR(self, instruction: Instruction, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):
        rd: REGISTER = self.register_table[instruction.segments[1].int]
        rs1: REGISTER = self.register_table[instruction.segments[2].int]
        immediate_u: FWI_unsigned = instruction.segments[3]
        if alu_op_s:
            immediate_s = FWI.from_unsigned(immediate_u)
            result = alu_op_s(self.alu, rs1.s, immediate_s)
            if not isinstance(result, bool):
                rd.set_automatic(result)
        elif alu_op_u:
            result = alu_op_u(self.alu, rs1.u, immediate_u)
            if not isinstance(result, bool):
                rd.set_automatic(result)

    def __COMP_BRANCH(self, instruction: Instruction, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):

        rs1 = self.register_table[instruction.segments[1].int]
        rs2 = self.register_table[instruction.segments[2].int]
        jump_address = instruction.segments[3]
        if alu_op_s:
            result = alu_op_s(self.alu, rs1.s, rs2.s)
            if result:
                self.program_control.update_pc(
                    jump_address, self.register_table[hw_definitions.convert_reg_common_name_to_number("$pc")])
        else:
            raise OperationNotImplemented(
                "Comparison branch requires a signed ALU operation")

    def __UNCOND_BRANCH(self, instruction: Instruction, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):
        jump_address = instruction.segments[1]
        self.program_control.update_pc(
            jump_address, self.register_table[hw_definitions.convert_reg_common_name_to_number("$pc")])

    def __MEMORY(self, instruction: Instruction, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):
        address = instruction.segments[-1]
        if instruction.segments[2].int != 0:
            address_register: REGISTER = self.register_table[instruction.segments[2].int]
            address += address_register.u
        data_register = self.register_table[instruction.segments[1].int]
        if mmu_op:
            result = mmu_op(
                self.mmu, address, data_register)


class OpTypeExecutionRegistration():
    def __init__(self, type: OpTypes, to_execute: cpu_operation) -> None:
        self.type = type
        self.to_execute = to_execute


class Instruction():
    def __init__(self, fwi: FWI_unsigned, type: OpTypes):
        self.fwi: FWI_unsigned = fwi
        self.type = type

    @ property
    def segments(self) -> list[FWI_unsigned]:
        if self.type == OpTypes.GPR_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[15:18], self.fwi[0:14]]
        elif self.type == OpTypes.NUM_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], FWI.from_unsigned(self.fwi[0:18])]
        elif self.type == OpTypes.COMP_BRANCH:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[0:15]]
        elif self.type == OpTypes.UNCOND_BRANCH:
            return [self.fwi[27:31], self.fwi[0: 15]]
        elif self.type == OpTypes.MEMORY:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[0:15]]
        else:
            return [self.fwi]


cpu_operation = Callable[[VLQRISC_System, Instruction,
                          Optional[signed_alu_op_callable], Optional[unsigned_alu_op_callable], Optional[mmu_op_callable]], None]


class ReplacementTokens(str, enum.Enum):
    GPR = "GPR"  # General Purpose Register (GPR)
    NUM = "NUM"
    ADDRESS = "ADDR"


class OpTypes(str, enum.Enum):
    GPR_GPR = "register_with_register"
    NUM_GPR = "num_with_register"  # number with GPR
    COMP_BRANCH = "comparison_branch"
    UNCOND_BRANCH = "unconditional_branch"
    MEMORY = "memory"


class Operation():
    def __init__(self, name: str,  syntax_tokens: list[list[str]], type: OpTypes, op_code: int, alu_op_s: Optional[signed_alu_op_callable] = None, alu_op_u: Optional[unsigned_alu_op_callable] = None, mmu_op: Optional[mmu_op_callable] = None):
        self.name = name
        self.syntax_tokens = syntax_tokens
        self.type = type
        self.op_code = op_code
        self.alu_op_s = alu_op_s
        self.alu_op_u = alu_op_u
        self.mmu_op = mmu_op

    @ property
    def op_code_str(self):
        string = bin(self.op_code)
        return string[2:].zfill(5)

    @ property
    def op_code_fwi(self):
        return FWI_unsigned(self.op_code, 5)

    def __str__(self):
        return f"""{self.name}: Opcode = {self.op_code_str} {self.syntax_tokens}"""


class Operations(enum.Enum):

    ADD_REGS = Operation("ADD_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                             "+", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00000, ALU.ADD)

    ADD_REG_TO_NUM = Operation("ADD_REG_TO_NUM",
                               [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "+", ReplacementTokens.NUM],
                                [ReplacementTokens.GPR, "=", ReplacementTokens.NUM, "+", ReplacementTokens.GPR]],
                               OpTypes.NUM_GPR,
                               0b00001, ALU.ADD)

    AND_REGS = Operation("AND_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                           "&", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00010, alu_op_u=ALU.AND)

    AND_REG_W_NUM = Operation("AND_REG_W_NUM",
                              [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM],
                               [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM]],
                              OpTypes.NUM_GPR, 0b00011, alu_op_u=ALU.AND)

    OR_REGS = Operation("OR_REGS",
                        [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR], [
                            ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR]],
                        OpTypes.GPR_GPR,
                        0b00100, alu_op_u=ALU.OR)

    OR_REG_W_NUM = Operation("OR_REG_WITH_NUM",
                             [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM],
                                 [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM]],
                             OpTypes.GPR_GPR,
                             0b00101, alu_op_u=ALU.OR)

    BRANCH_IF_EQUAL = Operation("BRANCH_IF_EQUAL", [
                                ["if", '(', ReplacementTokens.GPR, "==", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00110, ALU.EQ)

    BRANCH_IF_NOT_EQUAL = Operation("BRANCH_IF_NOT_EQUAL", [
        ["if", '(', ReplacementTokens.GPR,  "!=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00111, ALU.NEQ)

    BRANCH_GT_OR_EQUAL = Operation("BRANCH_IF_GREATER_THAN_OR_EQUAL", [[
                                   "if", '(', ReplacementTokens.GPR,  ">=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01000, ALU.GE)

    BRANCH_GT = Operation("BRANCH_IF_GREATER_THAN", [[
        "if", '(', ReplacementTokens.GPR,  ">", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01001, ALU.GT)

    BRANCH_LT_OR_EQUAL = Operation("BRANCH_IF_LESS_THAN_OR_EQUAL", [[
        "if", '(', ReplacementTokens.GPR,  "<=", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01010, ALU.LE)

    BRANCH_LT = Operation("BRANCH_IF_LESS_THAN", [[
        "if", '(', ReplacementTokens.GPR,  "<", ReplacementTokens.GPR, ")", "j", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b01011, ALU.LT)

    JUMP = Operation("JUMP", [
        ["j", ReplacementTokens.ADDRESS]], OpTypes.UNCOND_BRANCH, 0b01100)

    LOAD_WORD = Operation(
        "LOAD_WORD", [["lw", ReplacementTokens.GPR, ",", ReplacementTokens.NUM], ["lw", ReplacementTokens.GPR, ",", ReplacementTokens.GPR]], OpTypes.MEMORY, 0b01101, mmu_op=MMU.LOAD_WORD)

    STORE_WORD = Operation("STORE_WORD", [
                           ["sw", ReplacementTokens.GPR,
                               ",", ReplacementTokens.NUM],
                           ["sw", ReplacementTokens.GPR, ",",
                               ReplacementTokens.GPR, "+", ReplacementTokens.NUM],
                           ["sw", ReplacementTokens.GPR, ",", ReplacementTokens.GPR]], OpTypes.MEMORY, 0b01110, mmu_op=MMU.STORE_WORD)

    LOAD_HALF_WORD_UNSIGNED = Operation(
        "LOAD_HALF_WORD", [["lhu", ReplacementTokens.GPR, ",", ReplacementTokens.NUM],
                           ["lhu", ReplacementTokens.GPR, ",", ReplacementTokens.GPR, "+", ReplacementTokens.NUM], ["lhu", ReplacementTokens.GPR, ",", ReplacementTokens.GPR]],
        OpTypes.MEMORY, 0b01111, mmu_op=MMU.LOAD_HALF_WORD_UNSIGNED)

    LOAD_BYTE_UNSIGNED = Operation(
        "LOAD_HALF_WORD", [["lbu", ReplacementTokens.GPR, ",", ReplacementTokens.NUM],
                           ["lbu", ReplacementTokens.GPR, ",", ReplacementTokens.GPR, "+", ReplacementTokens.NUM], [
                               "lbu", ReplacementTokens.GPR, ",", ReplacementTokens.GPR]],
        OpTypes.MEMORY, 0b10000, mmu_op=MMU.LOAD_WORD)


operators: list[str] = []
for op in Operations:
    tokens = op.value.syntax_tokens
    for list in tokens:
        for token in list:
            if token not in operators and token not in ReplacementTokens:
                operators.append(token)
