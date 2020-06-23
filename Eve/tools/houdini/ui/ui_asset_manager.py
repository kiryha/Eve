# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\houdini\ui\ui_asset_manager.ui',
# licensing of 'E:\Eve\Eve\tools\houdini\ui\ui_asset_manager.ui' applies.
#
# Created: Tue Jun 23 16:26:15 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AssetManager(object):
    def setupUi(self, AssetManager):
        AssetManager.setObjectName("AssetManager")
        AssetManager.resize(351, 105)
        self.verticalLayout = QtWidgets.QVBoxLayout(AssetManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(AssetManager)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_3 = QtWidgets.QLabel(self.splitter_2)
        self.label_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_3.setObjectName("label_3")
        self.boxAssetTypeFilter = QtWidgets.QComboBox(self.splitter_2)
        self.boxAssetTypeFilter.setObjectName("boxAssetTypeFilter")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter = QtWidgets.QSplitter(AssetManager)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_2.setObjectName("label_2")
        self.boxAssetName = QtWidgets.QComboBox(self.splitter)
        self.boxAssetName.setObjectName("boxAssetName")
        self.verticalLayout.addWidget(self.splitter)
        self.btnAssetCrete = QtWidgets.QPushButton(AssetManager)
        self.btnAssetCrete.setMinimumSize(QtCore.QSize(0, 35))
        self.btnAssetCrete.setObjectName("btnAssetCrete")
        self.verticalLayout.addWidget(self.btnAssetCrete)

        self.retranslateUi(AssetManager)
        QtCore.QMetaObject.connectSlotsByName(AssetManager)

    def retranslateUi(self, AssetManager):
        AssetManager.setWindowTitle(QtWidgets.QApplication.translate("AssetManager", "Asset Managet", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AssetManager", "Filter Asset Type:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AssetManager", "Asset Name:", None, -1))
        self.btnAssetCrete.setText(QtWidgets.QApplication.translate("AssetManager", "Create Asset Scene", None, -1))

