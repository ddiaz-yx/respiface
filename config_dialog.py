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
from parameter import Parameter, OpModEnum, ParamEnum
import copy
import styles as st
import numpy as np
SLIDER_MULTIPLIER = 10
EPS = 1e-6

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
        self.selected_param: Parameter = None
        self.selected_param_frame = QFrame()
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)
        self.frm_left_arrow.mousePressEvent = partial(self.frm_left_arrow_pressed)
        self.frm_right_arrow.mousePressEvent = partial(self.frm_right_arrow_pressed)
        self.adjusting(False)
        self.current_value = None
        self.frm_aceptar.mousePressEvent = partial(self.frm_aceptar_pressed)
        self.frm_cancelar.mousePressEvent = partial(self.frm_cancelar_pressed)
        self.frm_volver.mousePressEvent = partial(self.frm_volver_pressed)
        self.uncommited_change = False  # flag para indica que se cambió el valor de un parámetro, pero no se ha guardado
        self.frm_param_op_mode_pcv.mousePressEvent = partial(self.frm_param_op_mode_pcv_pressed)
        self.frm_param_op_mode_vcv.mousePressEvent = partial(self.frm_param_op_mode_vcv_pressed)


        # Pone los valores actuales en los labels
        if self.params['mode'].value == OpModEnum.vcv.value:
            self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_selected)
            self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_top)
        elif self.params['mode'].value == OpModEnum.pcv.value:
            self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_selected)
            self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_top)

        for name, param in self.params.items():
            frame_name = "frm_param_" + name
            f = self.findChild(QFrame, name=frame_name)
            if f:
                if param.value_as_index == True:
                    self.get_value_label(f).setText(f"{param.options[param.value]:{param.value_format}}")
                else:
                    self.get_value_label(f).setText(f"{param.value:{param.value_format}}")

    def set_styles(self):
        self.line.hide()
        self.setStyleSheet("background-color: " + st.BLACK + "; color: lightgrey;")
        self.frm_params_auto.setStyleSheet(st.qss_frm_top)
        self.frm_op_mode.setStyleSheet(st.qss_frm_group)
        self.frm_buttons.setStyleSheet(st.qss_frm_group)
        self.frm_values.setStyleSheet(st.qss_frm_group)
        self.lbl_title_op_mode.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_basic_params.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_more_params.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_right.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.frm_aceptar.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_cancelar.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_volver.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_left_arrow.setStyleSheet(st.qss_frm_top)
        self.frm_right_arrow.setStyleSheet(st.qss_frm_top)
        self.frm_param_op_mode_simv.hide()
        frames = self.findChildren(QFrame)
        for f in frames:
            if f.objectName().startswith('frm_param_'):
                f.setStyleSheet(st.qss_frm_top)

    def frm_param_op_mode_pcv_pressed(self, event: QMouseEvent):
        self.params['mode'].value = OpModEnum.pcv.value
        self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_selected)
        self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_top)

    def frm_param_op_mode_vcv_pressed(self, event: QMouseEvent):
        self.params['mode'].value = OpModEnum.vcv.value
        self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_selected)
        self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_top)

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
            self.frm_left_arrow.show()
            self.frm_right_arrow.show()
            self.horizontalSlider.show()
            self.frm_volver.setDisabled(True)
            self.frm_volver.setStyleSheet(st.qss_frm_but_disbled)
            self.frm_aceptar.setEnabled(True)
            self.frm_aceptar.setStyleSheet(st.qss_frm_but_enabled)
            self.frm_cancelar.setEnabled(True)
            self.frm_cancelar.setStyleSheet(st.qss_frm_but_enabled)
            self.frm_op_mode.setDisabled(True)
        else:
            self.frm_left_arrow.hide()
            self.frm_right_arrow.hide()
            self.horizontalSlider.hide()
            self.frm_volver.setEnabled(True)
            self.frm_volver.setStyleSheet(st.qss_frm_but_enabled)
            self.frm_aceptar.setDisabled(True)
            self.frm_aceptar.setStyleSheet(st.qss_frm_but_disbled)
            self.frm_cancelar.setDisabled(True)
            self.frm_cancelar.setStyleSheet(st.qss_frm_but_disbled)
            self.frm_op_mode.setEnabled(True)

        self.frm_left_arrow.setEnabled(enabled)
        self.frm_right_arrow.setEnabled(enabled)
        self.horizontalSlider.setEnabled(enabled)

    def slider_value_changed(self, val):
        step = self.selected_param.value_step
        self.current_value = self.slider_to_param_value(self.selected_param)
        self.update_selected_label()
        if self.current_value + step > self.selected_param.value_max + EPS:
            self.frm_right_arrow.setEnabled(False)
        if self.current_value - step > self.selected_param.value_min - EPS:
            self.frm_left_arrow.setEnabled(True)
        if self.current_value - step < self.selected_param.value_min - EPS:
            self.frm_left_arrow.setEnabled(False)
        if self.current_value + step < self.selected_param.value_max + EPS:
            self.frm_right_arrow.setEnabled(True)
        self.uncommited_change = True
        print(self.current_value)

    def frm_left_arrow_pressed(self, event: QMouseEvent):
        step = self.selected_param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.current_value -= step
        self.update_selected_label()
        self.update_slider()
        self.uncommited_change = True
        print(self.current_value)
        if self.current_value - step < self.selected_param.value_min - EPS:
            self.frm_left_arrow.setEnabled(False)
        if self.current_value + step < self.selected_param.value_max + EPS:
            self.frm_right_arrow.setEnabled(True)

    def frm_right_arrow_pressed(self, event: QMouseEvent):
        step = self.selected_param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.current_value += step
        self.update_selected_label()
        self.update_slider()
        self.uncommited_change = True

        if self.current_value + step > self.selected_param.value_max + EPS:
            self.frm_right_arrow.setEnabled(False)
        if self.current_value - step > self.selected_param.value_min - EPS:
            self.frm_left_arrow.setEnabled(True)

    def update_selected_label(self):
        """
        Sets the label text to the current param value
        :return:
        """
        fmt = self.selected_param.value_format
        label = self.get_value_label(self.selected_param_frame)
        if self.selected_param.value_as_index:
            label.setText(f"{self.selected_param.options[int(self.current_value)]:{fmt}}")
        else:
            label.setText(f"{self.current_value:{fmt}}")

    def update_slider(self):
        # Desconecta antes de cambiar el valor, de lo contrario esto gatillaría a su vez un cambio de este label
        try:
            self.horizontalSlider.disconnect()
        except TypeError:
            pass
        self.horizontalSlider.setValue(self.param_to_slider_value(self.selected_param, self.current_value))
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)

    def confirm_param(self):
        if self.selected_param.value_as_index:
            self.selected_param.value = int(self.current_value)
        else:
            self.selected_param.value = self.current_value
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
                frame.setStyleSheet(st.qss_frm_selected + st.qss_lbl_yellow)
                self.adjusting(True)
                self.selected_param_frame = frame
                self.selected_param = self.params[frame.objectName().replace("frm_param_", "")]
                self.horizontalSlider.setMaximum(self.selected_param.value_max*SLIDER_MULTIPLIER)
                self.horizontalSlider.setMinimum(self.selected_param.value_min*SLIDER_MULTIPLIER)
                self.horizontalSlider.setSingleStep(1)
                self.current_value = self.selected_param.value
                self.update_slider()
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

    def slider_to_param_value(self, param):
        val = self.horizontalSlider.value()/SLIDER_MULTIPLIER
        if param.value_as_index:
            return int(val)
        else:
            return val - (val%param.value_step)# float(f"{val:{param.value_format}}")

    def param_to_slider_value(self, param, value):
        return value*SLIDER_MULTIPLIER
