from __future__ import annotations
from typing import Optional
import unittest
from src.VLQRISC_Assembler.hw_definitions import convert_reg_common_name_to_number
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.operations as operations
from src.VLQRISC_Assembler.operations import Operations
from dataclasses import dataclass


@dataclass(frozen=True)
class Scheme():
    """a docstring"""
    input: str
    expected_tokenized_line: list[str]
    syntax_tokens: list[list[str]]

    expected_immediate_operand: Optional[int]

    expected_Rd_common_name: Optional[str]
    expected_Rd_num: Optional[int]

    expected_Rs1_common_name: Optional[str]
    expected_Rs1_num: Optional[int]

    expected_Rs2_common_name: Optional[str]
    expected_Rs2_num: Optional[int]

    expected_opcode_int: int
    expected_opcode_str: str

    expected_type: operations.OpTypes


input_output_schemes = [
    Scheme("if($s4==$s2)", ["if", "(", "$s4", "==", "$s2", ")", "0x2"],
           Operations.BRANCH_IF_EQUAL.value.syntax_tokens,
           None, None, None,
           "$s4", convert_reg_common_name_to_number("$s4"),
           "$s2", convert_reg_common_name_to_number("$s2"),
           Operations.BRANCH_IF_EQUAL.value.op_code,
           Operations.BRANCH_IF_EQUAL.value.op_code_str,
           Operations.BRANCH_IF_EQUAL.value.type),
    Scheme("$s1=$s2+$s1", ["$s1", "=", "$s2", "+", "$s1"],
           Operations.ADD_REGS.value.syntax_tokens,
           None,
           "$s1", convert_reg_common_name_to_number("$s1"),
           "$s2", convert_reg_common_name_to_number("$s2"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.ADD_REGS.value.op_code,
           Operations.ADD_REGS.value.op_code_str,
           Operations.ADD_REGS.value.type),
    Scheme("$s1=$s2|$s1",
           ["$s1", "=", "$s2", "|", "$s1"],
           Operations.OR_REGS.value.syntax_tokens,
           None,
           "$s1", convert_reg_common_name_to_number("$s1"),
           "$s2", convert_reg_common_name_to_number("$s2"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.OR_REGS.value.op_code,
           Operations.OR_REGS.value.op_code_str,
           Operations.OR_REGS.value.type),
    Scheme("$s1=$s2&$s1",
           ["$s1", "=", "$s2", "&", "$s1"],
           Operations.AND_REGS.value.syntax_tokens,
           None,
           "$s1", convert_reg_common_name_to_number("$s1"),
           "$s2", convert_reg_common_name_to_number("$s2"),
           "$s1", convert_reg_common_name_to_number("$s1"),
           Operations.AND_REGS.value.op_code,
           Operations.AND_REGS.value.op_code_str,
           Operations.AND_REGS.value.type)


]


class TestLineParser(unittest.TestCase):
    def test_loop(self):
        for scheme in input_output_schemes:
            line_parser = parser.LineParser(scheme.input)
            line_data = line_parser.parse()

            # tokenized line
            self.assertEquals(line_data.tokenized_line,
                              scheme.expected_tokenized_line)

            # correct form
            self.assertTrue(any(
                form == line_data.form for form in scheme.syntax_tokens))

            # correct type
            self.assertEquals(line_data.type, scheme.expected_type)

            # opcode and opcode str
            self.assertEquals(
                line_data.opcode_int, scheme.expected_opcode_int)
            self.assertEquals(line_data.opcode_str,
                              scheme.expected_opcode_str)

            # Rd
            self.assertEquals(line_data.Rd_num, scheme.expected_Rd_num)
            self.assertEquals(line_data.Rd_common_name,
                              scheme.expected_Rd_common_name)

            # Rs1
            self.assertEquals(line_data.Rs1_num, scheme.expected_Rs1_num)
            self.assertEquals(line_data.Rs1_common_name,
                              scheme.expected_Rs1_common_name)

            # Rs2
            self.assertEquals(line_data.Rs2_num,
                              scheme.expected_Rs2_num)
            self.assertEquals(line_data.Rs2_common_name,
                              scheme.expected_Rs2_common_name)

            self.assertEquals(
                line_data.Rs1_common_name, scheme.expected_Rs1_common_name)

    def test_ADD_REGS(self):

        line_parser = parser.LineParser("$s1        =$s2+$s1")
        line_data: parser.LineData = line_parser.parse()

        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["$s1", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          Operations.ADD_REGS.value.op_code_str)
        #############
        line_parser = parser.LineParser("$s4=$s2+$s1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["$s4", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          Operations.ADD_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 6)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 9)

    def test_OR_REGS(self):

        line_parser = parser.LineParser("$s1=$s2|$s1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["$s1", "=", "$s2", "|", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in Operations.OR_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, Operations.OR_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          Operations.OR_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 6)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 6)

    def test_AND_REGS(self):
        line_parser = parser.LineParser("$t0=$s2&$t1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["$t0", "=", "$s2", "&", "$t1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in Operations.AND_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str

        self.assertEquals(
            found_opcode_int, Operations.AND_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          Operations.AND_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 2)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 1)

    def test_ADD_REG_TO_NUM(self):
        line_parser = parser.LineParser("$t0=$s2+1000")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["$t0", "=", "$s2", "+", "1000"]
        self.assertEquals(tokenized_line, expected)
        self.assertTrue(
            any(form == line_data.form for form in Operations.ADD_REG_TO_NUM.value.syntax_tokens))

        self.assertEquals(line_data.immediate_operand, 1000)
        self.assertEquals(line_data.Rd_common_name, "$t0")
        self.assertEquals(line_data.Rs1_common_name, "$s2")

        self.assertEquals(line_data.Rd_num, 1)
        self.assertEquals(line_data.Rs1_num, 7)

        self.assertEquals(line_data.opcode_int,
                          Operations.ADD_REG_TO_NUM.value.op_code)
        self.assertEquals(line_data.opcode_str,
                          Operations.ADD_REG_TO_NUM.value.op_code_str)

        line_parser = parser.LineParser("$t0=1000+$s2")
        line_data = line_parser.parse()

        self.assertTrue(
            any(form == line_data.form for form in Operations.ADD_REG_TO_NUM.value.syntax_tokens))

        self.assertEquals(line_data.opcode_int,
                          Operations.ADD_REG_TO_NUM.value.op_code)
        self.assertEquals(line_data.opcode_str,
                          Operations.ADD_REG_TO_NUM.value.op_code_str)

        self.assertEquals(line_data.immediate_operand, 1000)
        self.assertEquals(line_data.Rd_common_name, "$t0")
        self.assertEquals(line_data.Rs1_common_name, "$s2")

        self.assertEquals(line_data.Rd_num, 1)
        self.assertEquals(line_data.Rs1_num, 7)

    def _BRANCH_IF_EQUAL(self):
        line_parser = parser.LineParser("if($s4==$s2)")
        line_data = line_parser.parse()

        # test tokenization
        tokenized_line = line_data.tokenized_line
        expected = ["if", "(", "$s4", "==", "$s2", ")"]
        self.assertEquals(tokenized_line, expected)
        self.assertTrue(
            any(form == line_data.form for form in Operations.ADD_REG_TO_NUM.value.syntax_tokens))

        self.assertEquals(line_data.immediate_operand, 1000)
        self.assertEquals(line_data.Rd_common_name, "$t0")
        self.assertEquals(line_data.Rs1_common_name, "$s2")

        self.assertEquals(line_data.Rd_num, 1)
        self.assertEquals(line_data.Rs1_num, 7)

        self.assertEquals(line_data.opcode_int,
                          Operations.ADD_REG_TO_NUM.value.op_code)
        self.assertEquals(line_data.opcode_str,
                          Operations.ADD_REG_TO_NUM.value.op_code_str)
