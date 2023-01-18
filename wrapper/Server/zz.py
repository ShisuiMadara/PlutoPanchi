import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        t = 0
        while True:
            data = conn.recv(1024)
            print(data)
            t += 1
        #    if t == 102:
         #       break
