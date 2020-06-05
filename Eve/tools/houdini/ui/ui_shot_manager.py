# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\houdini\ui\ui_shot_manager.ui',
# licensing of 'E:\Eve\Eve\tools\houdini\ui\ui_shot_manager.ui' applies.
#
# Created: Fri Jun 05 11:30:02 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ShotManager(object):
    def setupUi(self, ShotManager):
        ShotManager.setObjectName("ShotManager")
        ShotManager.resize(348, 120)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShotManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(ShotManager)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.boxSequence = QtWidgets.QComboBox(self.splitter)
        self.boxSequence.setObjectName("boxSequence")
        self.boxShot = QtWidgets.QComboBox(self.splitter)
        self.boxShot.setObjectName("boxShot")
        self.verticalLayout.addWidget(self.splitter)
        self.btnCreateAnimationScene = QtWidgets.QPushButton(ShotManager)
        self.btnCreateAnimationScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnCreateAnimationScene.setObjectName("btnCreateAnimationScene")
        self.verticalLayout.addWidget(self.btnCreateAnimationScene)
        self.btnCreateRenderScene = QtWidgets.QPushButton(ShotManager)
        self.btnCreateRenderScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnCreateRenderScene.setObjectName("btnCreateRenderScene")
        self.verticalLayout.addWidget(self.btnCreateRenderScene)

        self.retranslateUi(ShotManager)
        QtCore.QMetaObject.connectSlotsByName(ShotManager)

    def retranslateUi(self, ShotManager):
        ShotManager.setWindowTitle(QtWidgets.QApplication.translate("ShotManager", "Shot Manager", None, -1))
        self.btnCreateAnimationScene.setText(QtWidgets.QApplication.translate("ShotManager", "Create Animation Scene", None, -1))
        self.btnCreateRenderScene.setText(QtWidgets.QApplication.translate("ShotManager", "Create Render Scene", None, -1))

