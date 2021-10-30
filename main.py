from PyQt5 import QtCore, QtGui, QtWidgets

from src.GUI.ui_child import Ui_MainWindow_child
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_child(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
