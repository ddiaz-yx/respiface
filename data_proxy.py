"""
El objetivo de la clase DataManager es ser de intermediario pincipal entre los datos desplegados
en pantalla e ingresados en ella y las entradas/salidas de datos por los puertos UART y SPI
"""

from PyQt5.QtCore import QThread, pyqtSignal
from enum import Enum, auto
from collections import deque
from threading import Event
import time
import socket
import os
from urllib.parse import urlparse
from urllib import parse
import struct
from parameter import Parameter
from threading import Thread

SOCKET_ADDRESS = "/home/mich/my_socket"
MAX_DATA_POINTS = 6000  # 60 segundos a 100 Hz
SAMPLE_PERIOD = 0.01  # seconds

PARAM_TYPES = {
    'fio2': float,
    'brpm': int,
    'ier': int,
    'ier_i': int,
    'ier_e': int,
    'ast': int,
    'mode': int,
    'tvm': int,
    'peep': int
}
PARAM_NAMES = (k for k in PARAM_TYPES)


class OpMode(Enum):
    PCV = 0
    VCV = 1
    SIMV = 2


def parse_data(n_samples, hex_string, timestamp):
    t = timestamp
    data = []
    dec = bytearray.fromhex(hex_string)
    iter_ = struct.iter_unpack('>d', dec)
    for i in range(0, n_samples):
        val, = next(iter_)
        data.extend([t, val])
        t = t + SAMPLE_PERIOD
    return data


class DataProxy(QThread):
    signal_params_properties_set = pyqtSignal(
        dict)  # Se emite una vez hayan sido configurados todos los parámetros (min, max y default)
    signal_new_param_values = pyqtSignal(
        dict)  # Se emite cuando se desde el socket llega un nuevo valor para un parámetro

    def __init__(self, cur_pressure: deque, cur_flow: deque, total_flow: deque, user_set_param: deque):
        QThread.__init__(self)
        try:
            os.unlink(SOCKET_ADDRESS)
        except OSError:
            if os.path.exists(SOCKET_ADDRESS):
                raise
        self.dq_cp = cur_pressure
        self.dq_cf = cur_flow
        self.dq_tf = total_flow
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(SOCKET_ADDRESS)
        #self.socket = socket.socket()
        #self.socket.bind(('', 5040))
        self.stop = Event()
        self.connection = None
        self.socket.listen(1)
        self.socket.setblocking(True)
        self.operation_mode = OpMode.VCV
        self.user_set_param: deque = user_set_param
        self.params = dict()
        for p in PARAM_NAMES:
            self.params[p] = Parameter(name=p)

    def send_new_param_value(self):
        """
        Periodically checks the deque for new params set by the user
        It can receive either a Parameter object or a dictionay of Parameters
        """
        while True:
            if len(self.user_set_param):
                msg = bytes("set_conf?".encode('ascii'))
                p = self.user_set_param.popleft()
                if isinstance(p, Parameter): # If it is a single parameter, put it inside a dict
                    p = {f'{p.name}': p}
                for param in p.values():
                    if param.name == 'ier':
                        val_i = PARAM_TYPES[param.name](param.value[0])
                        val_e = PARAM_TYPES[param.name](param.value[1])
                        msg += bytes(f"ier_i={val_i}&ier_e={val_e}".encode('ascii'))
                    else:
                        val = PARAM_TYPES[param.name](param.value)
                        msg += bytes(f"{param.name}={val}".encode('ascii'))
                    msg += bytes('&'.encode('ascii'))

                msg = msg[:-1] + bytes("\n".encode('ascii'))  # Removes last '&' and adds end-line
                print(f"Sending {msg} to socket")
                if self.connection is not None:
                    self.connection.sendall(msg)
            else:
                time.sleep(0.1)

    def run(self):
        ts = Thread(target=self.send_new_param_value, daemon=True)
        ts.start()

        while not self.stop.is_set():
            print("Waiting for connections from unix socket ...")
            self.connection, client_address = self.socket.accept()
            print("Peer connected !!!")
            while not self.stop.is_set():
                try:
                    data = self.connection.recv(2048)
                except ConnectionResetError:
                    print("Connection reset by peer")
                    break
                if data == b'':  # Se cerró la conexion
                    print("Connection reset by peer")
                    break
                else:
                    self.process_socket_data(data)

    def check_params(self):
        """
        Verifica que todos los parámetros hayan sido seteados antes de informar a la GUI
        """
        all_set = True
        for p in self.params.values():
            if p.value_max is None or p.value_min is None or p.value_default is None:
                all_set = False
        if all_set:
            self.signal_params_properties_set.emit(self.params)

    def ack(self):
        self.connection.sendall(bytes('+ack\n'.encode('ascii')))

    def process_socket_data(self, data):
        try:
            str_data = data.decode('ascii')
            o = urlparse(str_data)
            data = dict(parse.parse_qsl(o.query))
            if o.path == 'reset_conf':
                print("reset_conf")
            elif o.path == 'set_conf':
                print("New parameter value received")
                for param, value in data.items():
                    self.params[param].value = float(value)
                self.signal_new_param_values.emit(self.params)
                self.ack()
            elif o.path == 'def_conf':
                for param, value in data.items():
                    self.params[param].value_default = float(value)
                self.ack()
                self.check_params()
            elif o.path == 'min_conf':
                for param, value in data.items():
                    self.params[param].value_min = float(value)
                self.ack()
                self.check_params()
            elif o.path == 'max_conf':
                for param, value in data.items():
                    self.params[param].value_max = float(value)
                self.ack()
                self.check_params()
            elif o.path == 'd':
                num_samples = int(data['n'])
                timestamp = float(data['ts'])
                cp_vals = parse_data(num_samples, data['cp'], timestamp)
                cf_vals = parse_data(num_samples, data['cf'], timestamp)
                tf_vals = parse_data(num_samples, data['tf'], timestamp)
                self.dq_cp.append(cp_vals)
                self.dq_cf.append(cf_vals)
                self.dq_tf.append(tf_vals)
        except ValueError as e:
            print(e)
