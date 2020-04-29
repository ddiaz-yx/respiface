'''
This script sends simulated respiratory data for the main GUI to plot.
For it to work, both need to use the same socket address.
'''

import socket
import sys
import os
import time
from threading import Thread
import struct

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = "/home/mich/my_socket"
sock.connect(server_address)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('sim_data.csv', 'r') as csv:
    data = [l.split(',') for l in csv.read().splitlines()]

data = data[1:]

def send_data():
    global data, sock
    t_delta = 0.02
    i = 0
    next_t = 0
    while True:
        for line in data:
            t = time.time()
            cp = struct.pack('>d', float(line[1])).hex()
            cf = struct.pack('>d', float(line[2])).hex()
            tf = struct.pack('>d', float(line[3])).hex()
            msg = bytes(f"d?ts={t}&n=1&cp={cp}&cf={cf}&tf={tf}".encode('ascii'))
            sock.sendall(msg)
            time.sleep(t_delta)

tr = Thread(target=send_data, daemon=True)
tr.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    sock.close()
    sys.exit(0)
