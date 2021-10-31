
from __future__ import annotations
from src.Shared.fwi import FWI_unsigned
from src.VLQRISC_Assembler.operations import OpTypes


class Instruction():
    def __init__(self, fwi: FWI_unsigned, type: OpTypes):
        self.fwi: FWI_unsigned = fwi
        self.type = type

    @property
    def segments(self) -> list[FWI_unsigned]:
        if self.type == OpTypes.GPR_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[15:18], self.fwi[0:14]]
        elif self.type == OpTypes.NUM_GPR:
            return [self.fwi[27:31], self.fwi[23:26], self.fwi[19:22], self.fwi[0:18]]
        else:
            return [self.fwi]
