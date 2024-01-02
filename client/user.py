import socket
import threading

CHUNK_SIZE = 32

class User:
    def __init__(self, host_server, port_server):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host_server, port_server))
            self.recieve_user()
            self.listen()
            self.send()
        finally:
            self.sock.close()

    def recieve_user(self):
        print("Tell me your username:", end = " ")
        username = input()
        print("Now your password:", end = " ")
        password = input()
        self.send_info(username, password)

    def send_info(self, username, password):
        user = username.encode("utf-8")
        lenght_user = len(user).to_bytes(length = 4, byteorder = "big")
        password = password.encode("utf-8")
        lenght_password = len(password).to_bytes(length = 4, byteorder = "big")
        full_msg = bytearray()
        full_msg.extend(lenght_user + user + lenght_password + password)
        sended = 0
        while sended < len(full_msg):
            sended += self.sock.send(full_msg[sended:])

    def listen(self):
        listening = threading.Thread(target = self.listen_thread, daemon = True)
        listening.start()

    def listen_thread(self):
        while True:
            lenght_msg = int.from_bytes(self.sock.recv(4), byteorder = "big")
            msg = bytearray()
            while len(msg) < lenght_msg:
                lenght_recv = min(CHUNK_SIZE, lenght_msg - len(msg))
                msg.extend(self.sock.recv(lenght_recv))
            print(msg)

    def send(self):
        sending = threading.Thread(target = self.send_thread, daemon = True)
        sending.start()

    def send_thread(self):  
        while True:
            user = input("Tell me who you want to send a message: ", end = "")
            msg = input("What do you want to say?", end = "\n")
            