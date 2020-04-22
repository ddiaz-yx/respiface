from collections import deque
from threading import Thread, Event
import time
import socket

import os
from urllib.parse import urlparse
from urllib import parse


class DataProxy(Thread):
    def __init__(self, socket_address, deque_pressure: deque, deque_flow: deque, data_in: deque, data_out: deque):
        Thread.__init__(self)
        try:
            os.unlink(socket_address)
        except OSError:
            if os.path.exists(socket_address):
                raise
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(socket_address)
        self.deque_pressure = deque_pressure  # deque de listas [timestamp, valor] en direccion socket -> pantalla
        self.deque_flow = deque_flow  # deque de tuplas [timestamp, valor] en direccion socket -> pantalla
        self.data_in = data_in  # deque de objetos data_dict en dirección pantalla -> socket.
        self.data_out = data_out  # deque de objetos data_dict en dirección socket -> pantalla
        self.stop = Event()
        self.data_in_thread = Thread(target=self.ui_out, daemon=True)
        self.data_in_thread.start()
        self.connection = None
        self.socket.listen(1)
        self.socket.setblocking(True)

    def ui_out(self):
        while True:
            if len(self.data_in):
                print(f"Sending: {self.data_in}")
                data = self.data_in.popleft()
                msg = bytes(f"set_conf?{data[0]}={data[1]}".encode('utf8'))
                if self.connection is not None:
                    self.connection.sendall(msg)
            else:
                time.sleep(0.1)

    def run(self):
        while not self.stop.is_set():
            print("Waiting for connections from unix socket ...")
            self.connection, client_address = self.socket.accept()
            while not self.stop.is_set():
                data = self.connection.recv(2048)
                if data == b'':  # Se cerró la conexion
                    print("Conection closed by client")
                    break
                else:
                    self.process_socket_data(data)

    def process_socket_data(self, data):
        #print("Data Recieved: {}".format(data))
        str_data = data.decode('ascii')
        o = urlparse(str_data)
        params = dict(parse.parse_qsl(o.query))
        if o.path == 'set_conf':
            for name, value in params.items():
                self.data_out.append((name, value))
        if o.path == 'reset_conf':
            print("reset_conf")
        if o.path == 'd':
            try:
                if "cp" in params:
                    self.deque_pressure.append(float(params["cp"]))
                if "cf" in params:
                    self.deque_flow.append(float(params["cf"]))
                if "tf" in params:
                    pass
            except ValueError as e:
                print(e)

    def stop(self):
        self.stop.set()


if __name__ == '__main__':
    data_out = deque()
    data_in = deque()
    proxy = DataProxy("/tmp/my_socket", None, None, data_in, data_out)
    proxy.start()
    time.sleep(10)
    data_in.append(("peep", 2))
