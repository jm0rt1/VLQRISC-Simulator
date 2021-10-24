import unittest
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.operations as operations


class TestLineParser(unittest.TestCase):
    def test_ADD_REGS(self):

        line_parser = parser.LineParser("$s1=   $s2+    $s1")
        line_data = line_parser.parse()

        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.ADD_REGS.value.op_code_str)

        line_parser = parser.LineParser("$s4=$s2+$s1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s4", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.ADD_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 6)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 9)

    def test_OR_REGS(self):

        line_parser = parser.LineParser("$s1=$s2|$s1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "|", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.OR_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.OR_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.OR_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 6)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 6)

    def test_AND_REGS(self):
        line_parser = parser.LineParser("$t0=$s2&$t1")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$t0", "=", "$s2", "&", "$t1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.AND_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_data.opcode_int
        found_opcode_str = line_data.opcode_str

        self.assertEquals(
            found_opcode_int, operations.Operations.AND_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.AND_REGS.value.op_code_str)

        self.assertEquals(line_data.Rs2_num, 2)
        self.assertEquals(line_data.Rs1_num, 7)
        self.assertEquals(line_data.Rd_num, 1)

    def test_ADD_REG_TO_NUM(self):
        line_parser = parser.LineParser("$t0=$s2+1000")
        line_data = line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$t0", "=", "$s2", "+", "1000"]
        self.assertEquals(tokenized_line, expected)
        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.ADD_REG_TO_NUM.value.syntax_tokens))

        self.assertEquals(line_data.immediate_operand, 1000)
        self.assertEquals(line_data.Rd_common_name, "$t0")
        self.assertEquals(line_data.Rs1_common_name, "$s2")

        self.assertEquals(line_data.Rd_num, 1)
        self.assertEquals(line_data.Rs1_num, 7)

        self.assertEquals(line_data.opcode_int,
                          operations.Operations.ADD_REG_TO_NUM.value.op_code)
        self.assertEquals(line_data.opcode_str,
                          operations.Operations.ADD_REG_TO_NUM.value.op_code_str)

        line_parser = parser.LineParser("$t0=1000+$s2")
        line_data = line_parser.parse()

        self.assertTrue(
            any(form == line_data.form for form in operations.Operations.ADD_REG_TO_NUM.value.syntax_tokens))

        self.assertEquals(line_data.opcode_int,
                          operations.Operations.ADD_REG_TO_NUM.value.op_code)
        self.assertEquals(line_data.opcode_str,
                          operations.Operations.ADD_REG_TO_NUM.value.op_code_str)

        self.assertEquals(line_data.immediate_operand, 1000)
        self.assertEquals(line_data.Rd_common_name, "$t0")
        self.assertEquals(line_data.Rs1_common_name, "$s2")

        self.assertEquals(line_data.Rd_num, 1)
        self.assertEquals(line_data.Rs1_num, 7)
