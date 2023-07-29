#!/usr/bin/env python3

import argparse
import socket

def updateVar(var_value, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    data = str("type?")
    data = str(var_value) 
    client_socket.send(data.encode())

    client_socket.close()

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--value", "-v", type=int, help="Value of the variable")
    parser.add_argument("--port", "-p", type=int, help="Port number")
    parser.add_argument("--trigger", "-t", action="store_true", help="Trigger the update")

    args = parser.parse_args()

    # Call the updateVar function with the provided arguments

    updateVar(args.value, args.port)
