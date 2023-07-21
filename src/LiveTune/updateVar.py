import socket

def updateVar(var_value, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    data = var_value
    client_socket.send(data.encode())
    client_socket.close()