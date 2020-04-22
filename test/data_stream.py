'''
This script sends simulated respiratory data for the main GUI to plot.
For it to work, both need to use the same socket address.
'''

import socket
import sys
import os
import time
from threading import Thread

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = "/tmp/my_socket"
sock.connect(server_address)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('P_lung.csv', 'r') as csv:
    p_data = [l.split(',') for l in csv.read().splitlines()]
with open('Vdot.csv', 'r') as csv:
    f_data = [l.split(',') for l in csv.read().splitlines()]


def send_pressure_data():
    global p_data, sock
    t_delta = 0.03
    i = 0
    next_t = 0
    while True:
        t = float(p_data[i][0])
        while t < next_t and i < len(p_data):
            t = float(p_data[i][0])
            i += 1
        if i < len(p_data):
            msg = bytes(f"d?cp={p_data[i][1]}".encode('utf8'))
            sock.sendall(msg)
            next_t = t + t_delta
            time.sleep(t_delta)
        else:
            i = 0
            next_t = 0


def send_flow_data():
    global f_data, sock
    t_delta = 0.03
    i = 0
    next_t = 0
    while True:
        t = float(f_data[i][0])
        while t < next_t and i < len(f_data):
            t = float(f_data[i][0])
            i += 1
        if i < len(f_data):
            msg = bytes(f"d?cf={f_data[i][1]}".encode('utf8'))
            sock.sendall(msg)
            next_t = t + t_delta
            time.sleep(t_delta)
        else:
            i = 0
            next_t = 0


t1 = Thread(target=send_pressure_data, daemon=True)
t2 = Thread(target=send_flow_data, daemon=True)
t1.start()
t2.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    sock.close()
    sys.exit(0)
