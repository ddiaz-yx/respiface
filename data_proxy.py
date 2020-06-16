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
from parameter import Parameter, ParamEnum, PLOT_TIME_SCALES
from threading import Thread
import logging

SOCKET_ADDRESS = "/tmp/touchscreen.sock"
MAX_DATA_POINTS = 6000  # 60 segundos a 100 Hz
SAMPLE_PERIOD = 0.01  # seconds
SAMPLE_LENGTH_BYTES = 8
BUF_RX_SIZE = 1048

PARAM_TYPES = {
	'fio2': float,
	'brpm': int,
	'ier': str,
	'ier_i': float,
	'ier_e': float,
	'ast': int,
	'mode': int,
	'tvm': int,
	'peep': int,
	'mf': float,
	'mp': float,
	'gscale': int,
	'pt': float
}
PARAM_NAMES = (k for k in PARAM_TYPES)


class OpMode(Enum):
	PCV = 0
	VCV = 1
	SIMV = 2


class DataMessage(object):

	START = "start"
	STOP = "stop"

	def __init__(self, message_type, params = None):
		self._message_type = message_type
		self._params = params

	def formatted_msg(self):
		params = ""
		if self._params:
			first = True
			for k, v in self._params.items():
				if not first:
					params = "{}&{}={}".format(params, k, v)
				else:
					first = False
					params = "{}={}".format(k, v)
		msg = "{}?{}\n".format(self._message_type, params).encode('ascii')
		return msg


