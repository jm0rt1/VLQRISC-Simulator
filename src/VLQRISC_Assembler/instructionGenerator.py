
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.operations as operations


class MissingOpcode(Exception):
    pass


class InstructionGenerator():
    def __init__(self, line_data: parser.LineData) -> None:
        self.line_data = line_data

    def generate(self):
        self.__generate_binary_strings()
        if self.line_data.type == operations.OpTypes.GPR_GPR:
            return self.__generate_GPR_GPR_inst()

    def __generate_binary_strings(self):
        if self.line_data.opcode_str:
            self.opcode = self.line_data.opcode_str
        else:
            raise MissingOpcode("No opcode was parsed")

        if self.line_data.Rd_num:
            self.Rd = self.line_data.Rd_num.bits
        if self.line_data.Rs1_num:
            self.Rs1 = self.line_data.Rs1_num.bits
        if self.line_data.Rs2_num:
            self.Rs2 = self.line_data.Rs2_num.bits

    def __generate_GPR_GPR_inst(self):
        return f"{self.opcode}{self.Rd}{self.Rs1}{self.Rs2}" + "0"*13
