'''
Screen intended beheavior:
Clicking on a parameter, enables editing its value with the slider or the arrow buttons
Clicking again on the parameter frame or clicking Accept, will set the parameter, although changes will only be applied upon returning to the main screen.
Clicking Cancel buton will undo changes to the selected parameter, and deselect it
Clicking Volver will return to the main screen. A dialog will ask to confirm the changes. If confirmed, the new parameters and/or operation mode will be applied
'''
from PyQt5.QtGui import QMouseEvent

from confirm_dialog import ConfirmDialog
from ui_config_dialog import Ui_Dialog

from PyQt5.QtWidgets import QDialog, QFrame, QLabel
from PyQt5 import QtCore, Qt

from functools import partial
from parameter import Parameter
import copy
import styles as st


class ConfigDialog(QDialog, Ui_Dialog):

    def __init__(self, params: dict, parent=None):
        QDialog.__init__(self, parent)
        self.params = copy.deepcopy(params)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.set_styles()
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
        self.frm_aceptar.mousePressEvent = partial(self.frm_aceptar_pressed)
        self.frm_cancelar.mousePressEvent = partial(self.frm_cancelar_pressed)
        self.frm_volver.mousePressEvent = partial(self.frm_volver_pressed)
        self.uncommited_change = False  # flag para indica que se cambió el valor de un parámetro, pero no se ha guardado

        # Pone los valores actuales en los labels
        for name, param in self.params.items():
            frame_name = "frm_param_" + name
            f = self.findChild(QFrame, name=frame_name)
            if f:
                self.get_value_label(f).setText(f"{param.value:{param.value_format}}")

    def set_styles(self):
        self.line.hide()
        self.setStyleSheet("background-color: " + st.BLACK + "; color: lightgrey;")
        self.frm_params_auto.setStyleSheet(st.qss_frm_top)
        self.frm_op_mode.setStyleSheet(".QFrame{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(0, 0, 0, 255));}")
        self.frm_buttons.setStyleSheet(".QFrame{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(0, 0, 0, 255));}")
        self.lbl_title_op_mode.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_basic_params.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_more_params.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_right.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.frm_aceptar.setStyleSheet(st.qss_accept_frame)
        self.frm_cancelar.setStyleSheet(st.qss_cancel_frame)
        self.frm_volver.setStyleSheet(st.qss_return_frame)
        frames = self.findChildren(QFrame)
        for f in frames:
            if f.objectName().startswith('frm_param_'):
                f.setStyleSheet(st.qss_frm_top)

    def frm_aceptar_pressed(self, event: QMouseEvent):
        if self.selected_param is not None:
            self.confirm_param()

    def frm_cancelar_pressed(self, event: QMouseEvent):
        if self.selected_param is not None:
            self.get_value_label(self.selected_param_frame).setText(
                f"{self.selected_param.value:{self.selected_param.value_format}}")
            self.selected_param_frame.setStyleSheet(st.qss_frm_top)
            self.selected_param = None
            self.selected_param_frame = None
        self.adjusting(False)
        self.uncommited_change = False

    def frm_volver_pressed(self, event: QMouseEvent):
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
            self.frm_volver.setDisabled(True)
        else:
            self.btn_left_arrow.hide()
            self.btn_right_arrow.hide()
            self.horizontalSlider.hide()
            self.frm_volver.setEnabled(True)

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
        self.selected_param_frame.setStyleSheet(st.qss_frm_top)
        self.selected_param = None
        self.selected_param_frame = None
        self.adjusting(False)
        self.uncommited_change = False

    def frame_pressed(self, frame: QFrame, event: QMouseEvent):
        if not frame.objectName().replace("frm_param_", "") in self.params.keys():
            return
        if frame.parent().objectName() == "frm_values":
            if frame == self.selected_param_frame:  # Confirma el parámetro
                self.confirm_param()
                return
            elif not self.uncommited_change:
                self.unselect_child_frames(frame.parent())
                frame.setStyleSheet(st.qss_selected_frame + st.qss_lbl_yellow)
                self.adjusting(True)
                self.selected_param_frame = frame
                self.selected_param = self.params[frame.objectName().replace("frm_param_", "")]
                val = float(self.get_value_label(frame).text())
                self.update_slider(val)
                print(f"Selected param: {self.selected_param.screen_name}")
        elif frame.parent().objectName() == "frm_op_mode" and not self.uncommited_change:
            self.unselect_child_frames(frame.parent())
            frame.setFrameShadow(QFrame.Sunken)

    def unselect_child_frames(self, frame):
        for f in frame.findChildren(QFrame, options=QtCore.Qt.FindDirectChildrenOnly):
            if f.objectName().startswith('frm_param_'):
                f.setStyleSheet(st.qss_frm_top)

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
