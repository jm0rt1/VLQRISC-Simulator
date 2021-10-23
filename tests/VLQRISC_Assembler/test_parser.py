import unittest
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.operations as operations


class TestLineParser(unittest.TestCase):
    def test_ADD_REGS(self):

        line_parser = parser.LineParser("$s1=   $s2+    $s1")
        line_parser.parse()

        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_parser.form for form in operations.Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_parser.opcode_int
        found_opcode_str = line_parser.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.ADD_REGS.value.op_code_str)

        line_parser = parser.LineParser("$s1=$s2+$s1")
        line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "+", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_parser.form for form in operations.Operations.ADD_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_parser.opcode_int
        found_opcode_str = line_parser.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.ADD_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.ADD_REGS.value.op_code_str)

    def test_OR_REGS(self):

        line_parser = parser.LineParser("$s1=$s2|$s1")
        line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "|", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_parser.form for form in operations.Operations.OR_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_parser.opcode_int
        found_opcode_str = line_parser.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.OR_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.OR_REGS.value.op_code_str)

    def test_AND_REGS(self):
        line_parser = parser.LineParser("$s1=$s2&$s1")
        line_parser.parse()
        # test tokenization
        tokenized_line = line_parser.tokenized_line
        expected = ["$s1", "=", "$s2", "&", "$s1"]
        self.assertEquals(tokenized_line, expected)

        # test standard form
        self.assertTrue(
            any(form == line_parser.form for form in operations.Operations.AND_REGS.value.syntax_tokens))

        # test opcode obtained
        found_opcode_int = line_parser.opcode_int
        found_opcode_str = line_parser.opcode_str
        self.assertEquals(
            found_opcode_int, operations.Operations.AND_REGS.value.op_code)
        self.assertEquals(found_opcode_str,
                          operations.Operations.AND_REGS.value.op_code_str)
