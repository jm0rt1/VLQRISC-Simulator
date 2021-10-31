from __future__ import annotations
from unittest.signals import registerResult
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QHeaderView
import src.GUI.ui_base as ui_base

import random
import src.GUI.regTableModel as tableModel
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
        instruction = instruction_generator.generate()
        self.system.execute(instruction)
        self.instruction_output_lbl.setText(instruction.fwi.bits)

        self.model = tableModel.TableModel(self.system.register_table_bits)
        self.reg_table.setModel(self.model)

        header = self.reg_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
