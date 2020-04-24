# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 200)
        Dialog.setMinimumSize(QtCore.QSize(350, 200))
        Dialog.setMaximumSize(QtCore.QSize(350, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAceptar = QtWidgets.QPushButton(Dialog)
        self.btnAceptar.setMinimumSize(QtCore.QSize(100, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnAceptar.setFont(font)
        self.btnAceptar.setObjectName("btnAceptar")
        self.horizontalLayout.addWidget(self.btnAceptar)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnCancelar = QtWidgets.QPushButton(Dialog)
        self.btnCancelar.setMinimumSize(QtCore.QSize(100, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnCancelar.setFont(font)
        self.btnCancelar.setObjectName("btnCancelar")
        self.horizontalLayout.addWidget(self.btnCancelar)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "¿Aplicar la configuración?"))
        self.btnAceptar.setText(_translate("Dialog", "Si"))
        self.btnCancelar.setText(_translate("Dialog", "No"))
