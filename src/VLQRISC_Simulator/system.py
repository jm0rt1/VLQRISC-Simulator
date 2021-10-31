from __future__ import annotations
from typing import Union
from src.VLQRISC_Simulator.hw_definitions import MEMORY_SIZE, REGISTER_NAMES
from src.Shared.fwi import FWI, FWI_unsigned


class VLQRISC_System():
    class REGISTER():
        def __init__(self, name: str, number: int):
            self.name = name
            self.NUMBER = REGISTER_NAMES[number]
            self.s = FWI(0, 32)
            self.u = FWI_unsigned(0, 32)

        def set_unsigned(self, u_value: FWI_unsigned):
            self.s = FWI.from_unsigned(u_value)
            self.u = u_value

        def set_signed(self, s_value: FWI):
            self.s = s_value
            self.u = FWI_unsigned.from_signed(s_value)

    class ALU():
        def __init__(self):
            self.a = None  # input
            self.b = None  # input
            self.c = None

        def set_operands(self, a: Union[FWI, FWI_unsigned], b: Union[FWI, FWI_unsigned]):
            self.a = a  # input
            self.b = b  # input

        def ADD(self, a: FWI, b: FWI) -> FWI:
            self.set_operands(a, b)
            return a+b

        def ADD_UNSIGNED(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            return a+b

        def AND(self, a: FWI_unsigned, b: FWI_unsigned) -> FWI_unsigned:
            self.set_operands(a, b)
            return a+b

    def __init__(self):
        self.memory_table = []
        self.memory_table = [FWI_unsigned(0, 8)]*MEMORY_SIZE

        self.register_table: list[VLQRISC_System.REGISTER] = []
        for i, name in enumerate(REGISTER_NAMES):
            self.register_table.append(
                self.REGISTER(name, i))

        self.alu = self.ALU()

    @ property
    def register_table_bits(self) -> list[tuple[str, str]]:
        register_table_bits: list[tuple[str, str]] = []
        for reg in self.register_table:
            register_table_bits.append((reg.name, reg.u.bits))
        return register_table_bits
