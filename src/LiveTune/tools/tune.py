#!/usr/bin/env python3

import argparse
import socket

REQTYPE = "request_type: update_var"
TRIGGER = "request_type: trigger_var"

from LiveTune.LiveVariableBase import Color

def typeChecker(s):
    """
    Determines the primitive type of a string.

    :param s: Input string.
    :return: String representation of the detected type.
    """

    # Try to convert to integer
    if s is None:
        return "None"
    try:
        int(s)
        return "int"
    except ValueError:
        pass

    # Try to convert to float
    try:
        float(s)
        return "float"
    except ValueError:
        pass

    # Check for boolean
    bool_values = ["true", "false", "True", "False"]
    if s in bool_values:
        return "bool"

    return "string"

def tune(var_value, port, tag, trigger):
    # print("Starting...")
    variable_port = request_port(tag, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('localhost', variable_port))
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
    except:
        print(f"{Color.RED}[ERROR]{Color.END} {Color.YELLOW}Failed to connect to the LiveTune dictionary. This is most likely because of an incorrect port.{Color.END}")
        raise
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

    # Call the tune function with the provided arguments
    # variable_port = request_port(args.tag, args.port)
    tune(args.value, args.port, args.tag,args.trigger)

if __name__ == '__main__':
    main()

