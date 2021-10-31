from src.VLQRISC_Simulator.hw_definitions import MEMORY_SIZE, REGISTER_NAMES
from src.Shared.fwi import FWI, FWI_unsigned


class VLQRISC_System():
    class REGISTER():
        def __init__(self, name: str):
            self.name =
            self.s = FWI(0, 8)
            self.u = FWI_unsigned(0, 8)

    class ALU():
        def __init__(self):
            self.a = None  # input
            self.b = None  # input
            self.c = None

        def set_operands(self, a: FWI, b: FWI):
            self.a = a  # input
            self.b = b  # input

        def ADD(self, a: FWI, b: FWI) -> FWI:
            self.set_operands(a, b)
            return a+b

        def ADD_UNSIGNED(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI:
            self.set_operands(a, b)
            return a+b

        @staticmethod
        def AND(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI:
            self.set_operands(a, b)
            return a+b

    def __init__(self):
        self.memory_table = []
        self.memory_table = [FWI_unsigned(0, 8)]*MEMORY_SIZE

        self.register_table = []
        for name in REGISTER_NAMES:
            self.register_table.append(
                (name, FWI_unsigned(0, 32)))

        self.alu = self.ALU()

    @ property
    def register_table_bits(self):
        register_table = []
        for i, reg in enumerate(self.register_table):
            register_table.append((reg[0], reg[1].bits))
        return register_table

    def register_table(self)
