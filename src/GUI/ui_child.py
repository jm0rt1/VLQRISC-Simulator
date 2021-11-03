from __future__ import annotations
import logging
from unittest.signals import registerResult
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QHeaderView
import src.GUI.ui_base as ui_base
import pathlib
import random
import src.GUI.tableModels as tableModel
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
        self.instruction_history.itemDoubleClicked.connect(
            self.set_instruction)
        self.update_reg_table()
        self.update_memory_table()
        self.instruction_history.addItems(self.load_items())

    def setupUi(self, MainWindow):
        return super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        return super().retranslateUi(MainWindow)

    def set_instruction(self):
        self.command_entry.setText(
            self.instruction_history.selectedItems()[0].text())

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
        self.update_memory_table()
        self.instruction_history.addItem(command)
        self.save_item(command)

    def update_reg_table(self):
        self.model = tableModel.RegTableModel(self.system.register_table_bits)
        self.reg_table.setModel(self.model)

        header = self.reg_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def update_memory_table(self):
        self.model = tableModel.MemoryTableModel(
            self.system.memory_table_bits)
        self.memory_table.setModel(self.model)

        header = self.reg_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def save_item(self, command: str):
        file = pathlib.Path("./history/command-history.txt")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()
        with open(file, "a") as fp:
            fp.write(f"{command}\n")

    def load_items(self):
        file = pathlib.Path("./history/command-history.txt")
        if file.exists():
            with open(file, "r") as fp:
                lines = fp.readlines()
                return lines
        else:
            return []
