from sys import path
from src.GUI.ui_child import Ui_MainWindow_child
from PyQt5 import QtCore, QtGui, QtWidgets
import logging
import logging.handlers
import pathlib


def setup_logging(path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        path, mode='a', maxBytes=256*(10**3), backupCount=25, encoding="utf-8")
    logger.addHandler(rotating_file_handler)
    #formatter = logging.Formatter()


if __name__ == "__main__":
    import sys
    setup_logging(pathlib.Path("./logs/VLQRISC_SIMULATOR.log"))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_child(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
