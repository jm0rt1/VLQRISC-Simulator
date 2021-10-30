
from PyQt5 import QtCore, QtGui, QtWidgets
from src.GUI.ui_base import Ui_MainWindow


class Ui_MainWindow_child(Ui_MainWindow):
    def setupUi(self, MainWindow):
        return super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        return super().retranslateUi(MainWindow)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_child()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
