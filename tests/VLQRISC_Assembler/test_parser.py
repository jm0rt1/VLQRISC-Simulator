from __future__ import annotations
from typing import Optional
import unittest
from src.VLQRISC_Simulator.hw_definitions import convert_reg_common_name_to_number
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Simulator.system as operations
from src.VLQRISC_Simulator.system import Operations
from dataclasses import dataclass


class TestLineParser(unittest.TestCase):
    def test_passing_input_output_schemes(self):
        for scheme in passing_input_output_schemes:
            line_parser = parser.LineParser(scheme.input)
            line_data = line_parser.parse()

            # tokenized line
            self.assertEqual(line_data.tokenized_line,
                             scheme.expected_tokenized_line)

            # correct form
            self.assertTrue(any(
                form == line_data.form for form in scheme.syntax_tokens))

            # correct type
            self.assertEqual(line_data.type, scheme.expected_type)

            # opcode and opcode str
            self.assertEqual(
                line_data.opcode_int.int, scheme.expected_opcode_int)
            self.assertEqual(line_data.opcode_str,
                             scheme.expected_opcode_str)

            if line_data.Rd_num is not None:
                # Rd
                self.assertEqual(line_data.Rd_num.int, scheme.expected_Rd_num)
                self.assertEqual(line_data.Rd_common_name,
                                 scheme.expected_Rd_common_name)
            else:
                self.assertEqual(line_data.immediate_operand,
                                 scheme.expected_immediate_operand)
                self.assertEqual(line_data.jump_address_str,
                                 scheme.jump_address_str)
            # Rs1
            if line_data.Rs1_num is not None:
                self.assertEqual(line_data.Rs1_num.int,
                                 scheme.expected_Rs1_num)
                self.assertEqual(line_data.Rs1_common_name,
                                 scheme.expected_Rs1_common_name)
            else:
                self.assertEqual(
                    line_data.Rs1_num, scheme.expected_Rs1_num)
                self.assertEqual(line_data.Rs1_common_name,
                                 scheme.expected_Rs1_common_name)

            # Rs2
            if line_data.Rs2_num is not None:
                self.assertEqual(line_data.Rs2_num.int,
                                 scheme.expected_Rs2_num)
                self.assertEqual(line_data.Rs2_common_name,
                                 scheme.expected_Rs2_common_name)
            else:
                self.assertEqual(
                    line_data.Rs1_num, scheme.expected_Rs1_num)
                self.assertEqual(line_data.Rs1_common_name,
                                 scheme.expected_Rs1_common_name)
            self.assertEqual(
                line_data.Rs1_common_name, scheme.expected_Rs1_common_name)
            if line_data.immediate_operand is not None:
                # jump adress and
                self.assertEqual(line_data.immediate_operand.int,
                                 scheme.expected_immediate_operand)
                self.assertEqual(line_data.jump_address_str,
                                 scheme.jump_address_str)
            else:
                self.assertEqual(line_data.immediate_operand,
                                 scheme.expected_immediate_operand)
                self.assertEqual(line_data.jump_address_str,
                                 scheme.jump_address_str)


@dataclass(frozen=True)
class Scheme():
    """a docstring"""
    input: str
    expected_tokenized_line: list[str]
    syntax_tokens: list[list[str]]

    expected_immediate_operand: Optional[int]
    jump_address_str: Optional[str]

    expected_Rd_common_name: Optional[str]
    expected_Rd_num: Optional[int]

    expected_Rs1_common_name: Optional[str]
    expected_Rs1_num: Optional[int]

    expected_Rs2_common_name: Optional[str]
    expected_Rs2_num: Optional[int]

    expected_opcode_int: int
    expected_opcode_str: str

    expected_type: operations.OpTypes


