import zmq
import time

host = "127.0.0.1"
port = "6000"

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Connects to a bound socket
socket.connect("tcp://{}:{}".format(host, port))

time.sleep(0.5)

# Subscribes to all topics
socket.subscribe("height")

# Receives a string format message
while(True):
    print(socket.recv().decode('utf-8'))

