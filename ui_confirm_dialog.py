# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 200)
        Dialog.setMinimumSize(QtCore.QSize(350, 200))
        Dialog.setMaximumSize(QtCore.QSize(350, 200))
        font = QtGui.QFont()
        font.setPointSize(9)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_text = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_text.setFont(font)
        self.lbl_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_text.setObjectName("lbl_text")
        self.verticalLayout.addWidget(self.lbl_text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frm_yes = QtWidgets.QFrame(Dialog)
        self.frm_yes.setMinimumSize(QtCore.QSize(100, 80))
        self.frm_yes.setFrameShape(QtWidgets.QFrame.Box)
        self.frm_yes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_yes.setObjectName("frm_yes")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frm_yes)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frm_yes)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.frm_yes)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.frm_no = QtWidgets.QFrame(Dialog)
        self.frm_no.setMinimumSize(QtCore.QSize(100, 80))
        self.frm_no.setFrameShape(QtWidgets.QFrame.Box)
        self.frm_no.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_no.setObjectName("frm_no")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frm_no)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frm_no)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout.addWidget(self.frm_no)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_text.setText(_translate("Dialog", "¿Aplicar la configuración?"))
        self.label_2.setText(_translate("Dialog", "Si"))
        self.label_3.setText(_translate("Dialog", "No"))