passing_input_output_schemes = [
    #Scheme("J label")

    Scheme("j label", ["j", "label"],
           Operations.JUMP.value.syntax_tokens, None, "label", None, None,
           None, None, None, None,
           Operations.JUMP.value.op_code,
           Operations.JUMP.value.op_code_str,
           Operations.JUMP.value.type),
    Scheme("if($s0<$s1)j label", ["if", "(", "$s0", "<", "$s1", ")", "j", "label"],
           Operations.BRANCH_LT.value.syntax_tokens, None, "label", None, None,
           "$s0", convert_reg_common_name_to_number("$s0"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.BRANCH_LT.value.op_code,
           Operations.BRANCH_LT.value.op_code_str,
           Operations.BRANCH_LT.value.type),
    Scheme("if($s0<=$s1)j label", ["if", "(", "$s0", "<=", "$s1", ")", "j", "label"],
           Operations.BRANCH_LT_OR_EQUAL.value.syntax_tokens, None, "label", None, None,
           "$s0", convert_reg_common_name_to_number("$s0"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.BRANCH_LT_OR_EQUAL.value.op_code,
           Operations.BRANCH_LT_OR_EQUAL.value.op_code_str,
           Operations.BRANCH_LT_OR_EQUAL.value.type),
    Scheme("if($s0>$s1)j label", ["if", "(", "$s0", ">", "$s1", ")", "j", "label"],
           Operations.BRANCH_GT.value.syntax_tokens, None, "label", None, None,
           "$s0", convert_reg_common_name_to_number("$s0"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.BRANCH_GT.value.op_code,
           Operations.BRANCH_GT.value.op_code_str,
           Operations.BRANCH_GT.value.type),
    Scheme("if($s0>=$s1)j label", ["if", "(", "$s0", ">=", "$s1", ")", "j", "label"],
           Operations.BRANCH_GT_OR_EQUAL.value.syntax_tokens, None, "label", None, None,
           "$s0", convert_reg_common_name_to_number("$s0"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.BRANCH_GT_OR_EQUAL.value.op_code,
           Operations.BRANCH_GT_OR_EQUAL.value.op_code_str,
           Operations.BRANCH_GT_OR_EQUAL.value.type),
    Scheme("if($s0!=$s1)j label", ["if", "(", "$s0", "!=", "$s1", ")", "j", "label"],
           Operations.BRANCH_IF_NOT_EQUAL.value.syntax_tokens, None, "label", None, None,
           "$s0", convert_reg_common_name_to_number("$s0"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.BRANCH_IF_NOT_EQUAL.value.op_code,
           Operations.BRANCH_IF_NOT_EQUAL.value.op_code_str,
           Operations.BRANCH_IF_NOT_EQUAL.value.type),
    Scheme("if($s4==$s2)j0x1111111111111111", ["if", "(", "$s4", "==", "$s2", ")", "j", "0x1111111111111111"],
           Operations.BRANCH_IF_EQUAL.value.syntax_tokens,
           None, "0x1111111111111111", None, None,
           "$s4", convert_reg_common_name_to_number(
               "$s4"),
           "$s2", convert_reg_common_name_to_number(
               "$s2"),
           Operations.BRANCH_IF_EQUAL.value.op_code,
           Operations.BRANCH_IF_EQUAL.value.op_code_str,
           Operations.BRANCH_IF_EQUAL.value.type),
    Scheme("$s1=$s2+$s1", ["$s1", "=", "$s2", "+", "$s1"],
           Operations.ADD_REGS.value.syntax_tokens,
           None, None,
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           "$s2", convert_reg_common_name_to_number(
               "$s2"),
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           Operations.ADD_REGS.value.op_code,
           Operations.ADD_REGS.value.op_code_str,
           Operations.ADD_REGS.value.type),
    Scheme("$s1=$s2|$s1", ["$s1", "=", "$s2", "|", "$s1"],
           Operations.OR_REGS.value.syntax_tokens,
           None, None,
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           "$s2", convert_reg_common_name_to_number(
               "$s2"),
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           Operations.OR_REGS.value.op_code,
           Operations.OR_REGS.value.op_code_str,
           Operations.OR_REGS.value.type),
    Scheme("$s1=$s2&$s1", ["$s1", "=", "$s2", "&", "$s1"],
           Operations.AND_REGS.value.syntax_tokens,
           None, None,
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           "$s2", convert_reg_common_name_to_number(
               "$s2"),
           "$s1", convert_reg_common_name_to_number(
               "$s1"),
           Operations.AND_REGS.value.op_code,
           Operations.AND_REGS.value.op_code_str,
           Operations.AND_REGS.value.type)
]
