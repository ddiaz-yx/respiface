"""
Sublcase de QDialog que modifica aspectos de estilo únicamente

"""
from PyQt5.QtGui import QFont

from ui_param_set import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QGroupBox, QLabel
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import QEvent
from parameter import Parameter, ParamEnum, OpModEnum
import copy

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
		self.btn_confirmar.pressed.connect(self.btn_confirmar_pressed)
		self.lbl_param_value.setFont(QFont('Arial', DEFAULT_VALUE_FONT_SIZE))
		self.btn_up.pressed.connect(self.btn_up_pressed)
		self.btn_down.pressed.connect(self.btn_down_pressed)
		self.btn_up_left.pressed.connect(self.btn_up_left_pressed)
		self.btn_down_left.pressed.connect(self.btn_down_left_pressed)

		self.param: Parameter = None
		self.param2: Parameter = None
		self.params = None
		self.d_params = None
		self.affected_params = None

		self.format = ""
		self.value_max = 0
		self.value_min = 0
		self.step = 1

		self.format_i = ""  # para el caso de I:E
		self.value_i_max = 0  # para el caso de I:E
		self.value_i_min = 0  # para el caso de I:E
		self.step_i = 1

	def set_parameter(self, p: Parameter, params):
		self.param = p
		self.params = copy.deepcopy(params)
		self.affected_params = []
		self.d_params = {}
		if p.units:
			self.lbl_param_name.setText(self.param.screen_name + " [" + p.units + "]")
		else:
			self.lbl_param_name.setText(self.param.screen_name)
		print(self.param.name)

		if self.param.name in (ParamEnum.ier_e.name, ParamEnum.brpm.name):
			self.grp_times.show()
			if params['mode'].value == OpModEnum.vcv.value:
				self.lbl_flowt_title.show()
				self.lbl_flowt.show()
				self.lbl_ptt_title.show()
				self.lbl_ptt.show()
			else:
				self.lbl_flowt_title.hide()
				self.lbl_flowt.hide()
				self.lbl_ptt_title.hide()
				self.lbl_ptt.hide()
		else:
			self.grp_times.hide()

		if self.param.name == ParamEnum.ier_e.name:
			self.param2 = self.params[ParamEnum.ier_i.name]

			self.format = self.param.value_format
			self.value_max = self.param.value_max
			self.value_min = self.param.value_min
			self.step = self.param.value_step

			self.format_i = self.param2.value_format
			self.value_i_max = self.param2.value_max
			self.value_i_min = self.param2.value_min
			self.step_i = self.param2.value_step

			self.d_params[ParamEnum.ier_i.name] = {'value': self.param2.value, 'dependent': False}
			self.d_params[ParamEnum.ier_e.name] = {'value': self.param.value, 'dependent': False}

			self.horizontalSlider.hide()
			self.horizontalSlider.setEnabled(False)
			self.btn_down_left.show()
			self.btn_up_left.show()
			self.lbl_max.hide()
			self.lbl_min.hide()
			self.lbl_param_value.setFont(QFont('Arial', IE_VALUE_FONT_SIZE))

			dep1 = Parameter.get_dependents(self.param2, self.params[ParamEnum.mode.name].value)
			dep2 = Parameter.get_dependents(self.param, self.params[ParamEnum.mode.name].value)
			dependents = dep1 + list(set(dep2) - set(dep1))
		else:
			self.format = self.param.value_format
			self.value_max = self.param.value_max
			self.value_min = self.param.value_min
			self.step = self.param.value_step

			self.d_params[self.param.name] = {'value': self.param.value, 'dependent': False}

			self.btn_down_left.hide()
			self.btn_up_left.hide()
			self.horizontalSlider.setMaximum(self.param.value_max)
			self.horizontalSlider.setMinimum(self.param.value_min)
			self.horizontalSlider.setValue(self.param.value)
			self.horizontalSlider.setSingleStep(self.param.value_step)
			self.horizontalSlider.setEnabled(True)
			self.horizontalSlider.show()
			self.horizontalSlider.valueChanged.connect(self.slider_value_changed)
			self.lbl_max.setText(f"{self.param.value_max:{self.param.value_format}}")
			self.lbl_min.setText(f"{self.param.value_min:{self.param.value_format}}")
			self.lbl_max.show()
			self.lbl_min.show()
			self.lbl_param_value.setFont(QFont('Arial', DEFAULT_VALUE_FONT_SIZE))

			dependents = Parameter.get_dependents(self.param, self.params[ParamEnum.mode.name].value)

		for dep in dependents:
			self.d_params[dep] = {'value': self.params[dep].value, 'dependent': True}

		group = self.findChild(QGroupBox, name="grp_affected_params")
		if group:
			if len(dependents):
					group.setVisible(True)
					for idx, dep in enumerate(dependents):
						param = self.params[dep]
						self.affected_params.append(param)
						lbl_name = group.findChild(QLabel, name="lbl_aff_param_name_{}".format(idx + 1))
						lbl_value = group.findChild(QLabel, name="lbl_aff_param_value_{}".format(idx + 1))
						if lbl_name and lbl_value:
							if len(param.units) > 0:
								lbl_name.setText("{} [{}]".format(param.screen_name, param.units))
							else:
								lbl_name.setText("{}".format(param.screen_name))
							lbl_value.setText("{:.2f}".format(param.value))
			else:
				group.setVisible(False)

		self.update_ui()
		print(f"Param: {self.param.name}")
		print(f" format: {self.format}")
		print(f" value_min: {self.value_min}")
		print(f" value_max: {self.value_max}")
		print(f" step: {self.step}")

	def update_ie_times(self):
		it, et, ft, ptt = Parameter.calculate_ie_times(self.d_params, self.params)
		lbl_it = self.findChild(QLabel, name='lbl_it')
		lbl_et = self.findChild(QLabel, name='lbl_et')
		lbl_ft = self.findChild(QLabel, name='lbl_flowt')
		lbl_ptt = self.findChild(QLabel, name='lbl_ptt')
		lbl_it.setText(f"{it:.1f}")
		lbl_et.setText(f"{et:.1f}")
		lbl_ft.setText(f"{ft:.1f}")
		lbl_ptt.setText(f"{ptt:.1f}")

	def update_ui(self):
		val = self.d_params[self.param.name]['value']
		if self.param.name == ParamEnum.ier_e.name:
			val2 = self.d_params[self.param2.name]['value']
			self.lbl_param_value.setText(f"{val2:{self.format_i}}:{val:{self.format}}")
			if val2 > self.value_i_max - self.step_i:
				self.btn_up_left.setDisabled(True)
			else:
				self.btn_up_left.setDisabled(False)
			if val2 < self.value_i_min + self.step_i:
				self.btn_down_left.setDisabled(True)
			else:
				self.btn_down_left.setDisabled(False)
		else:
			self.lbl_param_value.setText(f"{val:{self.format}}")

		if val > self.value_max - self.step:
			self.btn_up.setDisabled(True)
		else:
			self.btn_up.setDisabled(False)
		if val < self.value_min + self.step:
			self.btn_down.setDisabled(True)
		else:
			self.btn_down.setDisabled(False)

		if self.affected_params:
			# update affected params values
			for name, param in self.d_params.items():
				# update affected params values
				if param['dependent']:
					param['value'] = Parameter.calculate_param(name, self.d_params, self.params)

			# show updated values
			for idx, p in enumerate(self.affected_params):
				lbl_value = self.findChild(QLabel, name="lbl_aff_param_value_{}".format(idx + 1))
				lbl_value.setText("{:.2f}".format(self.d_params[p.name]['value']))

		self.update_ie_times()

	def update_slider(self):
		try:
			self.horizontalSlider.valueChanged.disconnect()
		except TypeError:
			pass
		self.horizontalSlider.setValue(self.d_params[self.param.name]['value'])
		self.horizontalSlider.valueChanged.connect(self.slider_value_changed)

	def slider_value_changed(self, val):
		self.d_params[self.param.name]['value'] = val - (val%self.step)
		self.update_ui()

	def btn_up_pressed(self):
		self.d_params[self.param.name]['value'] += self.step
		self.update_ui()
		self.update_slider()

	def btn_down_pressed(self):
		self.d_params[self.param.name]['value'] -= self.step
		self.update_ui()
		self.update_slider()

	def btn_up_left_pressed(self):
		self.d_params[self.param2.name]['value'] += self.step_i
		self.update_ui()

	def btn_down_left_pressed(self):
		self.d_params[self.param2.name]['value'] -= self.step_i
		self.update_ui()

	def btn_anular_pressed(self):
		self.reject()

	def btn_confirmar_pressed(self):
		self.accept()