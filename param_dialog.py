"""
Sublcase de QDialog que modifica aspectos de estilo únicamente

"""
from PyQt5.QtGui import QFont

from ui_param_set import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import QEvent
from parameter import Parameter, ParamEnum

css = '''
QSlider::groove:horizontal {
    border:                 1px solid #888;
    height:                 10px;
    margin:                 12px;
}
QSlider::handle:horizontal {
    background:             #AAAAAA;
    border:                 1px solid #FFFFFF;
    width:                 25px;
    height:                  40px;
    margin:                 -20px -5px;
}
'''

DEFAULT_VALUE_FONT_SIZE = 60
IE_VALUE_FONT_SIZE = 40

btn_style = """background-color: #BBBBBB; color: black;"""

class ParamSetDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0, 0, self.width(), self.height())
        self.frame.setStyleSheet("background-color: black;")
        self.lbl_param_name.setStyleSheet("color: lightgrey;")
        self.btn_anular.setStyleSheet(btn_style)
        self.btn_confirmar.setStyleSheet(btn_style)
        self.btn_down.setStyleSheet(btn_style)
        self.btn_down_left.setStyleSheet(btn_style)
        self.btn_up.setStyleSheet(btn_style)
        self.btn_up_left.setStyleSheet(btn_style)
        self.horizontalSlider.setStyleSheet(css)
        self.btn_anular.pressed.connect(self.btn_anular_pressed)
        self.lbl_param_value.setFont(QFont('Arial', DEFAULT_VALUE_FONT_SIZE))
        self.btn_up.pressed.connect(self.btn_up_pressed)
        self.btn_down.pressed.connect(self.btn_down_pressed)
        self.btn_up_left.pressed.connect(self.btn_up_left_pressed)
        self.btn_down_left.pressed.connect(self.btn_down_left_pressed)
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)

        self.param: Parameter = None

        self.format = ""
        self.value = 0
        self.value_max = 0
        self.value_min = 0
        self.step = 1

        self.format_i = ""  # para el caso de I:E
        self.value_i = 0  # para el caso de I:E
        self.value_i_max = 0  # para el caso de I:E
        self.value_i_min = 0  # para el caso de I:E
        self.step_i = 1

    def set_parameter(self, p: Parameter):
        self.param = p
        if p.units:
            self.lbl_param_name.setText(self.param.screen_name + " [" + p.units + "]")
        else:
            self.lbl_param_name.setText(self.param.screen_name)
        print(self.param.name)

        if self.param.name == ParamEnum.ier.name:
            self.format = self.param.value_format[1]
            self.value_max = self.param.value_max[1]
            self.value_min = self.param.value_min[1]
            self.step = self.param.value_step[1]
            self.value = self.param.value[1]

            self.format_i = self.param.value_format[0]
            self.value_i_max = self.param.value_max[0]
            self.value_i_min = self.param.value_min[0]
            self.step_i = self.param.value_step[0]
            self.value_i = self.param.value[0]

            self.lbl_param_value.setText(f"{self.value_i:{self.format_i}} : {self.value:{self.format}}")
            self.horizontalSlider.hide()
            self.btn_down_left.show()
            self.btn_up_left.show()
            self.lbl_max.hide()
            self.lbl_min.hide()
            self.lbl_param_value.setFont(QFont('Arial', IE_VALUE_FONT_SIZE))
        else:
            self.format = self.param.value_format
            self.value = self.param.value
            self.value_max = self.param.value_max
            self.value_min = self.param.value_min
            self.step = self.param.value_step

            self.lbl_param_value.setText(f"{self.param.value:{self.param.value_format}}")
            self.btn_down_left.hide()
            self.btn_up_left.hide()
            self.horizontalSlider.setMaximum(self.param.value_max)
            self.horizontalSlider.setMinimum(self.param.value_min)
            self.horizontalSlider.setValue(self.param.value)
            self.horizontalSlider.setSingleStep(self.param.value_step)
            self.horizontalSlider.show()
            self.lbl_max.setText(f"{self.param.value_max:{self.param.value_format}}")
            self.lbl_min.setText(f"{self.param.value_min:{self.param.value_format}}")
            self.lbl_max.show()
            self.lbl_min.show()
            self.lbl_param_value.setFont(QFont('Arial', DEFAULT_VALUE_FONT_SIZE))

        print(f"self.format: {self.format}")
        print(f"self.value: {self.value}")
        print(f"self.value_min: {self.value_min}")
        print(f"self.value_max: {self.value_max}")
        print(f"self.step: {self.step}")

    def slider_value_changed(self, val):
        val = val - val%self.step
        self.lbl_param_value.setText(f"{val:{self.format}}")

    def btn_up_pressed(self):
        txt = self.lbl_param_value.text()
        val = float(txt.split(":")[-1])    # en caso de I:E
        val = val + self.step
        if self.param.name == ParamEnum.ier.name:
            self.lbl_param_value.setText(f"{txt.split(':')[0]}:{val:{self.format}}")
        else:
            self.lbl_param_value.setText(f"{val:{self.param.value_format}}")
            self.horizontalSlider.setValue(val)
        if val > self.value_max - self.step:
            self.btn_up.setDisabled(True)
        if val > self.value_min + self.step:
            self.btn_down.setDisabled(False)

    def btn_down_pressed(self):
        txt = self.lbl_param_value.text()
        val = float(txt.split(":")[-1])    # en caso de I:E
        val = val - self.step
        if self.param.name == ParamEnum.ier.name:
            self.lbl_param_value.setText(f"{txt.split(':')[0]}:{val:{self.format}}")
        else:
            self.lbl_param_value.setText(f"{val:{self.param.value_format}}")
            self.horizontalSlider.setValue(val)
        if val < self.value_min + self.step:
            self.btn_down.setDisabled(True)
        if val < self.value_max - self.step:
            self.btn_up.setDisabled(False)

    def btn_up_left_pressed(self):
        txt = self.lbl_param_value.text()
        val = float(txt.split(":")[0])    # en caso de I:E
        val = val + self.step_i
        self.lbl_param_value.setText(f"{val:{self.format_i}}:{txt.split(':')[-1]}")
        if val > self.value_i_max - self.step_i:
            self.btn_up_left.setDisabled(True)
        if val > self.value_i_min + self.step_i:
            self.btn_down_left.setDisabled(False)

    def btn_down_left_pressed(self):
        txt = self.lbl_param_value.text()
        val = float(txt.split(":")[0])    # en caso de I:E
        val = val - self.param.value_step[0]
        self.lbl_param_value.setText(f"{val:{self.format_i}}:{txt.split(':')[-1]}")
        if val < self.value_i_min + self.step_i:
            self.btn_down_left.setDisabled(True)
        if val < self.value_i_max - self.step_i:
            self.btn_up_left.setDisabled(False)

    def btn_anular_pressed(self):
        self.hide()
