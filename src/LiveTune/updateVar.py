#!/usr/bin/env python3

import argparse
import socket

def updateVar(var_value, port):
    print("hello")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    data = str(var_value)
    client_socket.send(data.encode())
    client_socket.close()

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("var_value", type=int, help="Value of the variable")
    parser.add_argument("port", type=int, help="Port number")
    args = parser.parse_args()

    # Call the updateVar function with the provided arguments
    updateVar(args.var_value, args.port)
