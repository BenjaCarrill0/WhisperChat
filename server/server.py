import socket
import threading
import json

CHUNK_SIZE = 32

class Server:
    def __init__(self, host, port, users_file):
        self.users_path = users_file
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.lock_file = threading.Lock()
        self.lock_users = threading.Lock()
        self.lock_connections = threading.Lock()
        self.online_users = dict()
        self.sock.listen()
        self.accept_connections()
    
    def accept_connections(self):
        #This function creates a thread that all the time
        #Recieves differents connections
        thread = threading.Thread(target = self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        while True:
            client_sock, _ = self.sock.accept() #I use _ because the ip and port doesn't matter
            listening_client_thread = threading.Thread(target = self.listen_client,
                                                       args = (client_sock, ),
                                                       daemon = True)
            listening_client_thread.start()
    def listen_client(self, client_sock):
        lenght_user = int.from_bytes(self.sock.recv(4), byteorder = "big")
        user = self.sock.recv(lenght_user).decode("utf-8")
        lenght_password = int.from_bytes(self.sock.recv(4), byteorder = "big")
        password = self.sock.recv(lenght_password).decode("utf-8")
        #Now we check the file of users to see if the user is correct or not
        correct_user = False
        with self.lock_file:
            with open(self.users_path, "r") as users:
                data = json.load(users)
                if user in data:
                    if data[user] == password:
                        correct_user = True
        if correct_user:
            with self.lock_users:
                self.online_users[user] = client_sock
        #Now we can listen all messages of the user
        while correct_user:
            with self.lock_connections:
                lenght_msg = self.sock.recv(4)
                if lenght_msg == 0:
                    break
                lenght_target = self.sock.recv(4)
                if lenght_target == 0:
                    continue
                    #With this in case the user doesn't
                    #put any user. Then try another time
                target_user = self.recv(lenght_target).decode("utf-8")
                if target_user not in self.online_users:
                    error_msg = f"{target_user} is not online at this moment."
                    error_byte = error_msg.encode("utf-8")
                    self.send(error_byte, client_sock)
                else:
                    msg = bytearray()
                    while len(msg) < lenght_msg:
                        lenght_recv = min(CHUNK_SIZE, lenght_msg - len(msg))
                        msg.extend(self.sock.recv(lenght_recv))
                    self.send(msg, self.online_users[target_user])
        with self.lock_users:
            del self.online_users[user]
        client_sock.close()

    def send(msg, target_sock):
        lenght_msg = len(msg).to_bytes(length = 4, byteorder = "big")
        full_msg = lenght_msg + msg
        sended = 0
        while sended < len(full_msg):
            sended += target_sock.send(full_msg[sended:])