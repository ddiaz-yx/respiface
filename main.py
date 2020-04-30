import sys
from functools import partial
from threading import Thread
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPixmap, QColor
from PyQt5.QtWidgets import QLabel, QFrame, QMessageBox, QSplashScreen, QDialog
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView
import copy
from config_dialog import ConfigDialog
from param_dialog import ParamSetDialog
from ui_main_window import Ui_MainWindow
import yaml
from parameter import Parameter, ParamEnum
from collections import deque
from data_proxy import DataProxy
import time

CONFIG_FILE = "config.yaml"
COLOR_PRESSURE = "FFC107" # "EEEE88"
COLOR_FLOW = "00AA33" # "44FF88"
MAX_DATA_POINTS = 3000  # 60 segundos a 50 Hz
UNDER_CURVE_ALPHA = "88"

top_frames_style = '''QFrame{
                        background: #DDDDDD;
                    }
                    QLabel{
                        color: black;
                    }'''

grey_frame_style = '''QFrame{
                        background: lightgrey;
                    }
                    QLabel{
                        color: black;
                    }'''


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.dq_cp = deque([], MAX_DATA_POINTS)
        self.dq_cf = deque([], MAX_DATA_POINTS)
        self.dq_tf = deque([], MAX_DATA_POINTS)
        self.dq_user_set_param = deque()  # cola de parametros seteados por usuario, por enviar al controlador
        self.params = dict()  # Dict[str, Parameter]
        self.read_config()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("QMainWindow {background-color: white};")
        self.plot_update_timer = QtCore.QTimer()
        self.test_timer = QtCore.QTimer()

        self.gscale_options = (5, 20, 60)
        self.gscale_idx = 0             # Indice de gscale options
        self.gtime_ini = time.time()    # Marca el inicio de la ventana de gráficos

        self.set_styles()
        self.set_up_plots()

        self.frm_peep.mousePressEvent = partial(self.adjust_param, ParamEnum.peep)
        self.frm_fio2.mousePressEvent = partial(self.adjust_param, ParamEnum.fio2, )
        self.frm_flujototal.mousePressEvent = partial(self.adjust_param, ParamEnum.flujoaire, )
        self.frm_ratioie.mousePressEvent = partial(self.adjust_param, ParamEnum.ier, )
        self.frm_rpm.mousePressEvent = partial(self.adjust_param, ParamEnum.brpm, )
        self.frm_vtidal.mousePressEvent = partial(self.adjust_param, ParamEnum.tvm, )
        self.frm_gscale.mousePressEvent = partial(self.new_scale)

        self.plot_update_timer.timeout.connect(self.draw_plots)
        self.plot_update_timer.start(0)

        self.proxy = DataProxy(self.dq_cp, self.dq_cf, self.dq_tf, self.dq_user_set_param)
        self.proxy.start()

        self.dialog_set_param = ParamSetDialog(self.centralwidget)
        self.dialog_set_param.hide()

        self.splash = QDialog(self)
        self.splash.setStyleSheet("background-color: black;")
        self.splash.setModal(True)
        self.splash.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.splash.setGeometry(0, 0, 800, 480)

        self.splash.close() # En producción reemplazar por .show()

        # Signals and slots
        self.btnConfig.pressed.connect(self.btnConfig_pressed)
        self.proxy.signal_params_properties_set.connect(self.set_params_properties_from_controller)
        self.proxy.signal_new_param_values.connect(self.update_param_value_from_controller)

    def update_param_value_from_controller(self, params_: dict):
        '''
        Recibe los valore desde el controlador
        '''
        for name, prm in params_.items():
            if 'ier' not in name:
                try:
                    self.params[name].value = prm.value
                except KeyError as e:
                    print("Received config for unknown parameter: " + str(e))

        #Caso especial de ier
        if 'ier_i' in params_.keys() and 'ier_e' in params_.keys():
            self.params['ier'].value = (params_['ier_i'].value, params_['ier_e'].value)

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

        #Caso especial de ier
        self.params['ier'].value_min = (params_['ier_i'].value_min, params_['ier_e'].value_min)
        self.params['ier'].value_max = (params_['ier_i'].value_max, params_['ier_e'].value_max)
        self.params['ier'].value_default = (params_['ier_i'].value_default, params_['ier_e'].value_default)

        self.splash.hide()
        del self.splash

    def set_styles(self):
        self.frm_fio2.setStyleSheet(top_frames_style)
        self.frm_flujototal.setStyleSheet(top_frames_style)
        self.frm_peep.setStyleSheet(top_frames_style)
        self.frm_pmax.setStyleSheet(top_frames_style)
        self.frm_pmedia.setStyleSheet(top_frames_style)
        self.frm_ratioie.setStyleSheet(top_frames_style)
        self.frm_rpm.setStyleSheet(top_frames_style)
        self.frm_vtidal.setStyleSheet(top_frames_style)
        self.frm_op_mode.setStyleSheet(top_frames_style)
        self.frm_gscale.setStyleSheet(grey_frame_style)

    def set_up_plots(self):
        # TODO: deshabilitar botones por completo (no solamente el ajuste en los ejes)
        # PRESION -----------------------------------------------

        self.lbl_plot_top_title.setStyleSheet('QLabel{color: #' + COLOR_PRESSURE + '}')
        self.lbl_plot_top_title.setText("Presión [cm H2O]")
        self.p_widget.layout.setContentsMargins(0, 0, 0, 0)
        self.view_pressure = RemoteGraphicsView()
        self.p_widget.addWidget(self.view_pressure)
        self.plt_pressure: pg.PlotItem = self.view_pressure.pg.PlotItem(clipToView=True)
        self.plt_pressure.hideButtons()
        self.plt_pressure.setMenuEnabled(False)
        self.plt_pressure.setMouseEnabled(x=False, y=False)
        self.plt_pressure.getAxis('bottom').setPen({'color': COLOR_PRESSURE, 'width': 1})
        self.plt_pressure.getAxis('left').setPen({'color': COLOR_PRESSURE, 'width': 1})
        self.plt_pressure.getAxis('bottom').setStyle(showValues=False)
        # Esto funcionó para bajar el uso de CPU.
        # Sin embargo obliga a setear manualmente el rango
        self.plt_pressure.setRange(xRange=[0, 5], yRange=[0, 12], update=True)
        self.plt_pressure._setProxyOptions(deferGetattr=True)
        self.view_pressure.setCentralItem(self.plt_pressure)
        self.layout_pressure.addWidget(self.view_pressure)
        self.p_curve_lead = self.plt_pressure.plot([-10], [0], pen={'color': COLOR_PRESSURE, 'width': 1.5},
                                                   fillLevel=-0.5, brush=COLOR_PRESSURE+UNDER_CURVE_ALPHA)
        self.p_curve_trail = self.plt_pressure.plot([-10], [0], pen={'color': COLOR_PRESSURE, 'width': 1},
                                                    fillLevel=-0.5, brush=COLOR_PRESSURE+UNDER_CURVE_ALPHA)
        self.p_line = self.plt_pressure.addLine(y=110.5, pen={'color': COLOR_PRESSURE, 'width': 0.5})

        # FLUJO -----------------------------------------------
        self.lbl_plot_bottom_title.setText("Flujo [L/min]")
        self.lbl_plot_bottom_title.setStyleSheet('QLabel{color: #' + COLOR_FLOW + '}')
        self.f_widget.layout.setContentsMargins(0, 0, 0, 0)
        self.view_flow = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        self.f_widget.addWidget(self.view_flow)
        self.plt_flow: pg.PlotItem = self.view_flow.pg.PlotItem(clipToView=True)
        self.plt_flow.hideButtons()
        self.plt_flow.setMouseEnabled(x=False, y=False)
        self.plt_flow.getAxis('bottom').setPen({'color': COLOR_FLOW, 'width': 1})
        self.plt_flow.getAxis('left').setPen({'color': COLOR_FLOW, 'width': 1})
        # self.plt_flow.getAxis('left').setTicks([-100, 100])
        self.plt_flow.setRange(xRange=[0, 5], yRange=[-2, 2], update=True)
        self.plt_flow._setProxyOptions(deferGetattr=True)
        self.view_flow.setCentralItem(self.plt_flow)
        self.layout_flow.addWidget(self.view_flow)  # Relleno por mientras
        self.f_curve_lead = self.plt_flow.plot([-10], [0], pen={'color': COLOR_FLOW, 'width': 1.5}, fillLevel=-0.5,
                                               brush=COLOR_FLOW+UNDER_CURVE_ALPHA)
        self.f_curve_trail = self.plt_flow.plot([-10], [0], pen={'color': COLOR_FLOW, 'width': 1}, fillLevel=-0.5,
                                                brush=COLOR_FLOW+UNDER_CURVE_ALPHA)
        self.f_line = self.plt_flow.addLine(y=150, pen={'color': COLOR_FLOW, 'width': 0.5})

        self.adjust_gscale()

    def update_param_labels(self):
        for name, p in self.params.items():
            label = self.findChild(QLabel, name="lbl_" + name)
            if label:
                if name == "ier":
                    label.setText(f"{p.value[0]:{p.value_format[0]}}:{p.value[1]:{p.value_format[1]}}")
                else:
                    print(f"Value: {p.value}  Format:{p.value_format}")
                    label.setText(f"{p.value:{p.value_format}}")

    def new_scale(self, event: QMouseEvent):
        self.gscale_idx += 1
        self.gscale_idx %= len(self.gscale_options)
        self.adjust_gscale()

    def adjust_gscale(self):
        span = self.gscale_options[self.gscale_idx]
        self.lbl_gscale.setText(f"{span} s")
        self.gtime_ini = time.time()
        self.plt_pressure.setRange(xRange=[0, span], yRange=[0, 12], update=True, padding=0.03)
        self.plt_flow.setRange(xRange=[0, span], yRange=[-80, 80], update=True, padding=0.03)

    def read_config(self):
        with open(CONFIG_FILE, 'r') as config_file:
            self.cfg = yaml.safe_load(config_file)
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

            min_ = tuple(float(v) for v in min_.split(",")) if (isinstance(min_, str) and "," in min_) else float(min_)
            max_ = tuple(float(v) for v in max_.split(",")) if (isinstance(max_, str) and "," in max_) else float(max_)
            step = tuple(float(v) for v in step.split(",")) if (isinstance(step, str) and "," in step) else float(step)
            default = tuple(float(v) for v in default.split(",")) if (
                    isinstance(default, str) and "," in default) else float(default)
            fmt = tuple(f for f in fmt.split(",")) if "," in fmt else fmt

            self.params[p] = Parameter(name=p, screen_name=screen_name, units=units, min_=min_, max_=max_, step=step,
                                       fmt=fmt, default=default)

    def adjust_param(self, param_: ParamEnum, event: QMouseEvent):
        '''
        Adjustment of single params ( by clicking its frame in the main screen)
        '''
        self.dialog_set_param.set_parameter(self.params[param_.name])
        result = self.dialog_set_param.exec_()
        if result:
            print(f"New value for: {param_.name}: {self.dialog_set_param.value}")
            self.params[param_.name].value = self.dialog_set_param.value    # Setea el valor en variable local
            self.dq_user_set_param.append(self.params[param_.name])         # Envia el nuevo valor al controlador
            self.update_param_labels()

    def btnConfig_pressed(self):
        '''
        Adjust all params in a single screen
        '''
        dialog_cfg = ConfigDialog(params=self.params, parent=self.centralwidget)
        result = dialog_cfg.exec_()
        if result:
            print("Shazooo")
            self.params = copy.deepcopy(dialog_cfg.params)
            self.dq_user_set_param.append(self.params)  # Envia el nuevo valor al controlador
        self.update_param_labels()

    def draw_plots(self):
        t1 = Thread(target=self.draw_top)
        t2 = Thread(target=self.draw_bottom)
        t1.start()
        t2.start()

    def draw_top(self):
        if not len(self.dq_cf):
            return
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(np.array(self.dq_cp), edge_value=-1)
        #self.p_curve_trail.setData(x_trail, y_trail, _callSync='off')
        #self.p_curve_lead.setData(x_lead, y_lead, _callSync='off')
        self.p_curve_lead.setData(np.append(x_lead, x_trail), np.append(y_lead, y_trail), _callSync='off')

    def draw_bottom(self):
        if not len(self.dq_cf):
            return
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(np.array(self.dq_tf), edge_value=0)
        #self.f_curve_trail.setData(x_trail, y_trail, _callSync='off')
        #self.f_curve_lead.setData(x_lead, y_lead, _callSync='off')
        self.f_curve_lead.setData(np.append(x_lead, x_trail), np.append(y_lead, y_trail), _callSync='off')

    def time_arrange_data(self, data, edge_value):
        time_span = self.gscale_options[self.gscale_idx]
        x_lead = data[:, 0] - self.gtime_ini
        y_lead = data[:, 1]
        if x_lead[-1] >= time_span:
            self.gtime_ini = time.time()
        try:
            trail_idx = np.argmax(x_lead > x_lead[-1] - time_span)
            x_trail = x_lead[trail_idx:]
            x_trail = x_trail - x_trail[0] + x_lead[-1] #+ time_span / 100
            y_trail = y_lead[trail_idx:]

            #flancos
            x_lead[-1] = x_lead[-2] + 0.005
            y_lead[-1] = edge_value
            x_trail[0] = x_trail[1] - 0.005
            y_trail[0] = edge_value

        except IndexError:
            x_lead, y_lead, x_trail, y_trail = [], [], [], []
        return x_lead, y_lead, x_trail, y_trail

app = QtWidgets.QApplication(sys.argv)
with open("style.qss", 'r') as style_file:
    app.setStyleSheet(style_file.read())

pg.setConfigOption('antialias', True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

window = MainWindow()
window.show()
app.exec()
