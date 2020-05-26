import sys
from functools import partial
from threading import Thread
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
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
from data_proxy import DataProxy
import time
from pathlib import Path
import logging, logging.config
import styles as st

CONFIG_FILE = "config.yaml"
DATA_REFRESH_FREQ = 50  # 50 Hz
MAX_DATA_POINTS = 60 * DATA_REFRESH_FREQ  # 60 segundos a 50 Hz
MAX_STATS_POINTS = 10
UNDER_CURVE_ALPHA = "55"


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
        self.dq_tf = deque([], MAX_DATA_POINTS)
        self.dq_p_mmax = deque([], MAX_STATS_POINTS)
        self.dq_p_mavg = deque([], MAX_STATS_POINTS)
        self.dq_user_set_param = deque()  # cola de parametros seteados por usuario, por enviar al controlador
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.plot_update_timer = QtCore.QTimer()
        self.mem_check_timer = QtCore.QTimer()

        self.setCursor(Qt.BlankCursor)

        self.gscale_options = (5, 20, 60)
        self.gscale_idx = 0  # Indice de gscale options
        self.gtime_ini = time.time()  # Marca el inicio de la ventana de gráficos

        self.set_styles()
        self.set_up_plots()

        self.frm_peep.mousePressEvent = partial(self.adjust_param, ParamEnum.peep)
        self.frm_fio2.mousePressEvent = partial(self.adjust_param, ParamEnum.fio2, )
        self.frm_tf.mousePressEvent = partial(self.adjust_param, ParamEnum.tf, )
        self.frm_ratioie.mousePressEvent = partial(self.adjust_param, ParamEnum.ier, )
        self.frm_rpm.mousePressEvent = partial(self.adjust_param, ParamEnum.brpm, )
        self.frm_tvm.mousePressEvent = partial(self.adjust_param, ParamEnum.tvm, )
        self.frm_gscale.mousePressEvent = partial(self.new_scale)

        self.plot_update_timer.timeout.connect(self.draw_plots)
        self.plot_update_timer.start(DATA_REFRESH_FREQ)
        # self.mem_check_timer.timeout.connect(lambda : self.logger.info(f"Mem usage: {psutil.Process(os.getpid()).memory_info().rss}"))
        # self.mem_check_timer.start(1000)
        self.proxy = DataProxy(self.dq_cp, self.dq_cf, self.dq_tf, self.dq_p_mmax, self.dq_p_mavg, self.dq_user_set_param)
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
        self.frm_config.mousePressEvent = partial(self.btnConfig_pressed, )
        self.proxy.signal_params_properties_set.connect(self.set_params_properties_from_controller)
        self.proxy.signal_new_param_values.connect(self.update_param_value_from_controller)

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

    def set_styles(self):
        self.setStyleSheet("QMainWindow {background-color: " + st.BLACK + "};")
        self.frm_cpmax.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
        self.frm_cpavg.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
        self.frm_peep.setStyleSheet(st.qss_frm_top + st.qss_lbl_yellow)
        self.frm_fio2.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
        self.frm_tf.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
        self.frm_ratioie.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
        self.frm_rpm.setStyleSheet(st.qss_frm_top + st.qss_lbl_green)
        self.frm_tvm.setStyleSheet(st.qss_frm_top + st.qss_lbl_blue)
        self.frm_op_mode.setStyleSheet(st.qss_frm_top)
        self.frm_gscale.setStyleSheet(st.qss_frm_top)
        self.frm_config.setStyleSheet(st.qss_frm_top)
        self.frm_pant_bloq.setStyleSheet(st.qss_frm_top)
        self.frm_config.setContentsMargins(0, 0, 0, 0)
        self.lbl_config.setPixmap(QPixmap('resources/gear2.png'))

    def set_up_plots(self):
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
            if name == ParamEnum.gscale.name:
                self.gscale_idx = p.value
                self.adjust_gscale()
                continue
            if name in (ParamEnum.ier_i.name, ParamEnum.ier_e.name):
                continue
            label = self.findChild(QLabel, name="lbl_" + name)
            if label:
                label.setText(f"{p.value:{p.value_format}}")

        # ier
        ier_i = self.params[ParamEnum.ier_i.name]
        ier_e = self.params[ParamEnum.ier_e.name]
        label = self.findChild(QLabel, name="lbl_ier")
        if label:
            label.setText(f"{ier_i.value:{ier_i.value_format}}:{ier_e.value:{ier_e.value_format}}")

    def new_scale(self, event: QMouseEvent):
        self.gscale_idx += 1
        self.gscale_idx %= len(self.gscale_options)
        self.adjust_gscale()
        self.params[ParamEnum.gscale.name].value = self.gscale_idx
        self.dq_user_set_param.append(self.params[ParamEnum.gscale.name])

    def adjust_gscale(self):
        span = self.gscale_options[self.gscale_idx]
        self.lbl_gscale.setText(f"{span} s")
        self.gtime_ini = time.time()
        pad = 0.025
        y_max = 20
        self.plt_pressure.setRange(xRange=[0, span + 0.5], yRange=[-pad * y_max, y_max * (1 + pad)], update=True, padding=0)
        y_max = 5
        self.plt_flow.setRange(xRange=[0, span + 0.5], yRange=[-pad * y_max, y_max * (1 + pad)], update=True, padding=0)

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
                                       fmt=fmt, default=default)
            if options is not None:
                self.params[p].options = options
                self.params[p].value_as_index = True

        if ParamEnum.ier.name in self.params.keys():
            options = self.params[ParamEnum.ier.name].options
            self.params[ParamEnum.ier.name].options = tuple((f"{v.split(':')[0].rjust(3)}:{v.split(':')[1].rjust(3)}" for v in options))
            print(self.params[ParamEnum.ier.name].options)

        for m in self.cfg["modes"].keys():
            #TODO
            assert m in list(OpModEnum.__members__)
            self.modes[m] = OpMode(name=m)

        self.params['mode'] = Parameter(name='mode')
        self.params['mode'].value = OpModEnum.vcv.value     #VCV by default upon starting

        self.params[ParamEnum.gscale.name] = Parameter(name=ParamEnum.gscale.name)

    def adjust_param(self, param_: ParamEnum, event: QMouseEvent):
        '''
        Adjustment of single params ( by clicking its frame in the main screen)
        '''
        if param_.name == ParamEnum.ier.name:
            self.dialog_set_param.set_parameter(self.params[ParamEnum.ier_e.name], self.params[ParamEnum.ier_i.name])
        else:
            self.dialog_set_param.set_parameter(self.params[param_.name])
        result = self.dialog_set_param.exec_()
        if result:
            if param_.name == ParamEnum.ier.name:
                self.logger.info(f"New value for: {ParamEnum.ier_i.name}: {self.dialog_set_param.value_i}")
                self.logger.info(f"New value for: {ParamEnum.ier_e.name}: {self.dialog_set_param.value}")
                self.params[ParamEnum.ier_i.name].value = self.dialog_set_param.value_i  # Setea el valor en variable local
                self.params[ParamEnum.ier_e.name].value = self.dialog_set_param.value  # Setea el valor en variable local
                self.dq_user_set_param.append(self.params[ParamEnum.ier_i.name])  # Envia el nuevo valor al controlador
                self.dq_user_set_param.append(self.params[ParamEnum.ier_e.name])  # Envia el nuevo valor al controlador
            else:
                self.logger.info(f"New value for: {param_.name}: {self.dialog_set_param.value}")
                self.params[param_.name].value = self.dialog_set_param.value  # Setea el valor en variable local
                self.dq_user_set_param.append(self.params[param_.name])  # Envia el nuevo valor al controlador
            self.update_param_labels()

    def btnConfig_pressed(self, event: QMouseEvent):
        '''
        Adjust all params in a single screen
        '''
        dialog_cfg = ConfigDialog(params=self.params, parent=self.centralwidget)
        result = dialog_cfg.exec_()
        if result:
            self.params = copy.deepcopy(dialog_cfg.params)
            self.dq_user_set_param.append(self.params)  # Envia el nuevo valor al controlador
            print(f"Modo: {self.params['mode'].value}")
        self.update_param_labels()

    def draw_plots(self):
        t1 = Thread(target=self.draw_top)
        t2 = Thread(target=self.draw_bottom)
        t3 = Thread(target=self.draw_stats)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

    def draw_top(self):
        if not len(self.dq_cf):
            return
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(np.array(self.dq_cp), edge_value=-0.5)
        self.p_curve_trail.setData(x_trail, y_trail, _callSync='off')
        self.p_curve_lead.setData(x_lead, y_lead, _callSync='off')
        # self.p_curve_lead.setData(np.append(x_lead, x_trail), np.append(y_lead, y_trail), _callSync='off')

    def draw_bottom(self):
        if not len(self.dq_cf):
            return
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(np.array(self.dq_cf), edge_value=0)
        self.f_curve_trail.setData(x_trail, y_trail, _callSync='off')
        self.f_curve_lead.setData(x_lead, y_lead, _callSync='off')
        # self.f_curve_lead.setData(np.append(x_lead, x_trail), np.append(y_lead, y_trail), _callSync='off')

    def draw_stats(self):
        if len(self.dq_p_mmax):
            p_mmax_label = self.findChild(QLabel, name="lbl_cpmax")
            p_mmax_label.setText(f"{self.dq_p_mmax.pop():.2f}")
        if len(self.dq_p_mavg):
            p_mavg_label = self.findChild(QLabel, name="lbl_cpavg")
            p_mavg_label.setText(f"{self.dq_p_mavg.pop():.2f}")


    def time_arrange_data(self, data, edge_value):
        time_span = self.gscale_options[self.gscale_idx]
        time_span_points = time_span * DATA_REFRESH_FREQ

        if self.gtime_ini < data[:, 0][0]:
            self.gtime_ini = time.time()

        x_lead = data[:, 0] - self.gtime_ini
        y_lead = data[:, 1]
        if x_lead[-1] >= time_span:
            self.gtime_ini = time.time()
        try:
            if len(x_lead) < time_span_points:
                x_trail, y_trail = [], []
            else:
                trail_idx = len(x_lead) - time_span_points
                x_trail = x_lead[trail_idx:]
                x_trail = x_trail - x_trail[0] + x_lead[-1]  # + time_span / 100
                y_trail = y_lead[trail_idx:]

                # flancos
                x_trail[0] = x_trail[1] - 0.005
                y_trail[0] = edge_value

            # flancos
            x_lead[-1] = x_lead[-2] + 0.005
            y_lead[-1] = edge_value

        except IndexError as e:
            x_lead, y_lead, x_trail, y_trail = [], [], [], []

        return x_lead, y_lead, x_trail, y_trail


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
