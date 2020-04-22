import sys
from functools import partial
from threading import Thread

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView

import data_manager
from config_dialog import ConfigDialog
from param_dialog import ParamSetDialog
from ui_main_window import Ui_MainWindow
import yaml
from parameter import Parameter, ParamEnum
from collections import deque
from dataproxy import DataProxy
import time

CONFIG_FILE = "config.yaml"
COLOR_PRESSURE = "EEEE88"
COLOR_FLOW = "44FF88"
MAX_DATA_POINTS = 3000  # 60 segundos a 50 Hz

top_frames_style = '''QFrame{
    background: #99AABB;
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
    def __init__(self, *args, obj=None, deque_pressure: deque, deque_flow: deque, data_in: deque, data_out: deque,
                 **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.p_deque = deque_pressure
        self.f_deque = deque_flow
        self.params = dict()
        self.read_config()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.dialog_cfg = ConfigDialog(self.params)
        self.setStyleSheet("QMainWindow {background-color: black};")
        self.plot_update_timer = QtCore.QTimer()
        self.test_timer = QtCore.QTimer()

        self.gscale_options = (5, 20, 60)
        self.gscale_idx = 0  # Indice de gscale options
        self.gtime_ini = time.time()  # Marca el inicio de la ventana de gráficos

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

        self.frm_peep.mousePressEvent = partial(self.adjust_param, ParamEnum.peep)
        self.frm_fio2.mousePressEvent = partial(self.adjust_param, ParamEnum.fio2, )
        self.frm_flujototal.mousePressEvent = partial(self.adjust_param, ParamEnum.flujoaire, )
        self.frm_ratioie.mousePressEvent = partial(self.adjust_param, ParamEnum.ier, )
        self.frm_rpm.mousePressEvent = partial(self.adjust_param, ParamEnum.brpm, )
        self.frm_vtidal.mousePressEvent = partial(self.adjust_param, ParamEnum.tvm, )
        self.frm_gscale.mousePressEvent = partial(self.new_scale)

        # PRESION -----------------------------------------------
        self.p_widget.layout.setContentsMargins(0, 0, 0, 0)
        self.view_pressure = RemoteGraphicsView()
        self.p_widget.addWidget(self.view_pressure)
        self.plt_pressure: pg.PlotItem = self.view_pressure.pg.PlotItem(clipToView=True)
        self.plt_pressure.hideButtons()
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
        self.p_curve_lead = self.plt_pressure.plot([-10], [0], pen={'color': COLOR_PRESSURE, 'width': 1.5}, fillLevel=-0.5, brush=(0xEE, 0xEE, 0x88, 50))
        self.p_curve_trail = self.plt_pressure.plot([-10], [0], pen={'color': COLOR_PRESSURE, 'width': 1}, fillLevel=-0.5, brush=(0xEE, 0xEE, 0x88, 20))
        self.p_line = self.plt_pressure.addLine(y=110.5, pen={'color': COLOR_PRESSURE, 'width': 0.5})

        # FLUJO -----------------------------------------------
        self.f_widget.layout.setContentsMargins(0, 0, 0, 0)
        self.view_flow = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        self.f_widget.addWidget(self.view_flow)
        self.plt_flow: pg.PlotItem = self.view_flow.pg.PlotItem(clipToView=True)
        self.plt_flow.hideButtons()
        self.plt_flow.setMouseEnabled(x=False, y=False)
        self.plt_flow.getAxis('bottom').setPen({'color': COLOR_FLOW, 'width': 1})
        self.plt_flow.getAxis('left').setPen({'color': COLOR_FLOW, 'width': 1})
        #self.plt_flow.getAxis('left').setTicks([-100, 100])
        self.plt_flow.setRange(xRange=[0, 5], yRange=[-2, 2], update=True)
        self.plt_flow._setProxyOptions(deferGetattr=True)
        self.view_flow.setCentralItem(self.plt_flow)
        self.layout_flow.addWidget(self.view_flow)  # Relleno por mientras
        self.f_curve_lead = self.plt_flow.plot([-10], [0], pen={'color': COLOR_FLOW, 'width': 1.5}, fillLevel=-0.5, brush=(0x44, 0xFF, 0x88, 50))
        self.f_curve_trail = self.plt_flow.plot([-10], [0], pen={'color': COLOR_FLOW, 'width': 1}, fillLevel=-0.5, brush=(0x44, 0xFF, 0x88, 20))
        self.f_line = self.plt_flow.addLine(y=150, pen={'color': COLOR_FLOW, 'width': 0.5})

        # Refresco ----------------------------------------------
        self.plot_update_timer.start(50)
        self.plot_update_timer.timeout.connect(self.draw_plots)

        self.mgr = data_manager.DataManager(self.p_deque, self.f_deque)
        self.mgr.start()
        self.adjust_gscale()

        self.dialog_set_param = ParamSetDialog(self.centralwidget)
        self.dialog_set_param.hide()

        # Signals and slots
        self.btnConfig.pressed.connect(self.btnConfig_pressed)


    def new_config(self, new_param_dict):
        self.params = new_param_dict
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
        self.mgr.time_span = span
        self.gtime_ini = time.time()
        self.plt_pressure.setRange(xRange=[0, span], yRange=[0, 12], update=True, padding=0.03)
        self.plt_flow.setRange(xRange=[0, span], yRange=[-50, 50], update=True, padding=0.03)

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
                                       format_=fmt, default=default)

    def adjust_param(self, param_: ParamEnum, event: QMouseEvent):
        self.dialog_set_param.set_parameter(self.params[param_.name])
        self.dialog_set_param.show()

    def btnConfig_pressed(self):
        self.dialog_cfg = ConfigDialog(params= self.params, parent=self.centralwidget)
        self.dialog_cfg.done.connect(self.new_config)
        self.dialog_cfg.show()

    def draw_plots(self):
        t1 = Thread(target=self.draw_async)
        t1.start()

    def draw_async(self):
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(self.mgr.get_pressure_data())
        self.p_curve_lead.setData(x_lead, y_lead, _callSync='off')
        self.p_curve_trail.setData(x_trail, y_trail, _callSync='off')
        x_lead, y_lead, x_trail, y_trail = self.time_arrange_data(self.mgr.get_flow_data())
        self.f_curve_lead.setData(x_lead, y_lead, _callSync='off')
        self.f_curve_trail.setData(x_trail, y_trail, _callSync='off')

    def time_arrange_data(self, data):
        time_span = self.gscale_options[self.gscale_idx]
        x_lead = data[:, 0] - self.gtime_ini
        y_lead = data[:, 1]
        if x_lead[-1] >= time_span:
            self.gtime_ini = time.time()

        trail_idx = np.argmax(x_lead > x_lead[-1]-time_span)
        x_trail = x_lead[trail_idx:]
        x_trail = x_trail - x_trail[0] + x_lead[-1] + time_span/90
        y_trail = y_lead[trail_idx:]

        return x_lead, y_lead, x_trail, y_trail

app = QtWidgets.QApplication(sys.argv)
with open("style.qss", 'r') as style_file:
    app.setStyleSheet(style_file.read());
pg.setConfigOption('antialias', True)

deque_pressure = deque([], MAX_DATA_POINTS)  # deque de listas [timestamp, valor] en direccion socket -> pantalla
deque_flow = deque([], MAX_DATA_POINTS)  # deque de tuplas [timestamp, valor] en direccion socket -> pantalla
data_in = deque([], MAX_DATA_POINTS)  # deque de objetos data_dict en dirección pantalla -> socket.
data_out = deque([], MAX_DATA_POINTS)  # deque de objetos data_dict en dirección socket -> pantalla

proxy = DataProxy("/tmp/my_socket", deque_pressure, deque_flow, data_in, data_out)
proxy.start()
window = MainWindow(deque_pressure=deque_pressure, deque_flow=deque_flow, data_in=data_in, data_out=data_out)
window.show()
app.exec()
