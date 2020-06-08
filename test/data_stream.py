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

param_properties = ("def_conf?fio2=21.0&brpm=20&ier_i=1&ier_e=3&ast=1&mode=1&tvm=500&peep=12\n",
					"min_conf?fio2=21.0&brpm=5&ier_i=1&ier_e=5&ast=1&tvm=100&peep=12\n",
					"max_conf?fio2=100.0&brpm=100&ier_i=3&ier_e=1&ast=20&tvm=1000&peep=20\n")

param_sets = ("set_conf?fio2=52.3&ier_i=3&brpm=6&ier_e=1&ast=1&mode=1&tvm=120&peep=5\n",
			  "set_conf?fio2=21.0&brpm=20&ier_i=1&ier_e=3&ast=1&mode=1&tvm=500&peep=12\n",
			  "set_conf?fio2=25.0&brpm=5&ier_i=1&ier_e=5&ast=1&tvm=100&peep=8\n",
			  "set_conf?fio2=100.0&brpm=100&ier_i=3&ier_e=1&ast=20&tvm=1000&peep=20\n")


def send_data():
	global data, sock
	t_delta = 0.02
	i = 0
	while True:
		for line in data:
			t = time.time()
			cp = struct.pack('>d', float(line[1])).hex()
			cf = struct.pack('>d', float(line[2])).hex()
			tv = struct.pack('>d', float(line[3])).hex()
			msg = f"d?ts={t}&n=1&cp={cp}&cf={cf}&tv={tv}".encode('ascii')
			sock.sendall(msg)
			time.sleep(t_delta)


def send_param_value():
	for p in param_properties:
		sock.sendall(p.encode('ascii'))
	i = 0
	while True:
		time.sleep(5)
		msg = param_sets[i % 4].encode('ascii')
		print(f"Sending {msg}")
		sock.sendall(msg)
		i += 1


tr = Thread(target=send_data, daemon=True)
tr.start()
tr2 = Thread(target=send_param_value, daemon=True)
tr2.start()

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	sock.close()
	sys.exit(0)
