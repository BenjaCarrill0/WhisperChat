import socket
import threading
# host = "localhost"
# port = 1800
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((host, port))
# sock.listen()
# print("El server está escuchando")

# try:
#     sock_client, (ip_client, port_client) = sock.accept()
#     print(f"Se acaba de aceptar a la ip {ip_client} con port {port_client}")
#     while True:
#         print("Ahora se recibirá el largo del mensaje")
#         lenght_msg = int.from_bytes(sock_client.recv(4), byteorder = "big")
#         if lenght_msg == 0:
#             break
#         print(f"El largo es de {lenght_msg} bytes")
#         msg = sock_client.recv(lenght_msg).decode("utf-8")
#         print(msg)
# except ConnectionError:
#     print("Hubo algún error en la conexión con el cliente")

# finally:
#     sock.close()
#     print("Aquí termina todo")

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        online_users = set()
        self.sock.listen()
        self.accept_connections()
    
    def accept_connections(self):
        thread = threading.Thread(target = self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        client_sock, _ = self.sock.accept()
        listening_client_thread = threading.Thread(target =)
    
    def listening_client(self, client_sock):
        pass