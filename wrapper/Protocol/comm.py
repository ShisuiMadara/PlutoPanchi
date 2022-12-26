import socket

PORT = 23
IP_ADDRESS = "192.168.4.1"
CAMERA_PORT = 9060
CAMERA_IP_ADDRESS = "192.168.0.1"

class connection():

    def __init__(self):
        pass


    def connect_socket(self):
        print("Connecting ...")

        try:
            self.socketId = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
        except socket.error as err: 
            print(err)