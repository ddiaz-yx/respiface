# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_set.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)
        Dialog.setMinimumSize(QtCore.QSize(800, 480))
        Dialog.setMaximumSize(QtCore.QSize(800, 480))
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_confirmar = QtWidgets.QPushButton(self.frame)
        self.btn_confirmar.setGeometry(QtCore.QRect(641, 10, 140, 60))
        self.btn_confirmar.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_confirmar.setFont(font)
        self.btn_confirmar.setObjectName("btn_confirmar")
        self.horizontalSlider = QtWidgets.QSlider(self.frame)
        self.horizontalSlider.setGeometry(QtCore.QRect(11, 410, 781, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.btn_down_left = QtWidgets.QPushButton(self.frame)
        self.btn_down_left.setGeometry(QtCore.QRect(180, 230, 100, 100))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        self.btn_down_left.setFont(font)
        self.btn_down_left.setObjectName("btn_down_left")
        self.lbl_param_value = QtWidgets.QLabel(self.frame)
        self.lbl_param_value.setGeometry(QtCore.QRect(291, 180, 221, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_param_value.sizePolicy().hasHeightForWidth())
        self.lbl_param_value.setSizePolicy(sizePolicy)
        self.lbl_param_value.setMinimumSize(QtCore.QSize(0, 70))
        self.lbl_param_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_param_value.setObjectName("lbl_param_value")
        self.lbl_max = QtWidgets.QLabel(self.frame)
        self.lbl_max.setGeometry(QtCore.QRect(730, 350, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_max.setFont(font)
        self.lbl_max.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.lbl_max.setObjectName("lbl_max")
        self.btn_up = QtWidgets.QPushButton(self.frame)
        self.btn_up.setGeometry(QtCore.QRect(520, 100, 100, 100))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        self.btn_up.setFont(font)
        self.btn_up.setObjectName("btn_up")
        self.lbl_min = QtWidgets.QLabel(self.frame)
        self.lbl_min.setGeometry(QtCore.QRect(11, 370, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_min.setFont(font)
        self.lbl_min.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.lbl_min.setObjectName("lbl_min")
        self.btn_down = QtWidgets.QPushButton(self.frame)
        self.btn_down.setGeometry(QtCore.QRect(520, 230, 100, 100))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        self.btn_down.setFont(font)
        self.btn_down.setObjectName("btn_down")
        self.btn_anular = QtWidgets.QPushButton(self.frame)
        self.btn_anular.setGeometry(QtCore.QRect(21, 10, 140, 60))
        self.btn_anular.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_anular.setFont(font)
        self.btn_anular.setObjectName("btn_anular")
        self.lbl_param_name = QtWidgets.QLabel(self.frame)
        self.lbl_param_name.setGeometry(QtCore.QRect(170, 20, 461, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_param_name.sizePolicy().hasHeightForWidth())
        self.lbl_param_name.setSizePolicy(sizePolicy)
        self.lbl_param_name.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.lbl_param_name.setFont(font)
        self.lbl_param_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_param_name.setObjectName("lbl_param_name")
        self.btn_up_left = QtWidgets.QPushButton(self.frame)
        self.btn_up_left.setGeometry(QtCore.QRect(180, 100, 100, 100))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(28)
        self.btn_up_left.setFont(font)
        self.btn_up_left.setObjectName("btn_up_left")
        self.grp_affected_params = QtWidgets.QGroupBox(self.frame)
        self.grp_affected_params.setGeometry(QtCore.QRect(640, 100, 141, 231))
        self.grp_affected_params.setObjectName("grp_affected_params")
        self.lbl_aff_param_name_1 = QtWidgets.QLabel(self.grp_affected_params)
        self.lbl_aff_param_name_1.setGeometry(QtCore.QRect(10, 30, 121, 16))
        self.lbl_aff_param_name_1.setObjectName("lbl_aff_param_name_1")
        self.lbl_aff_param_value_1 = QtWidgets.QLabel(self.grp_affected_params)
        self.lbl_aff_param_value_1.setGeometry(QtCore.QRect(8, 50, 121, 20))
        self.lbl_aff_param_value_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_aff_param_value_1.setObjectName("lbl_aff_param_value_1")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_confirmar.setText(_translate("Dialog", "Confirmar"))
        self.btn_down_left.setText(_translate("Dialog", "\\/"))
        self.lbl_param_value.setText(_translate("Dialog", "3.1"))
        self.lbl_max.setText(_translate("Dialog", "Max"))
        self.btn_up.setText(_translate("Dialog", "/\\"))
        self.lbl_min.setText(_translate("Dialog", "Min"))
        self.btn_down.setText(_translate("Dialog", "\\/"))
        self.btn_anular.setText(_translate("Dialog", "Anular"))
        self.lbl_param_name.setText(_translate("Dialog", "Param [units]"))
        self.btn_up_left.setText(_translate("Dialog", "/\\"))
        self.grp_affected_params.setTitle(_translate("Dialog", "Parámetros afectados"))
        self.lbl_aff_param_name_1.setText(_translate("Dialog", "Vol. Tidal [mL]:"))
        self.lbl_aff_param_value_1.setText(_translate("Dialog", "500"))
