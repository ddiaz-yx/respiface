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
        font = QtGui.QFont()
        font.setPointSize(9)
        Dialog.setFont(font)
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
        self.grp_affected_params.setGeometry(QtCore.QRect(20, 100, 141, 101))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.grp_affected_params.setFont(font)
        self.grp_affected_params.setObjectName("grp_affected_params")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.grp_affected_params)
        self.verticalLayout.setContentsMargins(1, 1, 1, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_aff_param_name_1 = QtWidgets.QLabel(self.grp_affected_params)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_aff_param_name_1.setFont(font)
        self.lbl_aff_param_name_1.setObjectName("lbl_aff_param_name_1")
        self.verticalLayout.addWidget(self.lbl_aff_param_name_1)
        self.lbl_aff_param_value_1 = QtWidgets.QLabel(self.grp_affected_params)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_aff_param_value_1.setFont(font)
        self.lbl_aff_param_value_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lbl_aff_param_value_1.setObjectName("lbl_aff_param_value_1")
        self.verticalLayout.addWidget(self.lbl_aff_param_value_1)
        self.grp_times = QtWidgets.QGroupBox(self.frame)
        self.grp_times.setGeometry(QtCore.QRect(20, 219, 141, 111))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.grp_times.setFont(font)
        self.grp_times.setObjectName("grp_times")
        self.gridLayout = QtWidgets.QGridLayout(self.grp_times)
        self.gridLayout.setContentsMargins(1, -1, 1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.grp_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.grp_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lbl_it = QtWidgets.QLabel(self.grp_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_it.setFont(font)
        self.lbl_it.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_it.setObjectName("lbl_it")
        self.gridLayout.addWidget(self.lbl_it, 0, 1, 1, 1)
        self.lbl_et = QtWidgets.QLabel(self.grp_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_et.setFont(font)
        self.lbl_et.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_et.setObjectName("lbl_et")
        self.gridLayout.addWidget(self.lbl_et, 1, 1, 1, 1)
        self.lbl_ptt_title = QtWidgets.QLabel(self.grp_times)
        self.lbl_ptt_title.setObjectName("lbl_ptt_title")
        self.gridLayout.addWidget(self.lbl_ptt_title, 3, 0, 1, 1)
        self.lbl_ptt = QtWidgets.QLabel(self.grp_times)
        self.lbl_ptt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_ptt.setObjectName("lbl_ptt")
        self.gridLayout.addWidget(self.lbl_ptt, 3, 1, 1, 1)
        self.lbl_flowt_title = QtWidgets.QLabel(self.grp_times)
        self.lbl_flowt_title.setObjectName("lbl_flowt_title")
        self.gridLayout.addWidget(self.lbl_flowt_title, 2, 0, 1, 1)
        self.lbl_flowt = QtWidgets.QLabel(self.grp_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_flowt.setFont(font)
        self.lbl_flowt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_flowt.setObjectName("lbl_flowt")
        self.gridLayout.addWidget(self.lbl_flowt, 2, 1, 1, 1)

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
        self.grp_times.setTitle(_translate("Dialog", "Tiempos [s]:"))
        self.label_2.setText(_translate("Dialog", "Espiración:"))
        self.label.setText(_translate("Dialog", "Inspiración:"))
        self.lbl_it.setText(_translate("Dialog", "0.0"))
        self.lbl_et.setText(_translate("Dialog", "0.0"))
        self.lbl_ptt_title.setText(_translate("Dialog", "Plateu:"))
        self.lbl_ptt.setText(_translate("Dialog", "0.0"))
        self.lbl_flowt_title.setText(_translate("Dialog", "Flujo:"))
        self.lbl_flowt.setText(_translate("Dialog", "0.0"))
