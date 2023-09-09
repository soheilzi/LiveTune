#!/usr/bin/env python3

import argparse
import socket

REQTYPE = "request_type: update_var"

def typeChecker(var_value):
    if var_value == "True" or var_value == "False":
        return "bool"
    elif var_value.isdigit():
        return "int"
    elif len(var_value) == 1:
        return "char"
    elif var_value.replace('.', '', 1).isdigit():
        return "float"
    else:
        return "string"

def updateVar(var_value, port):
    # print("Starting...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('localhost', port))
    # print("Connected to server")

    client_socket.send(REQTYPE.encode())  # Send request type to the server
    # print("Sent request type")

    response = client_socket.recv(1024).decode()  # Receive response type from the server

    if response == typeChecker(var_value): # Check if var matches the response type
        data = var_value
        client_socket.send(data.encode())
        # print("Sent data")

    # print("Closing connection")
    
    client_socket.close()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--value", "-v", type=str, help="Value of the variable")
    parser.add_argument("--port", "-p", type=int, help="Port number")

    args = parser.parse_args()

    # Call the updateVar function with the provided arguments
    updateVar(args.value, args.port)

if __name__ == '__main__':
    main()

