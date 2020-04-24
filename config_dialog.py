'''
Screen intended beheavior:
Clicking on a parameter, enables editing its value with the slider or the arrow buttons
Clicking again on the parameter frame or clicking Accept, will set the parameter, although changes will only be applied upon returning to the main screen.
Clicking Cancel buton will undo changes to the selected parameter, and deselect it
Clicking Volver will return to the main screen. A dialog will ask to confirm the changes. If confirmed, the new parameters and/or operation mode will be applied
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent

from confirm_dialog import ConfirmDialog
from ui_config_dialog import Ui_Dialog

from PyQt5.QtWidgets import QDialog, QFrame, QLabel
from PyQt5 import QtCore, Qt

from functools import partial
from parameter import Parameter
import copy

class ConfigDialog(QDialog, Ui_Dialog):

    def __init__(self, params: dict, parent=None):
        QDialog.__init__(self, parent)
        self.params = copy.deepcopy(params)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: lightgray; color: black;")
        self.setGeometry(0, 0, self.width(), self.height())
        for f in self.findChildren(QFrame):
            if f.objectName().startswith("frm"):
                f.mousePressEvent = partial(self.frame_pressed, f)
        self.selected_op_mode = ""
        self.selected_param: Parameter = None
        self.selected_param_frame = QFrame()
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)
        self.btn_left_arrow.pressed.connect(self.btn_left_arrow_pressed)
        self.btn_right_arrow.pressed.connect(self.btn_right_arrow_pressed)
        self.adjusting(False)
        self.btnAceptar.pressed.connect(self.btnAceptar_pressed)
        self.btnCancelar.pressed.connect(self.btnCancelar_pressed)
        self.btnVolver.pressed.connect(self.btnVolver_pressed)
        self.uncommited_change = False  # flag para indica que se cambió el valor de un parámetro, pero no se ha guardado

        # Pone los valores actuales en los labels
        for name, param in self.params.items():
            frame_name = "frm_" + name
            f = self.findChild(QFrame, name=frame_name)
            if f:
                self.get_value_label(f).setText(f"{param.value:{param.value_format}}")

    def btnAceptar_pressed(self):
        if self.selected_param is not None:
            self.confirm_param()

    def btnCancelar_pressed(self):
        if self.selected_param is not None:
            self.get_value_label(self.selected_param_frame).setText(f"{self.selected_param.value:{self.selected_param.value_format}}")
            self.selected_param_frame.setFrameShadow(QFrame.Raised)
            self.selected_param = None
            self.selected_param_frame = None
        self.adjusting(False)
        self.uncommited_change = False

    def btnVolver_pressed(self):
        dlg = ConfirmDialog()
        if dlg.exec_():
            self.accept()
        else:
            self.reject()

    def adjusting(self, enabled):
        if enabled:
            self.btn_left_arrow.show()
            self.btn_right_arrow.show()
            self.horizontalSlider.show()
            self.btnVolver.setEnabled(False)
        else:
            self.btn_left_arrow.hide()
            self.btn_right_arrow.hide()
            self.horizontalSlider.hide()
            self.btnVolver.setEnabled(True)

        self.btn_left_arrow.setEnabled(enabled)
        self.btn_right_arrow.setEnabled(enabled)
        self.horizontalSlider.setEnabled(enabled)

    def btn_left_arrow_pressed(self):
        fmt = self.selected_param.value_format
        step = self.selected_param.value_step
        value = float(self.get_value_label(self.selected_param_frame).text())
        value -= step
        self.get_value_label(self.selected_param_frame).setText(f"{value:{fmt}}")
        self.update_slider(value)
        self.uncommited_change = True
        if value - step < self.selected_param.value_min:
            self.btn_left_arrow.setEnabled(False)
        if value + step < self.selected_param.value_max:
            self.btn_right_arrow.setEnabled(True)

    def btn_right_arrow_pressed(self):
        fmt = self.selected_param.value_format
        step = self.selected_param.value_step
        value = float(self.get_value_label(self.selected_param_frame).text())
        value += step
        self.get_value_label(self.selected_param_frame).setText(f"{value:{fmt}}")
        self.update_slider(value)
        self.uncommited_change = True
        if value + step > self.selected_param.value_max:
            self.btn_right_arrow.setEnabled(False)
        if value - step > self.selected_param.value_min:
            self.btn_left_arrow.setEnabled(True)

    def update_slider(self, val):
        # Desconecta antes de cambiar el valor, de lo contrario esto gatillaría a su vez un cambio de este label
        try:
            self.horizontalSlider.disconnect()
        except TypeError:
            pass
        self.horizontalSlider.setValue(self.param_to_slider_value(self.selected_param, val))
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)

    def confirm_param(self):
        self.selected_param.value = float(self.get_value_label(self.selected_param_frame).text())
        self.selected_param_frame.setFrameShadow(QFrame.Raised)
        self.selected_param = None
        self.selected_param_frame = None
        self.adjusting(False)
        self.uncommited_change = False

    def frame_pressed(self, frame: QFrame, event: QMouseEvent):
        if frame.parent().objectName() == "frm_values":
            if frame == self.selected_param_frame:  # Confirma el parámetro
                self.confirm_param()
                return
            elif not self.uncommited_change:
                self.unselect_child_frames(frame.parent())
                frame.setFrameShadow(QFrame.Sunken)
                self.adjusting(True)
                self.selected_param_frame = frame
                self.selected_param = self.params[frame.objectName().replace("frm_", "")]
                val = float(self.get_value_label(frame).text())
                self.update_slider(val)
                print(f"Selected param: {self.selected_param.screen_name}")
        elif frame.parent().objectName() == "frm_op_mode" and not self.uncommited_change:
            self.unselect_child_frames(frame.parent())
            frame.setFrameShadow(QFrame.Sunken)

    def unselect_child_frames(self, frame):
        for f in frame.findChildren(QFrame, options=QtCore.Qt.FindDirectChildrenOnly):
            f.setFrameShadow(QFrame.Raised)

    def get_value_label(self, frame):
        for label in frame.findChildren(QLabel):
            if "value" in label.objectName():
                return label

    def slider_value_changed(self, val):
        fmt = self.selected_param.value_format
        value = self.slider_to_param_value(self.selected_param)
        self.get_value_label(self.selected_param_frame).setText(f"{value:{fmt}}")
        self.uncommited_change = True
        if value + self.selected_param.value_step > self.selected_param.value_max:
            self.btn_right_arrow.setEnabled(False)
        if value - self.selected_param.value_step > self.selected_param.value_min:
            self.btn_left_arrow.setEnabled(True)
        if value - self.selected_param.value_step < self.selected_param.value_min:
            self.btn_left_arrow.setEnabled(False)
        if value + self.selected_param.value_step < self.selected_param.value_max:
            self.btn_right_arrow.setEnabled(True)

    def slider_to_param_value(self, param):
        return self.horizontalSlider.value() / self.horizontalSlider.maximum() \
              * (param.value_max - param.value_min) + param.value_min

    def param_to_slider_value(self, param, value):
        return (value - param.value_min) / (param.value_max - param.value_min) * self.horizontalSlider.maximum()