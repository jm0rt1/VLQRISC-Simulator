from __future__ import annotations
from typing import Optional, Tuple
from src.Shared.fwi import FWI_unsigned, FWIOverFlow
from src.VLQRISC_Simulator import hw_definitions

import src.VLQRISC_Simulator.system as operations
from src.VLQRISC_Simulator.hw_definitions import REGISTER_NAMES
import copy


class InvalidOperationInput(Exception):
    pass


class WrongOperationType(Exception):
    pass


class NoTypeSpecified(Exception):

    pass


class LineParser():
    """
    Used to parse a single Line of VLQRISC Assembly

    """

    def __init__(self, line: str):
        self.line = copy.copy(line)

    def parse(self):
        """
        Returns a LineData type that can be used to generate an instruction for the cpu
        """
        self.line_data: LineData = LineData(self.__tokenize_line(self.line))

        self.line_data.form = self.__generate_standard_form()

        self.line_data.opcode_int, self.line_data.opcode_str, self.line_data.type = self.__get_op_info()

        self.__parse_operands()

        return self.line_data

    def __parse_operands(self):
        def get_operands_num_gpr():
            self.raise_on_wrong_op_type(operations.OpTypes.NUM_GPR)

            if "$" not in self.line_data.tokenized_line[0] and ("$" not in self.line_data.tokenized_line[2] != "$" not in self.line_data.tokenized_line[4]):
                raise InvalidOperationInput(
                    f"{operations.OpTypes.NUM_GPR} operation requires the following $Rd = NUM [operation] $Rs1 or $Rd = Rs1 [operation] NUM")
            else:
                self.line_data.Rd_common_name = self.line_data.tokenized_line[0]
                self.line_data.immediate_operand = None
                self.line_data.Rs1_common_name = None
            try:
                self.line_data.immediate_operand = FWI_unsigned(int(
                    self.line_data.tokenized_line[2]), 19)
                self.line_data.Rs1_common_name = self.line_data.tokenized_line[4]

            except:
                try:
                    self.line_data.immediate_operand = FWI_unsigned(int(
                        self.line_data.tokenized_line[4]), 19)
                    self.line_data.Rs1_common_name = self.line_data.tokenized_line[2]
                except FWIOverFlow:
                    raise
                except:
                    if self.line_data.immediate_operand is None or self.line_data.Rs1_common_name is None:
                        raise InvalidOperationInput(
                            f"{operations.OpTypes.NUM_GPR} requires one of the two operands to be a number, the other a register")

            self.line_data.Rs1_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rs1_common_name), 4)
            self.line_data.Rd_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rd_common_name), 4)

        def get_operands_gpr_gpr():
            self.raise_on_wrong_op_type(operations.OpTypes.GPR_GPR)

            # type:ignore
            if "$" not in self.line_data.tokenized_line[0] and "$" not in self.line_data.tokenized_line[2] and "$" not in self.line_data.tokenized_line[4]:
                raise InvalidOperationInput(
                    f"{operations.OpTypes.GPR_GPR} operation requires the following $Rd = $Rs1 [operation] $Rs2")

            self.line_data.Rd_common_name = self.line_data.tokenized_line[0]
            self.line_data.Rs1_common_name = self.line_data.tokenized_line[2]
            self.line_data.Rs2_common_name = self.line_data.tokenized_line[4]

            self.line_data.Rd_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rd_common_name), 4)
            self.line_data.Rs1_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rs1_common_name), 4)
            self.line_data.Rs2_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rs2_common_name), 4)

        def get_operands_comp_branch():
            self.raise_on_wrong_op_type(operations.OpTypes.COMP_BRANCH)
            # type:ignore
            if "$" not in self.line_data.tokenized_line[2] and "$" not in self.line_data.tokenized_line[4]:
                raise InvalidOperationInput(
                    f"{operations.OpTypes.COMP_BRANCH} operation requires the following format if(Rs1 [logical operator] Rs2)")
            self.line_data.Rs1_common_name = self.line_data.tokenized_line[2]
            self.line_data.Rs2_common_name = self.line_data.tokenized_line[4]

            self.line_data.Rs1_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rs1_common_name), 4)
            self.line_data.Rs2_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                self.line_data.Rs2_common_name), 4)
            self.line_data.address_str = self.line_data.tokenized_line[-1]

        def get_operands_uncond_branch():
            self.raise_on_wrong_op_type(operations.OpTypes.UNCOND_BRANCH)
            self.line_data.address_str = self.line_data.tokenized_line[-1]

        def get_operands_memory():
            self.raise_on_wrong_op_type(operations.OpTypes.MEMORY)
            if self.line_data.form:
                # address is an immediate
                if self.line_data.form[3] == operations.ReplacementTokens.NUM:
                    self.line_data.address_str = self.line_data.tokenized_line[3]

                # address is a register
                if self.line_data.form[2] == operations.ReplacementTokens.GPR:
                    self.line_data.Rs1_common_name = self.line_data.tokenized_line[2]
                    self.line_data.Rs1_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                        self.line_data.Rs1_common_name), 4)
                # get the offset if there is one
                if len(self.line_data.form) == 6 and self.line_data.form[5] == operations.ReplacementTokens.NUM:
                    self.line_data.address_str = self.line_data.tokenized_line[5]

                self.line_data.Rd_common_name = self.line_data.tokenized_line[1]
                self.line_data.Rd_num = FWI_unsigned(hw_definitions.convert_reg_common_name_to_number(
                    self.line_data.Rd_common_name), 4)

        if self.line_data.type == operations.OpTypes.GPR_GPR:
            get_operands_gpr_gpr()
        elif self.line_data.type == operations.OpTypes.NUM_GPR:
            get_operands_num_gpr()
        elif self.line_data.type == operations.OpTypes.COMP_BRANCH:
            get_operands_comp_branch()
        elif self.line_data.type == operations.OpTypes.UNCOND_BRANCH:
            get_operands_uncond_branch()
        elif self.line_data.type == operations.OpTypes.MEMORY:
            get_operands_memory()
        else:
            raise NoTypeSpecified("There was no operation type specified")

    def raise_on_wrong_op_type(self, op_type: operations.OpTypes):
        if self.line_data.type is not op_type:
            raise WrongOperationType(
                f"This must be called on a {op_type}")

    def __get_op_info(self) -> Tuple[FWI_unsigned, str, operations.OpTypes]:
        for op in operations.Operations.__members__.values():
            tokens = op.value.syntax_tokens
            if any(form == self.line_data.form for form in tokens):
                return FWI_unsigned(op.value.op_code, 5), op.value.op_code_str, op.value.type

        raise InvalidOperationInput(f"invalid line of input {self.line}")

    def __generate_standard_form(self):

        standard_line = copy.copy(self.line)

        for reg in REGISTER_NAMES:
            standard_line = standard_line.replace(
                reg, f"{operations.ReplacementTokens.GPR} ")

        standard_line_tokens: list[str] = self.__tokenize_line(standard_line)

        if "j" in standard_line_tokens:
            standard_line_tokens[standard_line_tokens.index(
                "j")+1] = operations.ReplacementTokens.ADDRESS

        for i, token in enumerate(standard_line_tokens):
            try:
                float(token)
                standard_line_tokens[i] = operations.ReplacementTokens.NUM.value
            except:
                continue
        return standard_line_tokens

    def __tokenize_line(self, line: str) -> list[str]:
        operators = operations.operators
        for operator in operators:
            if operator == "=" and ("==" in line or "!=" in line or "<=" in line or ">=" in line):
                continue
            elif (operator == "<" and "<=" in line) or (operator == ">" and ">=" in line):
                continue

            line = line.replace(operator, f" {operator} ")

        line.strip()
        tokens: list[str] = line.split()  # type: ignore

        return tokens


class LineData():
    def __init__(self, tokenized_line: list[str]):
        self.opcode_int: FWI_unsigned
        self.opcode_str: Optional[str] = None

        self.tokenized_line: list[str] = tokenized_line

        self.type: Optional[operations.OpTypes] = None
        self.form: Optional[list[str]] = None

        self.Rd_common_name: Optional[str] = None
        self.Rs1_common_name: Optional[str] = None
        self.Rs2_common_name: Optional[str] = None

        self.immediate_operand: Optional[FWI_unsigned] = None

        self.Rd_num: Optional[FWI_unsigned] = None
        self.Rs1_num: Optional[FWI_unsigned] = None
        self.Rs2_num: Optional[FWI_unsigned] = None
        self.address_str: Optional[str] = None
