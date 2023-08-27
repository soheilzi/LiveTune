#!/usr/bin/env python3

import argparse
import socket

TRIGGER = "request_type: trigger_var"

def triggerVar(port):
    # print("Starting...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('localhost', port))
    # print("Connected to server")

    client_socket.send(TRIGGER.encode())  # Send request type to the server
    # print("Sent request type")

    # print("Closing connection")
    
    client_socket.close()

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, help="Port number")

    args = parser.parse_args()

    # Call the updateVar function with the provided arguments

    triggerVar(args.port)
