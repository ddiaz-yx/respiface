import sys
from functools import partial
from threading import Thread
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QLabel, QFrame, QMessageBox, QSplashScreen, QDialog, QLayout
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView
import copy
from config_dialog import ConfigDialog
from param_dialog import ParamSetDialog
from ui_main_window import Ui_MainWindow
import yaml
from parameter import Parameter, ParamEnum, OpMode, OpModEnum, PLOT_TIME_SCALES
from collections import deque
from data_proxy import DataProxy, DataMessage
import time
from pathlib import Path
import logging, logging.config
import styles as st

CONFIG_FILE = "config.yaml"
DATA_REFRESH_FREQ = 50  # 50 Hz
MAX_DATA_POINTS = 60 * DATA_REFRESH_FREQ + 50 # 60 segundos a 50 Hz
MAX_STATS_POINTS = 10
UNDER_CURVE_ALPHA = "55"
P_MAX_CHANGE_SCALE_THRESHOLD = 0.1
F_MAX_CHANGE_SCALE_THRESHOLD = 0.1
F_MIN_CHANGE_SCALE_THRESHOLD = 0.1


class StyleSheetBlinkingAnimation(object):

	def __init__(self, widget, style1, style2, duration, loop_count=1):
		self._widget = widget
		self._style1 = style1
		self._style2 = style2
		self._initial_loop_count = loop_count
		self.loop_count = loop_count

		state1 = QtCore.QState()
		state2 = QtCore.QState()

		self.timer1 = QtCore.QTimer(state1)
		self.timer1.setInterval(duration)
		self.timer1.setSingleShot(True)
		self.timer2 = QtCore.QTimer(state2)
		self.timer2.setInterval(duration)
		self.timer2.setSingleShot(True)

		state1.entered.connect(self._check_loop_count)
		state1.assignProperty(widget, 'styleSheet', style1)
		state2.entered.connect(self._update_loop_count)
		state2.entered.connect(self.timer2.start)
		state2.assignProperty(widget, 'styleSheet', style2)

		state1.addTransition(self.timer1.timeout, state2)
		state2.addTransition(self.timer2.timeout, state1)

		self.machine = QtCore.QStateMachine()
		self.machine.addState(state1)
		self.machine.addState(state2)
		self.machine.setInitialState(state1)

	def start(self):
		if self.machine.isRunning():
			return
		self.loop_count = self._initial_loop_count
		self.machine.start()

	def stop(self):
		self.timer1.stop()
		self.timer2.stop()
		self.machine.stop()
		self._widget.setStyleSheet(self._style1)

	def _check_loop_count(self):
		if self.loop_count <= 0:
			self.stop()
		else:
			self.timer1.start()

	def _update_loop_count(self):
		self.loop_count -= 1


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, config_, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.plt_pressure = pg.PlotItem(clipToView=True)
		self.plt_flow = pg.PlotItem(clipToView=True)
		self.setupUi(self)
		self.logger = logging.getLogger('gui')
		self.logger.info("\n\n*************Iniciando GUI*******************\n")
		self.params = dict()    # Dict of str:Parameter
		self.modes = dict()     # Dict of str:OpMode
		self.cfg = config_
		self.read_config()
		self.dq_cp = deque([], MAX_DATA_POINTS)
		self.dq_cf = deque([], MAX_DATA_POINTS)
		self.dq_tv = deque([], MAX_DATA_POINTS)
		self.dq_p_max = deque([], MAX_STATS_POINTS)
		self.dq_p_avg = deque([], MAX_STATS_POINTS)
		self.dq_peep = deque([], MAX_STATS_POINTS)
		self.dq_fio2 = deque([], MAX_STATS_POINTS)
		self.dq_f_max = deque([], MAX_STATS_POINTS)
		self.dq_user_set_param = deque()  # cola de parametros seteados por usuario, por enviar al controlador
		self.dq_data_message = deque()
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.plot_update_timer = QtCore.QTimer()
		self.mem_check_timer = QtCore.QTimer()

		self.plots_y_ranges = {
			'pressure': {'min': 0.0, 'max': 1.0, 'min_pos': 1.0, 'max_neg': -1.0},
			'flow': {'min': -1.0, 'max': 1.0, 'min_pos': 1.0, 'max_neg': -1.0}
		}

		self.setCursor(Qt.BlankCursor)

		self.block_button_animation = StyleSheetBlinkingAnimation(self.frm_pant_bloq, st.qss_frm_top + st.qss_frm_selected, st.qss_frm_top, 70, 4)

		self.gscale_options = (5, 20, 60)
		self.gscale_idx = 0  # Indice de gscale options
		self.gtime_ini = time.time()  # Marca el inicio de la ventana de gráficos

		self.set_styles()
		self.set_up_plots()

		self.set_blockable_ui_mouse_press_events()
		self.frm_gscale.mousePressEvent = partial(self.new_scale)
		self.frm_pant_bloq.mousePressEvent = partial(self.toggle_block)

		self.blockable_ui = [self.frm_peep, self.frm_fio2, self.frm_mf, self.frm_ratioie, self.frm_rpm, self.frm_tvm, self.frm_op_mode, self.frm_config, self.frm_start_stop]
		self.blocked = False
		self.running = False

		self.plot_update_timer.timeout.connect(self.draw_plots)
		# self.mem_check_timer.timeout.connect(lambda : self.logger.info(f"Mem usage: {psutil.Process(os.getpid()).memory_info().rss}"))
		# self.mem_check_timer.start(1000)
		self.proxy = DataProxy(self.dq_cp, self.dq_cf, self.dq_tv, self.dq_p_max, self.dq_p_avg, self.dq_peep, self.dq_fio2, self.dq_f_max, self.dq_user_set_param, self.dq_data_message)
		self.proxy.start()

		self.dialog_set_param = ParamSetDialog(self.centralwidget)
		self.dialog_set_param.hide()

		self.splash = QDialog(self)
		self.splash.setStyleSheet("background-color: black;")
		self.splash.setModal(True)
		self.splash.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.splash.setGeometry(0, 0, 800, 480)

		self.splash.close()  # En producción reemplazar por .show()

		# Signals and slots
		self.proxy.signal_params_properties_set.connect(self.set_params_properties_from_controller)
		self.proxy.signal_new_param_values.connect(self.update_param_value_from_controller)
		self.proxy.signal_status_report.connect(self.received_state_report)

	def set_blockable_ui_mouse_press_events(self):
		self.frm_peep.mousePressEvent = partial(self.adjust_param, ParamEnum.peep)
		self.frm_fio2.mousePressEvent = partial(self.adjust_param, ParamEnum.fio2,)
		self.frm_mf.mousePressEvent = partial(self.adjust_param, ParamEnum.mf,)
		self.frm_ratioie.mousePressEvent = partial(self.adjust_param, ParamEnum.ier,)
		self.frm_rpm.mousePressEvent = partial(self.adjust_param, ParamEnum.brpm,)
		self.frm_tvm.mousePressEvent = partial(self.adjust_param, ParamEnum.tvm,)
		self.frm_cpmax.mousePressEvent = partial(self.adjust_param, ParamEnum.mp,)
		self.frm_op_mode.mousePressEvent = partial(self.btnConfig_pressed, )
		self.frm_config.mousePressEvent = partial(self.btnConfig_pressed, )
		self.frm_start_stop.mousePressEvent = partial(self.button_start_stop_pressed)

	def update_param_value_from_controller(self, params_: dict):
		'''
		Recibe los valore desde el controlador
		'''
		for name, prm in params_.items():
			try:
				if name == ParamEnum.gscale.name:
					try:
						val = PLOT_TIME_SCALES.index(prm.value)
					except ValueError as e:
						print("unknown time scale: {}".format(prm.value))
						val = 0
				else:
					val = prm.value
				self.params[name].value = val
			except KeyError as e:
				print("Received config for unknown parameter: " + str(e))

		if 'mode' in params_:
			self.update_adjustable()
		self.update_param_labels()


	def set_params_properties_from_controller(self, params_: dict):
		'''
		Recibe los valore min, max y por defecto desde el controlador
		Recién una vez seteados estos valores, se permite al usuario interactuar
		'''
		for name, prm in params_.items():
			if 'ier' not in name:
				self.params[name].value_min = prm.value_min
				self.params[name].value_max = prm.value_max
				self.params[name].value_default = prm.value_default

		self.splash.hide()
		del self.splash

	def received_state_report(self, running: bool):
		self.running = running
		self.update_running_state()

	def set_styles(self):
		self.setStyleSheet("QMainWindow {background-color: " + st.BLACK + "};")
		self.frm_cpmax.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
		self.frm_cpavg.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
		self.frm_peep.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
		self.frm_fio2.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
		self.frm_mf.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
		self.frm_ratioie.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
		self.frm_rpm.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
		self.frm_tvm.setStyleSheet(st.qss_frm_top + st.qss_lbl_blue)
		self.frm_op_mode.setStyleSheet(st.qss_frm_top)
		self.frm_gscale.setStyleSheet(st.qss_frm_top)
		self.frm_config.setStyleSheet(st.qss_frm_top)
		self.frm_pant_bloq.setStyleSheet(st.qss_frm_top)
		self.frm_config.setContentsMargins(0, 0, 0, 0)
		self.frm_start_stop.setStyleSheet(st.qss_frm_start_button)
		# self.lbl_config.setPixmap(QPixmap('resources/gear2.png'))

	def set_up_plots(self):
		font = QtGui.QFont()
		font.setPointSize(9)

		# PRESION -----------------------------------------------
		self.lbl_plot_top_title.setText("Presión [cm H2O]")
		self.lbl_plot_top_title.setStyleSheet('QLabel{color: ' + st.YELLOW + '}')
		self.p_widget.layout.setContentsMargins(0, 0, 0, 0)  # left=0, top=0, right=0, bottom=0
		view = pg.GraphicsView()
		view.setCentralItem(self.plt_pressure)
		self.p_widget.addWidget(view)
		self.plt_pressure.setRange(xRange=[0, 5], yRange=[0, 15], update=True)
		self.plt_pressure.showGrid(x=True, y=True, alpha=0.3)
		self.plt_pressure.hideButtons()
		self.plt_pressure.setMenuEnabled(False)
		self.plt_pressure.setMouseEnabled(x=False, y=False)
		self.plt_pressure.getAxis('bottom').setPen({'color': st.YELLOW, 'width': 1})
		self.plt_pressure.getAxis('left').setPen({'color': st.YELLOW, 'width': 1})
		self.plt_pressure.getAxis('bottom').setStyle(showValues=False)
		self.plt_pressure.getAxis('left').setFont(font)

		self.p_curve_lead = self.plt_pressure.plot([-10], [0], pen={'color': st.YELLOW, 'width': 1.5},
												   fillLevel=-0.5, brush=st.YELLOW + UNDER_CURVE_ALPHA)
		self.p_curve_trail = self.plt_pressure.plot([-10], [0], pen={'color': st.YELLOW, 'width': 1},
													fillLevel=-0.5, brush=st.YELLOW + UNDER_CURVE_ALPHA)
		self.p_line = self.plt_pressure.addLine(y=110.5, pen={'color': st.YELLOW, 'width': 0.5})

		# FLUJO -----------------------------------------------
		self.lbl_plot_bottom_title.setText("Flujo [L/min]")
		self.lbl_plot_bottom_title.setStyleSheet('QLabel{color: ' + st.GREEN + '}')
		self.f_widget.layout.setContentsMargins(0, 0, 0, 0)
		view_flow = pg.GraphicsView()
		view_flow.setCentralItem(self.plt_flow)
		self.f_widget.addWidget(view_flow)
		self.plt_flow.setRange(xRange=[0, 5], yRange=[0, 5], update=True)
		self.plt_flow.showGrid(x=True, y=True, alpha=0.3)
		self.plt_flow.hideButtons()
		self.plt_flow.setMouseEnabled(x=False, y=False)
		self.plt_flow.getAxis('bottom').setPen({'color': st.GREEN, 'width': 1})
		self.plt_flow.getAxis('left').setPen({'color': st.GREEN, 'width': 1})
		self.plt_pressure.getAxis('left').setFont(font)
		self.plt_pressure.getAxis('bottom').setFont(font)

		self.f_curve_lead = self.plt_flow.plot([-10], [0], pen={'color': st.GREEN, 'width': 1.5}, fillLevel=-0.5,
											   brush=st.GREEN + UNDER_CURVE_ALPHA)
		self.f_curve_trail = self.plt_flow.plot([-10], [0], pen={'color': st.GREEN, 'width': 1}, fillLevel=-0.5,
												brush=st.GREEN + UNDER_CURVE_ALPHA)
		self.f_line = self.plt_flow.addLine(y=150, pen={'color': st.GREEN, 'width': 0.5})

		self.adjust_gscale()

	def update_param_labels(self):
		if self.params['mode'].value == OpModEnum.vcv.value:
			self.lbl_op_mode.setText("VCV")
		elif self.params['mode'].value == OpModEnum.pcv.value:
			self.lbl_op_mode.setText("PCV")

		for name, p in self.params.items():
			if name == ParamEnum.pt.name:
				continue
			if name == ParamEnum.gscale.name:
				self.gscale_idx = p.value
				self.adjust_gscale()
				continue
			if name in (ParamEnum.ier_i.name, ParamEnum.ier_e.name):
				continue
			label = self.findChild(QLabel, name="lbl_" + name)
			if label:
				if p.measured:
					if p.adjustable:
						label.setText(f"{p.units} [{p.value:{p.value_format}}]")
					else:
						label.setText(f"{p.units}")
				else:
					label.setText(f"{p.value:{p.value_format}}")

		# ier
		ier_i = self.params[ParamEnum.ier_i.name]
		ier_e = self.params[ParamEnum.ier_e.name]
		label = self.findChild(QLabel, name="lbl_ier")
		if label:
			label.setText(f"{ier_i.value:{ier_i.value_format}}:{ier_e.value:{ier_e.value_format}}")

	def update_adjustable(self):
		current_mode = OpModEnum(self.params['mode'].value).name
		for name, p in self.params.items():
			if name == 'mode':
				continue
			if name in self.modes[current_mode].adjustable_params:
				p.adjustable = True
			else:
				p.adjustable = False

	def new_scale(self, event: QMouseEvent):
		self.gscale_idx += 1
		self.gscale_idx %= len(self.gscale_options)
		self.adjust_gscale()
		self.params[ParamEnum.gscale.name].value = self.gscale_idx
		self.dq_user_set_param.append([self.params[ParamEnum.gscale.name]])

	def adjust_gscale(self):
		self.gtime_ini = time.time()
		self.set_plots_ranges()

	def set_plots_ranges(self):
		span = self.gscale_options[self.gscale_idx]
		self.lbl_gscale.setText(f"{span} s")
		pad = 0.025
		self.plt_pressure.setRange(xRange=[0, span*1.025], yRange=[-pad * self.plots_y_ranges['pressure']['max'], self.plots_y_ranges['pressure']['max'] * (1 + P_MAX_CHANGE_SCALE_THRESHOLD)], update=True, padding=0)
		self.plt_flow.setRange(xRange=[0, span*1.025], yRange=[(1 + F_MIN_CHANGE_SCALE_THRESHOLD) * self.plots_y_ranges['flow']['min'], self.plots_y_ranges['flow']['max'] * (1 + F_MAX_CHANGE_SCALE_THRESHOLD)], update=True, padding=0)

	def read_config(self):
		self.gscale_options = tuple(self.cfg["gscale"]["options"])
		for p in self.cfg["resp_params"].keys():
			assert p in list(ParamEnum.__members__)
			screen_name = self.cfg["resp_params"][p]["screen_name"]
			min_ = self.cfg["resp_params"][p]["min"]
			max_ = self.cfg["resp_params"][p]["max"]
			fmt = self.cfg["resp_params"][p]["format"]
			step = self.cfg["resp_params"][p]["step"]
			default = self.cfg["resp_params"][p]["default"]
			units = self.cfg["resp_params"][p]["units"]
			measured = self.cfg["resp_params"][p]["measured"]
			options = None
			try:
				options = tuple(self.cfg["resp_params"][p]["options"])
				print(options)
			except KeyError:
				pass

			min_ = tuple(float(v) for v in min_.split(",")) if (isinstance(min_, str) and "," in min_) else float(min_)
			max_ = tuple(float(v) for v in max_.split(",")) if (isinstance(max_, str) and "," in max_) else float(max_)
			step = tuple(float(v) for v in step.split(",")) if (isinstance(step, str) and "," in step) else float(step)
			default = tuple(float(v) for v in default.split(",")) if (
					isinstance(default, str) and "," in default) else float(default)
			fmt = tuple(f for f in fmt.split(",")) if "," in fmt else fmt

			self.params[p] = Parameter(name=p, screen_name=screen_name, units=units, min_=min_, max_=max_, step=step,
									   fmt=fmt, default=default, measured=measured)
			if options is not None:
				self.params[p].options = options
				self.params[p].value_as_index = True

		if ParamEnum.ier.name in self.params.keys():
			options = self.params[ParamEnum.ier.name].options
			self.params[ParamEnum.ier.name].options = tuple((f"{v.split(':')[0].rjust(3)}:{v.split(':')[1].rjust(3)}" for v in options))
			print(self.params[ParamEnum.ier.name].options)

		for m in self.cfg["modes"].keys():
			assert m in list(OpModEnum.__members__)
			self.modes[m] = OpMode(name=m)
			for p in self.cfg['modes'][m].keys():
				if self.cfg['modes'][m][p]['adjustable']:
					self.modes[m].adjustable_params.append(p)

		self.params['mode'] = Parameter(name='mode')
		self.params['mode'].value = OpModEnum.vcv.value     #VCV by default upon starting
		self.update_adjustable()

		self.params[ParamEnum.gscale.name] = Parameter(name=ParamEnum.gscale.name)

	def adjust_param(self, param_: ParamEnum, event: QMouseEvent):
		'''
		Adjustment of single params ( by clicking its frame in the main screen)
		'''
		if param_.name == ParamEnum.ier.name:
			self.dialog_set_param.set_parameter(self.params[ParamEnum.ier_e.name], self.params)
		else:
			if self.params[param_.name].adjustable:
				self.dialog_set_param.set_parameter(self.params[param_.name], self.params)
			else:
				return
		self.plot_update_timer.stop()
		result = self.dialog_set_param.exec_()
		self.plot_update_timer.start()
		if result:
			params = []
			for name, param in self.dialog_set_param.d_params.items():
				self.logger.info(f"New value for: {name}: {param['value']}")
				self.params[name].value = param['value']
				params.append(self.params[name])
			self.dq_user_set_param.append(params)
			self.update_param_labels()

	def btnConfig_pressed(self, event: QMouseEvent):
		'''
		Adjust all params in a single screen
		'''
		self.plot_update_timer.stop()
		dialog_cfg = ConfigDialog(params=self.params, parent=self.centralwidget)
		result = dialog_cfg.exec_()
		self.plot_update_timer.start()
		if result:
			self.params = copy.deepcopy(dialog_cfg.params)
			self.dq_user_set_param.append([p for k, p in self.params.items()])  # Envia el nuevo valor al controlador
			print(f"Modo: {self.params['mode'].value}")
			self.update_adjustable()
			self.set_blockable_ui_mouse_press_events()
		self.update_param_labels()

	def draw_plots(self):
		time_span = self.gscale_options[self.gscale_idx]
		if time.time() - self.gtime_ini >= time_span:
			self.gtime_ini += time_span

		t1 = Thread(target=self.draw_top)
		t2 = Thread(target=self.draw_bottom)
		t3 = Thread(target=self.update_current_labels)
		t1.start()
		t2.start()
		t3.start()
		t1.join()
		t2.join()
		t3.join()

	def draw_top(self):
		if not len(self.dq_cp):
			return
		x_lead, y_lead, x_trail, y_trail, data_min, data_max = self.time_arrange_data(np.array(self.dq_cp))

		if data_max < self.plots_y_ranges['pressure']['min_pos']:
			data_max = self.plots_y_ranges['pressure']['min_pos']
		if P_MAX_CHANGE_SCALE_THRESHOLD <= abs((data_max - self.plots_y_ranges['pressure']['max'])/data_max):
			self.plots_y_ranges['pressure']['max'] = data_max
			self.set_plots_ranges()

		self.p_curve_trail.setData(x_trail, y_trail, _callSync='off')
		self.p_curve_lead.setData(x_lead, y_lead, _callSync='off')

	def draw_bottom(self):
		if not len(self.dq_cf):
			return
		x_lead, y_lead, x_trail, y_trail, data_min, data_max = self.time_arrange_data(np.array(self.dq_cf))

		if data_max < self.plots_y_ranges['flow']['min_pos']:
			data_max = self.plots_y_ranges['flow']['min_pos']
		if data_min > self.plots_y_ranges['flow']['max_neg']:
			data_min = self.plots_y_ranges['flow']['max_neg']
		should_update_ranges = False
		if F_MAX_CHANGE_SCALE_THRESHOLD <= abs((data_max - self.plots_y_ranges['flow']['max']) / data_max):
			self.plots_y_ranges['flow']['max'] = data_max
			should_update_ranges = True
		if F_MIN_CHANGE_SCALE_THRESHOLD <= abs((data_min - self.plots_y_ranges['flow']['min']) / data_min):
			self.plots_y_ranges['flow']['min'] = data_min
			should_update_ranges = True
		if should_update_ranges:
			self.set_plots_ranges()

		self.f_curve_trail.setData(x_trail, y_trail, _callSync='off')
		self.f_curve_lead.setData(x_lead, y_lead, _callSync='off')

	def update_current_labels(self):
		if len(self.dq_p_max):
			p_mmax_label = self.findChild(QLabel, name="lbl_cpmax")
			p_mmax_label.setText(f"{self.dq_p_max.popleft():.2f}")
		if len(self.dq_p_avg):
			p_mavg_label = self.findChild(QLabel, name="lbl_cpavg")
			p_mavg_label.setText(f"{self.dq_p_avg.popleft():.2f}")
		if len(self.dq_peep):
			peep_label = self.findChild(QLabel, name="lbl_current_peep")
			peep_label.setText(f"{self.dq_peep.popleft():.2f}")
		if len(self.dq_f_max):
			cf_label = self.findChild(QLabel, name="lbl_current_fl")
			cf_label.setText(f"{self.dq_f_max.popleft():.0f}")
		if len(self.dq_fio2):
			fio2_label = self.findChild(QLabel, name="lbl_current_fio2")
			fio2_label.setText(f"{self.dq_fio2.popleft():.0f}")
		if len(self.dq_tv):
			tvm_label = self.findChild(QLabel, name="lbl_current_tvm")
			tvm_label.setText(f"{self.dq_tv[-1][1]:.0f}")

	def time_arrange_data(self, data):
		time_span = self.gscale_options[self.gscale_idx]
		time_span_points = time_span * DATA_REFRESH_FREQ

		if self.gtime_ini < data[:, 0][0]:
			self.gtime_ini = time.time()

		x_lead = data[:, 0] - self.gtime_ini
		y_lead = data[:, 1]

		try:
			if x_lead[-1] - x_lead[0] < time_span:
				x_trail, y_trail = [], []
			else:
				trail_idx = np.argmax(x_lead > x_lead[-1] - time_span)
				x_trail = x_lead[trail_idx:]
				x_trail = x_trail + time_span
				y_trail = y_lead[trail_idx:]

				if x_trail[-1] > time_span:
					trail_end = np.argmax(x_trail > time_span)
					x_trail = x_trail[:trail_end]
					y_trail = y_trail[:trail_end]

				gap = int(10 * time_span_points / 1000)
				if gap > len(x_trail):
					gap = len(x_trail)
				x_trail = x_trail[gap:]
				y_trail = y_trail[gap:]

		except IndexError as e:
			x_lead, y_lead, x_trail, y_trail = [], [], [], []

		x_lead_start_idx = np.argmax(x_lead >= 0)
		lead_max = np.max(y_lead[x_lead_start_idx:])
		lead_min = np.min(y_lead[x_lead_start_idx:])
		if len(y_trail) > 0:
			trail_max = np.max(y_trail)
			trail_min = np.min(y_trail)
			data_min = min([lead_min, trail_min])
			data_max = max([lead_max, trail_max])
		else:
			data_min = lead_min
			data_max = lead_max
		return x_lead, y_lead, x_trail, y_trail, data_min, data_max

	def block_button_blink(self, event: QMouseEvent):
		self.block_button_animation.start()

	def toggle_block(self, event: QMouseEvent):
		style = st.qss_frm_top
		self.blocked = not self.blocked
		if self.blocked:
			style += st.qss_frm_selected
			for ui in self.blockable_ui:
				ui.mousePressEvent = partial(self.block_button_blink)
		else:
			self.block_button_animation.stop()
			self.set_blockable_ui_mouse_press_events()
		self.frm_pant_bloq.setStyleSheet(style)

	def update_running_state(self):
		label = self.frm_start_stop.findChild(QLabel)
		if self.running:
			self.gtime_ini = time.time()
			self.plot_update_timer.start(DATA_REFRESH_FREQ)
			self.frm_start_stop.setStyleSheet(st.qss_frm_stop_button)
			if label:
				label.setText("Detener")
		else:
			self.plot_update_timer.stop()
			self.frm_start_stop.setStyleSheet(st.qss_frm_start_button)
			if label:
				label.setText("Comenzar")
			self.dq_cp.clear()
			self.dq_cf.clear()
			self.dq_tv.clear()
			self.dq_p_max.clear()
			self.dq_p_avg.clear()
			self.dq_peep.clear()
			self.dq_fio2.clear()
			self.dq_f_max.clear()

	def button_start_stop_pressed(self, event: QMouseEvent):
		self.running = not self.running
		if self.running:
			self.dq_data_message.append(DataMessage(DataMessage.START))
		else:
			self.dq_data_message.append(DataMessage(DataMessage.STOP))


pg.setConfigOption('antialias', True)
pg.setConfigOption('background', st.BLACK)
pg.setConfigOption('foreground', 'k')
app = QtWidgets.QApplication(sys.argv)
Path('logs').mkdir(exist_ok=True)
with open("style.qss", 'r') as style_file:
	app.setStyleSheet(style_file.read())
with open(CONFIG_FILE, 'r') as config_file:
	config = yaml.load(config_file)
logging.config.dictConfig(config['logging'])
window = MainWindow(config)
window.show()
app.exec()
