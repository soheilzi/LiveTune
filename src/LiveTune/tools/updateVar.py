#!/usr/bin/env python3

import argparse
import socket

REQTYPE = "request_type: update_var"
TRIGGER = "request_type: trigger_var"

from LiveTune.liveVar import Color

def typeChecker(var_value):
    if var_value is None:
        return "None"
    elif var_value == "True" or var_value == "False":
        return "bool"
    elif var_value.isdigit():
        return "int"
    elif len(var_value) == 1:
        return "char"
    elif var_value.replace('.', '', 1).isdigit():
        return "float"
    else:
        return "string"

def updateVar(var_value, port, trigger):
    # print("Starting...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('localhost', port))
    # print("Connected to server")

    client_socket.send(REQTYPE.encode())  # Send request type to the server
    # print("Sent request type")

    response = client_socket.recv(1024).decode()  # Receive response type from the server

    if trigger and (response == "trigger"):
        client_socket.send(TRIGGER.encode())  # Send request type to the server
    elif (response == typeChecker(var_value)) and var_value is not None: # Check if var matches the response type
        data = var_value
        client_socket.send(data.encode())
    else:
        print(f"{Color.RED}[ERROR]{Color.END} {Color.YELLOW}Variable type mismatch. Expected {response}, got {typeChecker(var_value)}{Color.END}")

    # print("Closing connection")
    
    client_socket.close()

def request_port(tag: str, port: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', port))
        client_socket.send(f"request_type: dictionary_entry - {tag}".encode())
        response = client_socket.recv(1024).decode()
    finally:
        client_socket.close()

    return int(response)



def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--value", "-v", type=str, help="Value of the variable")
    parser.add_argument("--port", "-p", type=int, help="Port number", required=True)
    parser.add_argument("--tag", "-t", type=str, help="Tag of the variable", required=True)
    parser.add_argument("--trigger", "-tr", action="store_true", help="Trigger the variable")

    args = parser.parse_args()

    # Call the updateVar function with the provided arguments
    variable_port = request_port(args.tag, args.port)
    updateVar(args.value, variable_port, args.trigger)

if __name__ == '__main__':
    main()

