import socket

host = "localhost"
port = 1800
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((host, port))
    print("Conexión realizada correctamente")
    while True:
        msg = input("Introduce el mensaje que quieres enviar:\n")
        msg_bytes = msg.encode("utf-8")
        lenght_msg = len(msg_bytes).to_bytes(length = 4, byteorder = "big")
        sock.sendall(lenght_msg + msg_bytes)

except ConnectionError as e:
    print(f"Error: {e}")
    print("Se genero un error, posiblemente porque el server no está prendido")

finally:
    sock.close()
    print("Aquí termina todo")