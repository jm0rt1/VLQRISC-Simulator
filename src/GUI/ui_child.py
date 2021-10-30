from __future__ import annotations
import src.GUI.ui_base as ui_base

import random
import src.GUI.tableModel as tableModel
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.instructionGenerator as ir
from src.VLQRISC_Simulator.system import VLQRISC_System


class Ui_MainWindow_child(ui_base.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.system = VLQRISC_System()
        self.update_reg_tbl_btn.clicked.connect(self.update_table)
        self.command_entry.setClearButtonEnabled(True)

    def setupUi(self, MainWindow):
        return super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        return super().retranslateUi(MainWindow)

    def update_table(self):
        command = self.command_entry.text()
        lp = parser.LineParser(command)
        line_data = lp.parse()
        instruction_generator = ir.InstructionGenerator(line_data)
        instruction_fwi = instruction_generator.generate()
        self.instruction_output_lbl.setText(instruction_fwi.bits)

        data = []
        for i in range(0, 10):
            data.append([])

            for j in range(0, 2):
                data[i].append(random.randint(1, 100))

        self.model = tableModel.TableModel(self.system.register_table_bits)
        self.reg_table.setModel(self.model)
