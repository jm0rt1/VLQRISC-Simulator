import unittest
import src.VLQRISC_Assembler.operations as operations


class TestOperations(unittest.TestCase):
    def test_opcode_print(self):

        add_reg_str = str(operations.Operations.ADD_REGS.value)
        if "00000" not in add_reg_str:
            raise Exception(f"Not 5 bits: \n\n{add_reg_str}\n")

    def test_unique_opcodes(self):
        op: operations.Operation

        opcodes_used: list[int] = []

        for op in operations.Operations.__members__.values():
            opcodes_used.append(op.value.op_code)

        if len(opcodes_used) > len(set(opcodes_used)):
            raise Exception("Non-unique set")
