from __future__ import annotations
import logging
from unittest.signals import registerResult
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QHeaderView
from src.GUI.error_dialog import Ui_Dialog
import src.GUI.ui_base as ui_base

import random
import src.GUI.regTableModel as tableModel
import src.VLQRISC_Assembler.parser as parser
import src.VLQRISC_Assembler.instructionGenerator as ir
from src.VLQRISC_Simulator.system import VLQRISC_System


class Ui_MainWindow_child(ui_base.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.main_window = MainWindow
        self.system = VLQRISC_System()
        self.update_reg_tbl_btn.clicked.connect(self.update)
        self.command_entry.setClearButtonEnabled(True)
        self.logger = logging.getLogger()
        self.update_reg_table()

    def setupUi(self, MainWindow):
        return super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        return super().retranslateUi(MainWindow)

    def update(self):
        command = self.command_entry.text()
        lp = parser.LineParser(command)
        try:
            line_data = lp.parse()
        except Exception as e:
            self.error_label.setText(str(e))
            self.logger.exception(e)
            return
        instruction_generator = ir.InstructionGenerator(line_data)
        try:
            instruction = instruction_generator.generate()
        except Exception as e:
            self.error_label.setText(str(e))
            self.logger.exception(e)

            return
        try:
            self.system.execute(instruction)
        except Exception as e:
            self.error_label.setText(str(e))
            self.logger.exception(e)

            return
        self.error_label.setText("Success!")

        self.instruction_output_lbl.setText(instruction.fwi.bits)
        self.update_reg_table()

    def update_reg_table(self):
        self.model = tableModel.TableModel(self.system.register_table_bits)
        self.reg_table.setModel(self.model)

        header = self.reg_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