class DataProxy(QThread):
	signal_params_properties_set = pyqtSignal(
		dict)  # Se emite una vez hayan sido configurados todos los parámetros (min, max y default)
	signal_new_param_values = pyqtSignal(
		dict)  # Se emite cuando se desde el socket llega un nuevo valor para un parámetro
	signal_status_report = pyqtSignal(bool)

	def __init__(self, cur_pressure: deque, cur_flow: deque, total_flow: deque, p_max: deque, p_avg: deque, peep: deque, fio2: deque, f_max: deque, user_set_param: deque, data_msg: deque):
		QThread.__init__(self)
		self.logger = logging.getLogger('gui')
		try:
			os.unlink(SOCKET_ADDRESS)
		except OSError:
			if os.path.exists(SOCKET_ADDRESS):
				raise
		self.dq_cp = cur_pressure
		self.dq_cf = cur_flow
		self.dq_tv = total_flow
		self.dq_p_max = p_max
		self.dq_p_avg = p_avg
		self.dq_peep = peep
		self.dq_fio2 = fio2
		self.dq_f_max = f_max
		self.buf_rx = deque(maxlen=BUF_RX_SIZE)
		self.parsed_data = ""
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
		self.data_msg: deque = data_msg
		self.params = dict()
		for p in PARAM_NAMES:
			self.params[p] = Parameter(name=p)

	def parse_data(self, n_samples, hex_string, timestamp):
		t = timestamp
		data = []
		try:
			dec = bytearray.fromhex(hex_string[:n_samples*SAMPLE_LENGTH_BYTES*2])
		except ValueError as e:
			self.logger.exception(f"Error parsing hex-string {hex_string}")
			return False
		iter_ = struct.iter_unpack('>d', dec)
		for i in range(0, n_samples):
			val, = next(iter_)
			data.extend([t, val])
			t = t + SAMPLE_PERIOD
		return data

	def parse_stats(self, n_samples, hex_string):
		data = []
		try:
			dec = bytearray.fromhex(hex_string[:n_samples*SAMPLE_LENGTH_BYTES*2])
		except ValueError as e:
			self.logger.exception(f"Error parsing hex-string {hex_string}")
			return False
		iter_ = struct.iter_unpack('>d', dec)
		for i in range(0, n_samples):
			val, = next(iter_)
			data.append(val)
		return data

	def send_new_param_value(self):
		"""
		Periodically checks the deque for new params set by the user
		It can receive either a Parameter object or a dictionay of Parameters
		"""
		while True:
			msg = None
			if len(self.user_set_param):
				msg = bytes("set_conf?".encode('ascii'))
				params = self.user_set_param.popleft()
				for param in params:
					if param.name == ParamEnum.gscale.name:
						val = PLOT_TIME_SCALES[PARAM_TYPES[param.name](param.value)]
					else:
						val = PARAM_TYPES[param.name](param.value)
					msg += bytes(f"{param.name}={val}&".encode('ascii'))
				msg = msg[:-1] + bytes("\n".encode('ascii'))  # Removes last '&' and adds end-line
			elif len(self.data_msg):
				dm = self.data_msg.popleft()
				msg = dm.formatted_msg()

			if msg is not None:
				self.logger.info(f"Sending {msg} to socket")
				if self.connection is not None:
					self.connection.sendall(msg)
			else:
				time.sleep(0.1)

	def parse_buffer(self):
		while len(self.buf_rx) > 0:
			c = self.buf_rx.popleft()
			if c == '\n':
				return True
			else:
				self.parsed_data = "".join([self.parsed_data, c])
		return False

	def run(self):
		ts = Thread(target=self.send_new_param_value, daemon=True)
		ts.start()

		while not self.stop.is_set():
			self.logger.info("Waiting for connections from unix socket ...")
			self.connection, client_address = self.socket.accept()
			self.logger.info("Peer connected !!!")
			while not self.stop.is_set():
				try:
					found_cmd = False
					if len(self.buf_rx) > 0:
						if self.parse_buffer():
							self.process_socket_data(self.parsed_data)
							found_cmd = True
							self.parsed_data = ""
					if not found_cmd:
						data = self.connection.recv(BUF_RX_SIZE)
						if len(data) > 0:
							for d in data.decode("utf-8"):
								self.buf_rx.append(d)
						else:
							self.logger.warning("Connection reset by peer")
							break
				except ConnectionResetError:
					self.logger.warning("Connection reset by peer")
					break
				time.sleep(0.001)

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
		try:
			self.connection.sendall(bytes('+ack\n'.encode('ascii')))
		except ConnectionResetError as e:
			self.logger.exception("Conection reset")


	def process_socket_data(self, data):
		try:
			o = urlparse(data)
			data = dict(parse.parse_qsl(o.query))
			if o.path == 'reset_conf':
				print("reset_conf")
			elif o.path == 'set_conf':
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
			elif o.path == "status":
				for k, v in data.items():
					if k == "running":
						self.signal_status_report.emit(bool(int(v)))
				self.ack()
			elif o.path == 'd':
				num_samples = int(data['n'])
				timestamp = float(data['ts'])
				cp_vals = self.parse_data(num_samples, data['cp'], timestamp)
				cf_vals = self.parse_data(num_samples, data['cf'], timestamp)
				tv_vals = self.parse_data(num_samples, data['tv'], timestamp)
				p_max = self.parse_stats(num_samples, data['cp_max'])
				p_avg = self.parse_stats(num_samples, data['cp_avg'])
				peep = self.parse_stats(num_samples, data['peep'])
				fio2 = self.parse_stats(num_samples, data['fio2'])
				f_max = self.parse_stats(num_samples, data['mf'])
				if cp_vals:
					self.dq_cp.append(cp_vals)
				if cf_vals:
					self.dq_cf.append(cf_vals)
				if tv_vals:
					self.dq_tv.append(tv_vals)
				if p_max:
					for val in p_max:
						self.dq_p_max.append(val)
				if p_avg:
					for val in p_avg:
						self.dq_p_avg.append(val)
				if peep:
					for val in peep:
						self.dq_peep.append(val)
				if fio2:
					for val in fio2:
						self.dq_fio2.append(val)
				if f_max:
					for val in f_max:
						self.dq_f_max.append(val)
		except ValueError as e:
			self.logger.exception("")
