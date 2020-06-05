import hou
from PySide2 import QtCore, QtUiTools, QtWidgets
from ui import ui_shot_manager

class Window(QtWidgets.QDialog, ui_shot_manager.Ui_ShotManager):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.btnCreateRenderScene.clicked.connect(self.prn)

    def prn(self):
        print 'OLA'

def run_shot_manager():
    win = Window()
    win.show()

