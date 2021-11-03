
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Simulator.system as operations

from src.Shared.fwi import FWI, FWI_unsigned
from src.VLQRISC_Simulator.system import Instruction


class MissingOpcode(Exception):
    pass


class OpTypeNotRecognized(Exception):
    pass


class InstructionGenerator():
    """
    Instruction Generator -- Generates an instruction that can then be interpreted by the VLQRISC_System upon execution
    """

    def __init__(self, line_data: parser.LineData) -> None:
        self.line_data = line_data

        self.Rd = None
        self.Rs1 = None
        self.Rs2 = None
        self.immediate_operand = None
        self.address_str = None

    def generate(self) -> Instruction:
        self.__generate_binary_strings()

        if self.line_data.type == operations.OpTypes.GPR_GPR:
            return self.__generate_GPR_GPR_inst()
        elif self.line_data.type == operations.OpTypes.NUM_GPR:
            return self.__generate_NUM_GPR_inst()
        elif self.line_data.type == operations.OpTypes.COMP_BRANCH:
            return self.__generate_COMP_BRANCH_inst()
        elif self.line_data.type == operations.OpTypes.UNCOND_BRANCH:
            return self.__generate_UNCOND_BRANCH()
        elif self.line_data.type == operations.OpTypes.MEMORY:
            return self.__generate_MEMORY()
        else:
            raise OpTypeNotRecognized("Instruction type not implemented")

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
        if self.line_data.immediate_operand:
            self.immediate_operand = self.line_data.immediate_operand.bits
        if self.line_data.address_str:
            self.address_str = self.line_data.address_str

    def __generate_GPR_GPR_inst(self):
        return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{self.Rd}{self.Rs1}{self.Rs2}" + "0"*15), operations.OpTypes.GPR_GPR)

    def __generate_NUM_GPR_inst(self):

        return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{self.Rd}{self.Rs1}{self.immediate_operand}"), operations.OpTypes.NUM_GPR)

    def __generate_COMP_BRANCH_inst(self):
        jump_address = self.get_address()
        return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{self.Rs1}{self.Rs2}000{jump_address.bits}"), operations.OpTypes.COMP_BRANCH)

    def __generate_UNCOND_BRANCH(self):
        jump_address = self.get_address()
        zeros = "0"*11
        return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{zeros}{jump_address.bits}"), operations.OpTypes.UNCOND_BRANCH)

    def __generate_MEMORY(self):
        if self.address_str:
            address = self.get_address()
        else:
            address = FWI_unsigned(0, 16)
        if self.Rs1:
            zeros = "0"*3
            return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{self.Rd}{self.Rs1}{zeros}{address.bits}"), operations.OpTypes.MEMORY)

        zeros = "0"*7
        return Instruction(FWI_unsigned.from_binary_str(f"{self.opcode}{self.Rd}{zeros}{address.bits}"), operations.OpTypes.MEMORY)

    def get_address(self):
        jump_address: FWI_unsigned
        if self.address_str[0:2] == "0b":
            if self.address_str:
                jump_address = FWI_unsigned.address_from_binary_str(
                    self.address_str[2:])
        elif self.address_str.startswith("0x"):
            pass
            raise NotImplementedError("Hexadecimal input is not implemented")
            # assume
        else:
            # decimal or label
            if self.address_str.isnumeric():
                jump_address = FWI_unsigned(int(self.address_str), 16)
            else:
                raise NotImplementedError("Labels input is not implemented")

        return jump_address
