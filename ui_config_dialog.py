# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_dialog.ui'
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
        Dialog.setAutoFillBackground(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frm_main = QtWidgets.QFrame(Dialog)
        self.frm_main.setAutoFillBackground(True)
        self.frm_main.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_main.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frm_main.setLineWidth(0)
        self.frm_main.setObjectName("frm_main")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frm_main)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_5 = QtWidgets.QFrame(self.frm_main)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frm_op_mode = QtWidgets.QFrame(self.frame_5)
        self.frm_op_mode.setMaximumSize(QtCore.QSize(180, 16777215))
        self.frm_op_mode.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_op_mode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_op_mode.setObjectName("frm_op_mode")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frm_op_mode)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title_op_mode = QtWidgets.QLabel(self.frm_op_mode)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title_op_mode.sizePolicy().hasHeightForWidth())
        self.lbl_title_op_mode.setSizePolicy(sizePolicy)
        self.lbl_title_op_mode.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_title_op_mode.setFont(font)
        self.lbl_title_op_mode.setObjectName("lbl_title_op_mode")
        self.verticalLayout.addWidget(self.lbl_title_op_mode)
        self.frm_param_op_mode_vcv = QtWidgets.QFrame(self.frm_op_mode)
        self.frm_param_op_mode_vcv.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_param_op_mode_vcv.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_op_mode_vcv.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_op_mode_vcv.setLineWidth(2)
        self.frm_param_op_mode_vcv.setObjectName("frm_param_op_mode_vcv")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frm_param_op_mode_vcv)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frm_param_op_mode_vcv)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frm_param_op_mode_vcv)
        self.frm_param_op_mode_pcv = QtWidgets.QFrame(self.frm_op_mode)
        self.frm_param_op_mode_pcv.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_param_op_mode_pcv.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_op_mode_pcv.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_op_mode_pcv.setLineWidth(2)
        self.frm_param_op_mode_pcv.setObjectName("frm_param_op_mode_pcv")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frm_param_op_mode_pcv)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frm_param_op_mode_pcv)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.frm_param_op_mode_pcv)
        self.frm_param_op_mode_simv = QtWidgets.QFrame(self.frm_op_mode)
        self.frm_param_op_mode_simv.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_param_op_mode_simv.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_op_mode_simv.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_op_mode_simv.setLineWidth(2)
        self.frm_param_op_mode_simv.setObjectName("frm_param_op_mode_simv")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frm_param_op_mode_simv)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frm_param_op_mode_simv)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.frm_param_op_mode_simv)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4.addWidget(self.frm_op_mode)
        self.frm_values = QtWidgets.QFrame(self.frame_5)
        self.frm_values.setMinimumSize(QtCore.QSize(400, 0))
        self.frm_values.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_values.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_values.setObjectName("frm_values")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frm_values)
        self.gridLayout_2.setSpacing(8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frm_param_ier = QtWidgets.QFrame(self.frm_values)
        self.frm_param_ier.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_ier.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_ier.setLineWidth(2)
        self.frm_param_ier.setMidLineWidth(0)
        self.frm_param_ier.setObjectName("frm_param_ier")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frm_param_ier)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lbl_basic_5 = QtWidgets.QLabel(self.frm_param_ier)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_basic_5.setFont(font)
        self.lbl_basic_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_5.setObjectName("lbl_basic_5")
        self.horizontalLayout_7.addWidget(self.lbl_basic_5)
        self.lbl_basic_value_5 = QtWidgets.QLabel(self.frm_param_ier)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_5.setFont(font)
        self.lbl_basic_value_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_basic_value_5.setObjectName("lbl_basic_value_5")
        self.horizontalLayout_7.addWidget(self.lbl_basic_value_5)
        self.gridLayout_2.addWidget(self.frm_param_ier, 5, 0, 1, 1)
        self.frm_param_brpm = QtWidgets.QFrame(self.frm_values)
        self.frm_param_brpm.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_brpm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_brpm.setLineWidth(2)
        self.frm_param_brpm.setMidLineWidth(0)
        self.frm_param_brpm.setObjectName("frm_param_brpm")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frm_param_brpm)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lbl_basic_2 = QtWidgets.QLabel(self.frm_param_brpm)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_basic_2.setFont(font)
        self.lbl_basic_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_2.setObjectName("lbl_basic_2")
        self.horizontalLayout_10.addWidget(self.lbl_basic_2)
        self.lbl_basic_value_2 = QtWidgets.QLabel(self.frm_param_brpm)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_2.setFont(font)
        self.lbl_basic_value_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_basic_value_2.setObjectName("lbl_basic_value_2")
        self.horizontalLayout_10.addWidget(self.lbl_basic_value_2)
        self.gridLayout_2.addWidget(self.frm_param_brpm, 2, 0, 1, 1)
        self.frm_param_mode_dep_1 = QtWidgets.QFrame(self.frm_values)
        self.frm_param_mode_dep_1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_mode_dep_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_mode_dep_1.setLineWidth(2)
        self.frm_param_mode_dep_1.setMidLineWidth(0)
        self.frm_param_mode_dep_1.setObjectName("frm_param_mode_dep_1")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frm_param_mode_dep_1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lbl_basic_1 = QtWidgets.QLabel(self.frm_param_mode_dep_1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_basic_1.setFont(font)
        self.lbl_basic_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_1.setObjectName("lbl_basic_1")
        self.horizontalLayout_6.addWidget(self.lbl_basic_1)
        self.lbl_basic_value_1 = QtWidgets.QLabel(self.frm_param_mode_dep_1)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_1.setFont(font)
        self.lbl_basic_value_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_basic_value_1.setObjectName("lbl_basic_value_1")
        self.horizontalLayout_6.addWidget(self.lbl_basic_value_1)
        self.gridLayout_2.addWidget(self.frm_param_mode_dep_1, 1, 0, 1, 1)
        self.frm_param_mf = QtWidgets.QFrame(self.frm_values)
        self.frm_param_mf.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_mf.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_mf.setLineWidth(2)
        self.frm_param_mf.setMidLineWidth(0)
        self.frm_param_mf.setObjectName("frm_param_mf")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frm_param_mf)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lbl_sec_1 = QtWidgets.QLabel(self.frm_param_mf)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_sec_1.setFont(font)
        self.lbl_sec_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sec_1.setObjectName("lbl_sec_1")
        self.horizontalLayout_11.addWidget(self.lbl_sec_1)
        self.lbl_basic_value_6 = QtWidgets.QLabel(self.frm_param_mf)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_6.setFont(font)
        self.lbl_basic_value_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_value_6.setObjectName("lbl_basic_value_6")
        self.horizontalLayout_11.addWidget(self.lbl_basic_value_6)
        self.gridLayout_2.addWidget(self.frm_param_mf, 1, 2, 1, 1)
        self.frm_param_fio2 = QtWidgets.QFrame(self.frm_values)
        self.frm_param_fio2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_fio2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_fio2.setLineWidth(2)
        self.frm_param_fio2.setMidLineWidth(0)
        self.frm_param_fio2.setObjectName("frm_param_fio2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frm_param_fio2)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lbl_basic_4 = QtWidgets.QLabel(self.frm_param_fio2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_basic_4.setFont(font)
        self.lbl_basic_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_4.setObjectName("lbl_basic_4")
        self.horizontalLayout_8.addWidget(self.lbl_basic_4)
        self.lbl_basic_value_4 = QtWidgets.QLabel(self.frm_param_fio2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_4.setFont(font)
        self.lbl_basic_value_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_basic_value_4.setObjectName("lbl_basic_value_4")
        self.horizontalLayout_8.addWidget(self.lbl_basic_value_4)
        self.gridLayout_2.addWidget(self.frm_param_fio2, 4, 0, 1, 1)
        self.frm_param_peep = QtWidgets.QFrame(self.frm_values)
        self.frm_param_peep.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_peep.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_peep.setLineWidth(2)
        self.frm_param_peep.setMidLineWidth(0)
        self.frm_param_peep.setObjectName("frm_param_peep")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frm_param_peep)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lbl_basic_3 = QtWidgets.QLabel(self.frm_param_peep)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_basic_3.setFont(font)
        self.lbl_basic_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_3.setObjectName("lbl_basic_3")
        self.horizontalLayout_9.addWidget(self.lbl_basic_3)
        self.lbl_basic_value_3 = QtWidgets.QLabel(self.frm_param_peep)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_3.setFont(font)
        self.lbl_basic_value_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_basic_value_3.setObjectName("lbl_basic_value_3")
        self.horizontalLayout_9.addWidget(self.lbl_basic_value_3)
        self.gridLayout_2.addWidget(self.frm_param_peep, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 1, 1, 1)
        self.lbl_title_basic_params = QtWidgets.QLabel(self.frm_values)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title_basic_params.sizePolicy().hasHeightForWidth())
        self.lbl_title_basic_params.setSizePolicy(sizePolicy)
        self.lbl_title_basic_params.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_title_basic_params.setFont(font)
        self.lbl_title_basic_params.setObjectName("lbl_title_basic_params")
        self.gridLayout_2.addWidget(self.lbl_title_basic_params, 0, 0, 1, 1)
        self.frm_param_pt = QtWidgets.QFrame(self.frm_values)
        self.frm_param_pt.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frm_param_pt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_param_pt.setLineWidth(2)
        self.frm_param_pt.setObjectName("frm_param_pt")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frm_param_pt)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.lbl_sec_2 = QtWidgets.QLabel(self.frm_param_pt)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_sec_2.setFont(font)
        self.lbl_sec_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sec_2.setObjectName("lbl_sec_2")
        self.horizontalLayout_12.addWidget(self.lbl_sec_2)
        self.lbl_basic_value_7 = QtWidgets.QLabel(self.frm_param_pt)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lbl_basic_value_7.setFont(font)
        self.lbl_basic_value_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_basic_value_7.setObjectName("lbl_basic_value_7")
        self.horizontalLayout_12.addWidget(self.lbl_basic_value_7)
        self.gridLayout_2.addWidget(self.frm_param_pt, 2, 2, 1, 1)
        self.frm_times = QtWidgets.QFrame(self.frm_values)
        self.frm_times.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_times.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_times.setObjectName("frm_times")
        self.gridLayout = QtWidgets.QGridLayout(self.frm_times)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_flowt = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_flowt.setFont(font)
        self.lbl_flowt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_flowt.setObjectName("lbl_flowt")
        self.gridLayout.addWidget(self.lbl_flowt, 2, 1, 1, 1)
        self.lbl_flowt_title = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_flowt_title.setFont(font)
        self.lbl_flowt_title.setObjectName("lbl_flowt_title")
        self.gridLayout.addWidget(self.lbl_flowt_title, 2, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)
        self.lbl_et = QtWidgets.QLabel(self.frm_times)
        self.lbl_et.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_et.setObjectName("lbl_et")
        self.gridLayout.addWidget(self.lbl_et, 1, 1, 1, 1)
        self.lbl_it = QtWidgets.QLabel(self.frm_times)
        self.lbl_it.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_it.setObjectName("lbl_it")
        self.gridLayout.addWidget(self.lbl_it, 0, 1, 1, 1)
        self.lbl_ptt_title = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_ptt_title.setFont(font)
        self.lbl_ptt_title.setObjectName("lbl_ptt_title")
        self.gridLayout.addWidget(self.lbl_ptt_title, 3, 0, 1, 1)
        self.lbl_ptt = QtWidgets.QLabel(self.frm_times)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lbl_ptt.setFont(font)
        self.lbl_ptt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_ptt.setObjectName("lbl_ptt")
        self.gridLayout.addWidget(self.lbl_ptt, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frm_times, 4, 2, 2, 1)
        self.horizontalLayout_4.addWidget(self.frm_values)
        self.frm_buttons = QtWidgets.QFrame(self.frame_5)
        self.frm_buttons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_buttons.setObjectName("frm_buttons")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frm_buttons)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lbl_title_right = QtWidgets.QLabel(self.frm_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title_right.sizePolicy().hasHeightForWidth())
        self.lbl_title_right.setSizePolicy(sizePolicy)
        self.lbl_title_right.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_title_right.setFont(font)
        self.lbl_title_right.setText("")
        self.lbl_title_right.setObjectName("lbl_title_right")
        self.verticalLayout_5.addWidget(self.lbl_title_right)
        self.frm_aceptar = QtWidgets.QFrame(self.frm_buttons)
        self.frm_aceptar.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_aceptar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_aceptar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_aceptar.setObjectName("frm_aceptar")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frm_aceptar)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.frm_aceptar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.verticalLayout_5.addWidget(self.frm_aceptar)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.frm_cancelar = QtWidgets.QFrame(self.frm_buttons)
        self.frm_cancelar.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_cancelar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_cancelar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_cancelar.setObjectName("frm_cancelar")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frm_cancelar)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.frm_cancelar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.verticalLayout_5.addWidget(self.frm_cancelar)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.frm_volver = QtWidgets.QFrame(self.frm_buttons)
        self.frm_volver.setMinimumSize(QtCore.QSize(0, 70))
        self.frm_volver.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_volver.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_volver.setObjectName("frm_volver")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frm_volver)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.frm_volver)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.verticalLayout_5.addWidget(self.frm_volver)
        self.horizontalLayout_4.addWidget(self.frm_buttons)
        self.verticalLayout_6.addWidget(self.frame_5)
        self.line = QtWidgets.QFrame(self.frm_main)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.frm_adjust = QtWidgets.QFrame(self.frm_main)
        self.frm_adjust.setMinimumSize(QtCore.QSize(0, 50))
        self.frm_adjust.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_adjust.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_adjust.setObjectName("frm_adjust")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frm_adjust)
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frm_left_arrow = QtWidgets.QFrame(self.frm_adjust)
        self.frm_left_arrow.setMinimumSize(QtCore.QSize(60, 0))
        self.frm_left_arrow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_left_arrow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_left_arrow.setObjectName("frm_left_arrow")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frm_left_arrow)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_4 = QtWidgets.QLabel(self.frm_left_arrow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.horizontalLayout_5.addWidget(self.frm_left_arrow)
        self.horizontalSlider = QtWidgets.QSlider(self.frm_adjust)
        self.horizontalSlider.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_5.addWidget(self.horizontalSlider)
        self.frm_right_arrow = QtWidgets.QFrame(self.frm_adjust)
        self.frm_right_arrow.setMinimumSize(QtCore.QSize(60, 0))
        self.frm_right_arrow.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_right_arrow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_right_arrow.setObjectName("frm_right_arrow")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frm_right_arrow)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.frm_right_arrow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.horizontalLayout_5.addWidget(self.frm_right_arrow)
        self.frm_left_arrow_2 = QtWidgets.QFrame(self.frm_adjust)
        self.frm_left_arrow_2.setMinimumSize(QtCore.QSize(60, 0))
        self.frm_left_arrow_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_left_arrow_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_left_arrow_2.setObjectName("frm_left_arrow_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frm_left_arrow_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.frm_left_arrow_2)
        self.label_9.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_10.addWidget(self.label_9)
        self.horizontalLayout_5.addWidget(self.frm_left_arrow_2)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.frm_adjust)
        self.horizontalSlider_2.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalLayout_5.addWidget(self.horizontalSlider_2)
        self.frm_right_arrow_2 = QtWidgets.QFrame(self.frm_adjust)
        self.frm_right_arrow_2.setMinimumSize(QtCore.QSize(60, 0))
        self.frm_right_arrow_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_right_arrow_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_right_arrow_2.setObjectName("frm_right_arrow_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frm_right_arrow_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.frm_right_arrow_2)
        self.label_10.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_11.addWidget(self.label_10)
        self.horizontalLayout_5.addWidget(self.frm_right_arrow_2)
        self.verticalLayout_6.addWidget(self.frm_adjust)
        self.verticalLayout_2.addWidget(self.frm_main)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_title_op_mode.setText(_translate("Dialog", "Modo de operación"))
        self.label.setText(_translate("Dialog", "VCV"))
        self.label_2.setText(_translate("Dialog", "PCV"))
        self.label_3.setText(_translate("Dialog", "SIMV"))
        self.lbl_basic_5.setText(_translate("Dialog", "Ratio I:E"))
        self.lbl_basic_value_5.setText(_translate("Dialog", "0:0"))
        self.lbl_basic_2.setText(_translate("Dialog", "Frec. Resp. \n"
"[resp/min]"))
        self.lbl_basic_value_2.setText(_translate("Dialog", "0"))
        self.lbl_basic_1.setText(_translate("Dialog", "V. Tidal\n"
"[mL]"))
        self.lbl_basic_value_1.setText(_translate("Dialog", "0"))
        self.lbl_sec_1.setText(_translate("Dialog", "Flujo max\n"
"[L/min]"))
        self.lbl_basic_value_6.setText(_translate("Dialog", "0"))
        self.lbl_basic_4.setText(_translate("Dialog", "<html>Conc.O<span style=\" vertical-align:sub;\">2</span><br>[%]</html>"))
        self.lbl_basic_value_4.setText(_translate("Dialog", "0"))
        self.lbl_basic_3.setText(_translate("Dialog", "<html>PEEP <br>[cm H<span style=\" vertical-align:sub;\">2</span>O]</html>"))
        self.lbl_basic_value_3.setText(_translate("Dialog", "0"))
        self.lbl_title_basic_params.setText(_translate("Dialog", "Parámetros"))
        self.lbl_sec_2.setText(_translate("Dialog", "T. Plateu\n"
"[%]"))
        self.lbl_basic_value_7.setText(_translate("Dialog", "0"))
        self.lbl_flowt.setText(_translate("Dialog", "0.0"))
        self.lbl_flowt_title.setText(_translate("Dialog", "T. flujo [s]:"))
        self.label_11.setText(_translate("Dialog", "T. inspiración [s]:"))
        self.label_12.setText(_translate("Dialog", "T. espiración [s]:"))
        self.lbl_et.setText(_translate("Dialog", "0.0"))
        self.lbl_it.setText(_translate("Dialog", "0.0"))
        self.lbl_ptt_title.setText(_translate("Dialog", "T. plateu [s]:"))
        self.lbl_ptt.setText(_translate("Dialog", "0.0"))
        self.label_5.setText(_translate("Dialog", "Aceptar"))
        self.label_6.setText(_translate("Dialog", "Cancelar"))
        self.label_7.setText(_translate("Dialog", "Volver"))
        self.label_4.setText(_translate("Dialog", "<"))
        self.label_8.setText(_translate("Dialog", ">"))
        self.label_9.setText(_translate("Dialog", "<"))
        self.label_10.setText(_translate("Dialog", ">"))
