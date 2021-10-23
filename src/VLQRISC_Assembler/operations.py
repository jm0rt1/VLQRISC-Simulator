from __future__ import annotations
import enum


class ReplacementTokens(str, enum.Enum):
    GPR = "GPR"  # General Purpose Register (GPR)


class OpTypes(str, enum.Enum):
    GPR_GPR = "register_with_register"
    NUM_GPR = "num_with_register"  # number with GPR


class Operation():
    def __init__(self, name: str,  operation_tokens: list[list[str]], type: OpTypes, op_code: int):
        self.name = name
        self.operation_tokens = operation_tokens
        self.type = type
        self.op_code = op_code

    @property
    def op_code_str(self):
        string = bin(self.op_code)
        return string[2:].zfill(5)

    def __str__(self):
        return f"""{self.name}: Opcode = {self.op_code_str} {self.operation_tokens}"""


class Operations(enum.Enum):

    ADD_REGS = Operation("ADD_REGS",
                         [["GPR", "=", "GPR", "+", "GPR"]],
                         OpTypes.GPR_GPR,
                         0b00000)

    ADD_REG_TO_NUM = Operation("ADD_REG_TO_NUM", [["GPR", "=", "GPR", "+", "NUM"],
                               ["GPR", "=", "NUM", "+", "GPR"]],
                               OpTypes.NUM_GPR,
                               0b00001)

    AND_REGS = Operation("AND_REGS", [["GPR", "=", "GPR", "&", "GPR"]],
                         OpTypes.GPR_GPR,
                         0b00010)

    AND_REG_W_NUM = Operation("AND_REG_W_NUM",
                              [["GPR", "=", "GPR", "&", "NUM"],
                               ["GPR", "=", "GPR", "&", "NUM"]],
                              OpTypes.NUM_GPR, 0b00011)

    OR_REGS = Operation("OR_REGS",
                        [["GPR", "=", "GPR", "|", "GPR"], [
                            "GPR", "=", "GPR", "|", "GPR"]],
                        OpTypes.GPR_GPR,
                        0b00100)

    OR_REG_WITH_NUM = Operation("OR_REG_WITH_NUM",
                                [["GPR", "=", "GPR", "|", "NUM"],
                                 ["GPR", "=", "GPR", "|", "NUM"]], OpTypes.GPR_GPR, 0b00100)
