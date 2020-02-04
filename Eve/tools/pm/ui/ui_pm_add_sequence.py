# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_sequence.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_sequence.ui' applies.
#
# Created: Tue Dec 24 13:12:17 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddShot(object):
    def setupUi(self, AddShot):
        AddShot.setObjectName("AddShot")
        AddShot.resize(370, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddShot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutSequence = QtWidgets.QVBoxLayout()
        self.layoutSequence.setObjectName("layoutSequence")
        self.verticalLayout.addLayout(self.layoutSequence)
        self.btnAddSequence = QtWidgets.QPushButton(AddShot)
        self.btnAddSequence.setMinimumSize(QtCore.QSize(0, 40))
        self.btnAddSequence.setObjectName("btnAddSequence")
        self.verticalLayout.addWidget(self.btnAddSequence)

        self.retranslateUi(AddShot)
        QtCore.QMetaObject.connectSlotsByName(AddShot)

    def retranslateUi(self, AddShot):
        AddShot.setWindowTitle(QtWidgets.QApplication.translate("AddShot", "Add Shot", None, -1))
        self.btnAddSequence.setText(QtWidgets.QApplication.translate("AddShot", "Add Sequence", None, -1))

