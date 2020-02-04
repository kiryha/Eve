# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_shot.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_shot.ui' applies.
#
# Created: Tue Dec 24 10:44:09 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Shot(object):
    def setupUi(self, Shot):
        Shot.setObjectName("Shot")
        Shot.resize(369, 356)
        self.verticalLayout = QtWidgets.QVBoxLayout(Shot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QtWidgets.QSplitter(Shot)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.label_3 = QtWidgets.QLabel(self.splitter_3)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setMaximumSize(QtCore.QSize(85, 16777215))
        self.label_3.setObjectName("label_3")
        self.btnProjectName = QtWidgets.QPushButton(self.splitter_3)
        self.btnProjectName.setText("")
        self.btnProjectName.setObjectName("btnProjectName")
        self.verticalLayout.addWidget(self.splitter_3)
        self.splitter = QtWidgets.QSplitter(Shot)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        self.label.setMaximumSize(QtCore.QSize(85, 16777215))
        self.label.setObjectName("label")
        self.linShotName = QtWidgets.QLineEdit(self.splitter)
        self.linShotName.setObjectName("linShotName")
        self.verticalLayout.addWidget(self.splitter)
        self.splitter_5 = QtWidgets.QSplitter(Shot)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.label_7 = QtWidgets.QLabel(self.splitter_5)
        self.label_7.setMinimumSize(QtCore.QSize(120, 0))
        self.label_7.setObjectName("label_7")
        self.linStartFrame = QtWidgets.QLineEdit(self.splitter_5)
        self.linStartFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.linStartFrame.setObjectName("linStartFrame")
        self.linEndFrame = QtWidgets.QLineEdit(self.splitter_5)
        self.linEndFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.linEndFrame.setObjectName("linEndFrame")
        self.verticalLayout.addWidget(self.splitter_5)
        self.label_2 = QtWidgets.QLabel(Shot)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listAssets = QtWidgets.QListView(Shot)
        self.listAssets.setObjectName("listAssets")
        self.verticalLayout.addWidget(self.listAssets)
        self.splitter_2 = QtWidgets.QSplitter(Shot)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.btnLinkAsset = QtWidgets.QPushButton(self.splitter_2)
        self.btnLinkAsset.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btnLinkAsset.setObjectName("btnLinkAsset")
        self.btnUnlinkAsset = QtWidgets.QPushButton(self.splitter_2)
        self.btnUnlinkAsset.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btnUnlinkAsset.setObjectName("btnUnlinkAsset")
        self.verticalLayout.addWidget(self.splitter_2)
        self.label_4 = QtWidgets.QLabel(Shot)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.txtDescription = QtWidgets.QTextEdit(Shot)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtDescription.setObjectName("txtDescription")
        self.verticalLayout.addWidget(self.txtDescription)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Shot)
        QtCore.QMetaObject.connectSlotsByName(Shot)

    def retranslateUi(self, Shot):
        Shot.setWindowTitle(QtWidgets.QApplication.translate("Shot", "Shot", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Shot", "Project Name", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Shot", "Shot Name", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Shot", "Start | End", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Shot", "Linked Assets", None, -1))
        self.btnLinkAsset.setText(QtWidgets.QApplication.translate("Shot", "Link Asset", None, -1))
        self.btnUnlinkAsset.setText(QtWidgets.QApplication.translate("Shot", "Break Link", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Shot", "Shot Description", None, -1))

