from __future__ import annotations
from typing import Optional, Tuple

import src.VLQRISC_Assembler.operations as operations
from src.VLQRISC_Assembler.hw_definitions import RegisterNames
import copy


class InvalidOperation(Exception):
    pass


class LineParser():
    def __init__(self, line: str):
        self.line = copy.copy(line)

    def parse(self):
        self.tokenized_line = self.tokenize_line(self.line)
        self.form = self.generate_standard_form()

        self.opcode_int, self.opcode_str, self.type = self.get_op_info()

    def __build_machine_code(self):
        if self.type == operations.OpTypes.GPR_GPR:
            self.__get_regs_gpr_gpr()

    def __get_regs_gpr_gpr(self):
        if "$" not in self.tokenized_line[0] and "$" not in self.tokenized_line[2] and "$" not in self.tokenized_line[4]:
            raise InvalidOperation("expected $Rd = $Rs1 [operation] $Rs2")

    def get_op_info(self) -> Tuple[int, str, operations.OpTypes]:
        for op in operations.Operations.__members__.values():
            tokens = op.value.syntax_tokens
            if any(form == self.form for form in tokens):
                return op.value.op_code, op.value.op_code_str, op.value.type

        raise InvalidOperation(f"invalid line of input {self.line}")

    def generate_standard_form(self):
        standard_line = copy.copy(self.line)
        for reg in RegisterNames:
            standard_line = standard_line.replace(
                reg, f"{operations.ReplacementTokens.GPR} ")
        standard_line_tokens = self.tokenize_line(standard_line)
        return standard_line_tokens

    def tokenize_line(self, line: str) -> list[str]:
        if "=" in line and "==" not in line:
            line = line.replace(
                "=", " = ")
        if "+" in line:
            line = line.replace(
                "+", " + ")
        if "|" in line:
            line = line.replace("|", " | ")
        if "&" in line:
            line = line.replace("&", " & ")
        line.strip()
        tokens = line.split()
        return tokens

    def _(self):
        if "==" in self.line:
            self.line_split = self.line.split("==")
        self.line_split = self.line.split()

    def determine_opcode(self):

        if "=" in self.line and "==" not in self.line:
            if "+" in self.line:
                if self.line.count("$") == 2:
                    return operations.Operations.ADD_REGS.value.op_code
                else:
                    return operations.Operations.ADD_REG_TO_NUM.value.op_code
            elif "-" in self.line:
                pass
