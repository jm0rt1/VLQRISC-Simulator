from __future__ import annotations
import enum


class ReplacementTokens(str, enum.Enum):
    GPR = "GPR"  # General Purpose Register (GPR)
    NUM = "NUM"
    ADDRESS = "ADDR"


class OpTypes(str, enum.Enum):
    GPR_GPR = "register_with_register"
    NUM_GPR = "num_with_register"  # number with GPR
    COMP_BRANCH = "comparison_branch"


class Operation():
    def __init__(self, name: str,  syntax_tokens: list[list[str]], type: OpTypes, op_code: int):
        self.name = name
        self.syntax_tokens = syntax_tokens
        self.type = type
        self.op_code = op_code

    @property
    def op_code_str(self):
        string = bin(self.op_code)
        return string[2:].zfill(5)

    def __str__(self):
        return f"""{self.name}: Opcode = {self.op_code_str} {self.syntax_tokens}"""


class Operations(enum.Enum):

    ADD_REGS = Operation("ADD_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                             "+", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00000)

    ADD_REG_TO_NUM = Operation("ADD_REG_TO_NUM",
                               [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "+", ReplacementTokens.NUM],
                                [ReplacementTokens.GPR, "=", ReplacementTokens.NUM, "+", ReplacementTokens.GPR]],
                               OpTypes.NUM_GPR,
                               0b00001)

    AND_REGS = Operation("AND_REGS",
                         [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR,
                             "&", ReplacementTokens.GPR]],
                         OpTypes.GPR_GPR,
                         0b00010)

    AND_REG_W_NUM = Operation("AND_REG_W_NUM",
                              [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM],
                               [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "&", ReplacementTokens.NUM]],
                              OpTypes.NUM_GPR, 0b00011)

    OR_REGS = Operation("OR_REGS",
                        [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR], [
                            ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.GPR]],
                        OpTypes.GPR_GPR,
                        0b00100)

    OR_REG_WITH_NUM = Operation("OR_REG_WITH_NUM",
                                [[ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM],
                                 [ReplacementTokens.GPR, "=", ReplacementTokens.GPR, "|", ReplacementTokens.NUM]],
                                OpTypes.GPR_GPR,
                                0b00101)

    BRANCH_IF_EQUAL = Operation("BRANCH_IF_EQUAL", [
                                ["if", '(', ReplacementTokens.GPR, "==", ReplacementTokens.GPR, ")", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00110)

    BRANCH_IF_NOT_EQUAL = Operation("BRANCH_IF_NOT_EQUAL", [
        ["if", '(', ReplacementTokens.GPR,  "!=", ReplacementTokens.GPR, ")", ReplacementTokens.ADDRESS]], OpTypes.COMP_BRANCH, 0b00111)

    JUMP = Operation("JUMP", [
        ["J", "ADDR"]], OpTypes.COMP_BRANCH, 0b01000)
