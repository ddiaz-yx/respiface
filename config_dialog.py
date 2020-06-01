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
SLIDER_MULTIPLIER = 1
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
        self.setup_ui()
        self.d_params = None
        self.frm_aceptar.mousePressEvent = partial(self.frm_aceptar_pressed)
        self.frm_cancelar.mousePressEvent = partial(self.frm_cancelar_pressed)
        self.frm_volver.mousePressEvent = partial(self.frm_volver_pressed)
        self.uncommited_change = False  # flag para indica que se cambió el valor de un parámetro, pero no se ha guardado
        self.frm_param_op_mode_pcv.mousePressEvent = partial(self.frm_param_op_mode_pcv_pressed)
        self.frm_param_op_mode_vcv.mousePressEvent = partial(self.frm_param_op_mode_vcv_pressed)

        self.set_labels()

    def set_styles(self):
        self.line.hide()
        self.setStyleSheet("background-color: " + st.BLACK + "; color: lightgrey;")
        self.frm_op_mode.setStyleSheet(st.qss_frm_group)
        self.frm_buttons.setStyleSheet(st.qss_frm_group)
        self.frm_values.setStyleSheet(st.qss_frm_group)
        self.lbl_title_op_mode.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_basic_params.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.lbl_title_right.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.frm_aceptar.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_cancelar.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_volver.setStyleSheet(st.qss_frm_but_enabled)
        self.frm_left_arrow.setStyleSheet(st.qss_frm_top)
        self.frm_right_arrow.setStyleSheet(st.qss_frm_top)
        self.frm_left_arrow_2.setStyleSheet(st.qss_frm_top)
        self.frm_right_arrow_2.setStyleSheet(st.qss_frm_top)
        self.frm_param_op_mode_pcv.hide()
        self.frm_param_op_mode_simv.hide()
        frames = self.findChildren(QFrame)
        for f in frames:
            if f.objectName().startswith('frm_param_'):
                f.setStyleSheet(st.qss_frm_top)

    def set_labels(self):
        # Pone los valores actuales en los labels
        if self.params['mode'].value == OpModEnum.vcv.value:
            self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_selected)
            self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_top)
        elif self.params['mode'].value == OpModEnum.pcv.value:
            self.frm_param_op_mode_pcv.setStyleSheet(st.qss_frm_selected)
            self.frm_param_op_mode_vcv.setStyleSheet(st.qss_frm_top)

        for name, param in self.params.items():
            if name in (ParamEnum.ier_i.name, ParamEnum.ier_e.name):
                continue
            frame_name = "frm_param_" + name
            f = self.findChild(QFrame, name=frame_name)
            if f:
                self.get_value_label(f).setText(f"{param.value:{param.value_format}}")

        # ier
        ier_i = self.params[ParamEnum.ier_i.name]
        ier_e = self.params[ParamEnum.ier_e.name]
        f = self.findChild(QFrame, name="frm_param_ier")
        if f:
            self.get_value_label(f).setText(f"{ier_i.value:{ier_i.value_format}}:{ier_e.value:{ier_e.value_format}}")

    def setup_ui(self):
        try:
            self.horizontalSlider.valueChanged.disconnect()
        except TypeError:
            pass
        try:
            self.horizontalSlider_2.valueChanged.disconnect()
        except TypeError:
            pass

        if self.selected_param is None:
            self.frm_left_arrow.hide()
            self.frm_right_arrow.hide()
            self.horizontalSlider.hide()
            self.frm_left_arrow_2.hide()
            self.frm_right_arrow_2.hide()
            self.horizontalSlider_2.hide()
            self.frm_volver.setEnabled(True)
            self.frm_volver.setStyleSheet(st.qss_frm_but_enabled)
            self.frm_aceptar.setDisabled(True)
            self.frm_aceptar.setStyleSheet(st.qss_frm_but_disbled)
            self.frm_cancelar.setDisabled(True)
            self.frm_cancelar.setStyleSheet(st.qss_frm_but_disbled)
            self.frm_op_mode.setEnabled(True)
            self.frm_left_arrow.setEnabled(False)
            self.frm_right_arrow.setEnabled(False)
            self.horizontalSlider.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
        else:
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
            self.frm_left_arrow.setEnabled(True)
            self.frm_right_arrow.setEnabled(True)
            self.horizontalSlider.setEnabled(True)

            if self.selected_param == ParamEnum.ier.name:
                ier_i_param = self.params[ParamEnum.ier_i.name]
                ier_e_param = self.params[ParamEnum.ier_e.name]
                self.horizontalSlider_2.setEnabled(True)
                self.horizontalSlider.setMaximum(ier_i_param.value_max * SLIDER_MULTIPLIER)
                self.horizontalSlider.setMinimum(ier_i_param.value_min * SLIDER_MULTIPLIER)
                self.horizontalSlider.setSingleStep(1)
                self.horizontalSlider_2.setMaximum(ier_e_param.value_max * SLIDER_MULTIPLIER)
                self.horizontalSlider_2.setMinimum(ier_e_param.value_min * SLIDER_MULTIPLIER)
                self.horizontalSlider_2.setSingleStep(1)
                self.frm_left_arrow_2.show()
                self.frm_right_arrow_2.show()
                self.horizontalSlider_2.show()
            else:
                param = self.params[self.selected_param]
                self.horizontalSlider.setMaximum(param.value_max * SLIDER_MULTIPLIER)
                self.horizontalSlider.setMinimum(param.value_min * SLIDER_MULTIPLIER)
                self.horizontalSlider.setSingleStep(1)
                self.frm_left_arrow_2.hide()
                self.frm_right_arrow_2.hide()
                self.horizontalSlider_2.hide()

            self.horizontalSlider.valueChanged.connect(self.slider_value_changed)
            self.frm_left_arrow.mousePressEvent = partial(self.frm_left_arrow_pressed)
            self.frm_right_arrow.mousePressEvent = partial(self.frm_right_arrow_pressed)
            if self.selected_param == ParamEnum.ier.name:
                self.horizontalSlider_2.valueChanged.connect(self.slider_2_value_changed)
                self.frm_left_arrow_2.mousePressEvent = partial(self.frm_left_arrow_2_pressed)
                self.frm_right_arrow_2.mousePressEvent = partial(self.frm_right_arrow_2_pressed)

    def update_ui(self):
        if self.selected_param == ParamEnum.ier.name:
            param = self.params[ParamEnum.ier_i.name]
        else:
            param = self.params[self.selected_param]
        step = param.value_step
        val = self.d_params[param.name]['value']
        if val + step > param.value_max + EPS:
            self.frm_right_arrow.setEnabled(False)
        if val - step > param.value_min - EPS:
            self.frm_left_arrow.setEnabled(True)
        if val - step < param.value_min - EPS:
            self.frm_left_arrow.setEnabled(False)
        if val + step < param.value_max + EPS:
            self.frm_right_arrow.setEnabled(True)

        if self.selected_param == ParamEnum.ier.name:
            param = self.params[ParamEnum.ier_e.name]
            step = param.value_step
            val2 = self.d_params[ParamEnum.ier_e.name]['value']
            if val2 + step > param.value_max + EPS:
                self.frm_right_arrow_2.setEnabled(False)
            if val2 - step > param.value_min - EPS:
                self.frm_left_arrow_2.setEnabled(True)
            if val2 - step < param.value_min - EPS:
                self.frm_left_arrow_2.setEnabled(False)
            if val2 + step < param.value_max + EPS:
                self.frm_right_arrow_2.setEnabled(True)

        for name, param in self.d_params.items():
            # update affected params values
            if param['dependent']:
                param['value'] = Parameter.calculate_param(name, self.d_params, self.params)

            frame_name = "frm_param_" + name
            f = self.findChild(QFrame, name=frame_name)
            if f:
                label = self.get_value_label(f)
                label.setText(f"{param['value']:{self.params[name].value_format}}")

        label = self.get_value_label(self.selected_param_frame)
        if self.selected_param == ParamEnum.ier.name:
            ier_i_param = self.params[ParamEnum.ier_i.name]
            ier_e_param = self.params[ParamEnum.ier_e.name]
            val2 = self.d_params[ParamEnum.ier_e.name]['value']
            label.setText(f"{val:{ier_i_param.value_format}}:{val2:{ier_e_param.value_format}}")
        else:
            param = self.params[self.selected_param]
            label.setText(f"{val:{param.value_format}}")

    def update_slider(self, slider, value, valueChangedCallback):
        try:
            slider.valueChanged.disconnect()
        except TypeError:
            pass
        slider.setValue(self.param_to_slider_value(value))
        slider.valueChanged.connect(valueChangedCallback)

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
            self.set_labels()
            self.selected_param_frame.setStyleSheet(st.qss_frm_top)
            self.unselect_child_frames(self.selected_param_frame.parent())
            self.selected_param = None
            self.selected_param_frame = None
        self.setup_ui()
        self.uncommited_change = False

    def frm_volver_pressed(self, event: QMouseEvent):
        dlg = ConfirmDialog(parent=self.frm_main)
        if dlg.exec_():
            self.accept()
        else:
            self.reject()

    def slider_value_changed(self, val):
        if self.selected_param == ParamEnum.ier.name:
            param = self.params[ParamEnum.ier_i.name]
        else:
            param = self.params[self.selected_param]
        self.d_params[param.name]['value'] = self.slider_to_param_value(self.horizontalSlider, param)
        self.update_ui()
        self.uncommited_change = True

    def frm_left_arrow_pressed(self, event: QMouseEvent):
        if self.selected_param == ParamEnum.ier.name:
            param = self.params[ParamEnum.ier_i.name]
        else:
            param = self.params[self.selected_param]
        step = param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.d_params[param.name]['value'] -= step
        self.update_ui()
        self.update_slider(self.horizontalSlider, self.d_params[param.name]['value'], self.slider_value_changed)
        self.uncommited_change = True

    def frm_right_arrow_pressed(self, event: QMouseEvent):
        if self.selected_param == ParamEnum.ier.name:
            param = self.params[ParamEnum.ier_i.name]
        else:
            param = self.params[self.selected_param]
        step = param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.d_params[param.name]['value'] += step
        self.update_ui()
        self.update_slider(self.horizontalSlider, self.d_params[param.name]['value'], self.slider_value_changed)
        self.uncommited_change = True

    def slider_2_value_changed(self, val):
        param = self.params[ParamEnum.ier_e.name]
        self.d_params[ParamEnum.ier_e.name]['value'] = self.slider_to_param_value(self.horizontalSlider_2, param)
        self.update_ui()
        self.uncommited_change = True

    def frm_left_arrow_2_pressed(self, event: QMouseEvent):
        param = self.params[ParamEnum.ier_e.name]
        step = param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.d_params[ParamEnum.ier_e.name]['value'] -= step
        self.update_ui()
        self.update_slider(self.horizontalSlider_2, self.d_params[ParamEnum.ier_e.name]['value'], self.slider_2_value_changed)
        self.uncommited_change = True

    def frm_right_arrow_2_pressed(self, event: QMouseEvent):
        param = self.params[ParamEnum.ier_e.name]
        step = param.value_step
        str_value = self.get_value_label(self.selected_param_frame).text()
        self.d_params[ParamEnum.ier_e.name]['value'] += step
        self.update_ui()
        self.update_slider(self.horizontalSlider_2, self.d_params[ParamEnum.ier_e.name]['value'], self.slider_2_value_changed)
        self.uncommited_change = True

    def confirm_param(self):
        for name, param in self.d_params.items():
            self.params[name].value = param['value']
        self.selected_param_frame.setStyleSheet(st.qss_frm_top)
        self.unselect_child_frames(self.selected_param_frame.parent())
        self.selected_param = None
        self.selected_param_frame = None
        self.setup_ui()
        self.uncommited_change = False
        self.set_labels()

    def frame_pressed(self, frame: QFrame, event: QMouseEvent):
        if frame.parent().objectName() == "frm_values":
            if frame == self.selected_param_frame:  # Confirma el parámetro
                self.confirm_param()
                return
            elif not self.uncommited_change:
                self.unselect_child_frames(frame.parent())
                frame.setStyleSheet(st.qss_frm_selected)
                param_name = frame.objectName().replace("frm_param_", "")

                self.selected_param = param_name
                self.selected_param_frame = frame
                self.d_params = {}

                if param_name == ParamEnum.ier.name:
                    self.d_params[ParamEnum.ier_i.name] = {'value': self.params[ParamEnum.ier_i.name].value, 'dependent': False}
                    self.d_params[ParamEnum.ier_e.name] = {'value': self.params[ParamEnum.ier_e.name].value, 'dependent': False}
                    dep1 = Parameter.get_dependents(self.params[ParamEnum.ier_i.name], self.params[ParamEnum.mode.name].value)
                    dep2 = Parameter.get_dependents(self.params[ParamEnum.ier_e.name], self.params[ParamEnum.mode.name].value)
                    dependents = dep1 + list(set(dep2) - set(dep1))
                else:
                    self.d_params[param_name] = {'value': self.params[param_name].value, 'dependent': False}
                    dependents = Parameter.get_dependents(self.params[param_name], self.params[ParamEnum.mode.name].value)

                for dep in dependents:
                    self.d_params[dep] = {'value': self.params[dep].value, 'dependent': True}
                    frame_name = "frm_param_" + dep
                    f = self.findChild(QFrame, name=frame_name)
                    if f:
                        f.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)

                self.setup_ui()
                self.update_ui()
                if param_name == ParamEnum.ier.name:
                    self.update_slider(self.horizontalSlider, self.d_params[ParamEnum.ier_i.name]['value'], self.slider_value_changed)
                    self.update_slider(self.horizontalSlider_2, self.d_params[ParamEnum.ier_e.name]['value'], self.slider_2_value_changed)
                else:
                    self.update_slider(self.horizontalSlider, self.d_params[param_name]['value'], self.slider_value_changed)
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

    def slider_to_param_value(self, slider, param):
        val = slider.value()/SLIDER_MULTIPLIER
        return val - (val%param.value_step)# float(f"{val:{param.value_format}}")

    def param_to_slider_value(self, value):
        return value*SLIDER_MULTIPLIER
