"""
El objetivo de la clase DataManager es ser de intermediario pincipal entre los datos desplegados
en pantalla e ingresados en ella y las entradas/salidas de datos por los puertos UART y SPI
"""
import time
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from enum import Enum, auto
import numpy as np
from collections import namedtuple, deque

MAX_DATA_POINTS = 3000  # 60 segundos a 50 Hz


class OpMode(Enum):
    VCV = auto()


class DataManager(QThread):
    testsignal = pyqtSignal(str)

    def __init__(self, p_deque: deque, f_deque: deque):
        QThread.__init__(self)
        self.p_deque_in = p_deque  # data desde afuera
        self.f_deque_in = f_deque  # data desde afuera
        '''
        # Implementación con deque
        self._p_deque = deque()  # para almacenamiento local
        self._f_deque = deque()  # para almacenamiento local
        '''
        self._pressure_data_idx = 0
        self._flow_data_idx = 0
        self.pressure_data = np.zeros((MAX_DATA_POINTS, 2))
        self.flow_data = np.zeros((MAX_DATA_POINTS, 2))
        self.p_max = 0
        self.p_mean = 0
        self.peep = 0
        self.ie_ratio = 3.3
        self.rpm = 20
        self.v_tidal = 500
        self.total_flow = 20
        self.fio2 = 50
        self.operation_mode = OpMode.VCV
        self.time_span = 20
        self.t0 = time.time()

    def update_pressure_data(self):
        # Implementación con cola circular
        data_point = self.p_deque_in.popleft()
        self._pressure_data_idx += 1
        self._pressure_data_idx %= MAX_DATA_POINTS
        self.pressure_data[self._pressure_data_idx] = [time.time(), data_point]

    def update_flow_data(self):
        # Implementación con cola circular
        data_point = self.f_deque_in.popleft()
        self._flow_data_idx += 1
        self._flow_data_idx %= MAX_DATA_POINTS
        self.flow_data[self._flow_data_idx] = [time.time(), data_point]

    def get_pressure_data(self):
        idx = self._pressure_data_idx
        idx += 1
        idx = idx % MAX_DATA_POINTS
        return np.append(self.pressure_data[idx:], self.pressure_data[:idx], axis=0)

    def get_flow_data(self):
        idx = self._flow_data_idx
        idx += 1
        idx = idx % MAX_DATA_POINTS
        return np.append(self.flow_data[idx:], self.flow_data[:idx], axis=0)

    def run(self):
        while True:
            try:
                if len(self.p_deque_in):
                    self.update_pressure_data()
                if len(self.f_deque_in):
                    self.update_flow_data()
                else:
                    time.sleep(0.0001)

            except KeyboardInterrupt:
                sys.exit()
