import socket

def updateVar(var_value, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    data = var_value
    client_socket.send(data.encode())
    client_socket.close()

# Example usage
var_value = '30'
port = 12345

updateVar(var_value, port)

var_value = '40'
port = 12346

updateVar(var_value, port)
