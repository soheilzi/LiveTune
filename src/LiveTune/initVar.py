import threading
import socket
from typing import Any

class initVar:
    instances = []
    update_thread = None
    dictionary_port = []

    def __init__(self, initial_value, tag):
        if not isinstance(initial_value, (int, float)):
            raise TypeError("Initial value must be a number (int or float).")
        
        if self.dictionary_port == []:
            sock = socket.socket()
            sock.bind(('', 0))
            self.dictionary_port.append(sock.getsockname()[1])
            print("Port number for initVar dictionary: {}".format(self.dictionary_port[0]))

        sock = socket.socket()
        sock.bind(('', 0))
        self.port = sock.getsockname()[1]
        
        self.var_value = initial_value
        self.tag = tag
        self.dtype = type(initial_value)
        self.lock = threading.Lock()
        self.instances.append(self)
        self.enable()
        self.enable_dictionary_port()

    def __str__(self):
        return str(self.var_value)

    def __repr__(self):
        return f"initVar({self.var_value})"

    def __eq__(self, other):
        if isinstance(other, initVar):
            return self.var_value == other.var_value
        return False

    def __add__(self, other):
        if isinstance(other, initVar):
            return self.var_value + other.var_value
        raise TypeError(f"Unsupported operand type for +: 'initVar' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, initVar):
            return self.var_value - other.var_value
        raise TypeError(f"Unsupported operand type for -: 'initVar' and '{type(other).__name__}'")

    def __mul__(self, other):
        if isinstance(other, initVar):
            return self.var_value * other.var_value
        raise TypeError(f"Unsupported operand type for *: 'initVar' and '{type(other).__name__}'")

    def __truediv__(self, other):
        if isinstance(other, initVar):
            if other.var_value != 0:
                return self.var_value / other.var_value
            raise ZeroDivisionError("Division by zero is not allowed.")
        elif isinstance(other, int):
            if other != 0:
                return self.var_value / other
            raise ZeroDivisionError("Division by zero is not allowed.")
        raise TypeError(f"Unsupported operand type for /: 'initVar' and '{type(other).__name__}'")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __iadd__(self, other):
        if isinstance(other, initVar):
            with self.lock:
                self.var_value += other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value += other
            return self
        raise TypeError("Unsupported operand type for +=: 'initVar' and '{}'".format(type(other).__name__))
    
    def __isub__(self, other):
        if isinstance(other, initVar):
            with self.lock:
                self.var_value -= other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value -= other
            return self
        raise TypeError("Unsupported operand type for -=: 'initVar' and '{}'".format(type(other).__name__))

    def __imul__(self, other):
        if isinstance(other, initVar):
            with self.lock:
                self.var_value *= other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value *= other
            return self
        raise TypeError("Unsupported operand type for *=: 'initVar' and '{}'".format(type(other).__name__))

    def __itruediv__(self, other):
        if isinstance(other, initVar):
            if other.var_value != 0:
                with self.lock:
                    self.var_value /= other.var_value
                return self
            raise ZeroDivisionError("Division by zero is not allowed.")
        elif isinstance(other, int):
            if other != 0:
                with self.lock:
                    self.var_value /= other
                return self
            raise ZeroDivisionError("Division by zero is not allowed.")
        raise TypeError("Unsupported operand type for /=: 'initVar' and '{}'".format(type(other).__name__))


    def __getitem__(self, key):
        if key == 'value':
            return self.var_value
        if key == 'dtype':
            return self.dtype
        if key == 'port':
            return self.port
        raise KeyError("Invalid key '{}' for __getitem__".format(key))

    def __setitem__(self, key, value):
        if key == 'value':
            with self.lock:
                self.var_value = value
            return
        if key == 'dtype':
            raise TypeError("Cannot change dtype of initVar.")
        if key == 'port':
            raise TypeError("Cannot change port of initVar.")
        raise KeyError("Invalid key '{}' for __setitem__".format(key))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.var_value



    def handleClient(self, connection):
        REQTYPE = "request_type: update_var"

        if connection.recv(1024).decode() == REQTYPE: # Receive request type from the client
            connection.send(str(self.dtype.__name__).encode())
        else:
            connection.close()
            return

        while True:
            data = connection.recv(1024).decode()
            if not data:
                break

            with self.lock:
                self.var_value = self.dtype(data)

        connection.close()

    def enable(self):
        listenerThread = threading.Thread(target=self.startListener)
        listenerThread.start()

    def _find_port(self, tag):
        for instance in self.instances:
            if instance.tag == tag:
                return str(instance.port)
        raise KeyError(f"Tag '{tag}' not found.")

    def enable_dictionary_port(self):
        listenerThread = threading.Thread(target=self.startListener_dictionary_port)
        listenerThread.start()

    def handleClient_dictionary_port(self, connection):
        REQTYPE = "request_type: dictionary_entry - " # the send format is "request_type: dictionary_entry - <tag>"
        print("Handling client dictionary port")
        message = connection.recv(1024).decode()
        if REQTYPE in message:
            print("Received request for port:", message)
            tag = message[33:] # substring from 33 till end to get tag
            connection.send(self._find_port(tag).encode())
        else:
            print("Closing connection")
            connection.close()


    def startListener_dictionary_port(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listenerSocket.bind(('localhost', self.dictionary_port[0]))
            print("before listen")
            listenerSocket.listen(1)

            # Debug print statement for listening
            # print(f"Listening for client connections on port {self.dictionary_port[0]}...")

            while True:
                print("before accept")
                connection, address = listenerSocket.accept()

                client_thread = threading.Thread(target=self.handleClient_dictionary_port, args=(connection,))
                client_thread.start()
        finally:
            listenerSocket.close()

    def check_port(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
            except OSError:
                return False  # Port is already in use
            return True  # Port is available

    def startListener(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if not self.check_port(self.port):
                raise RuntimeError(f"Port {self.port} is already in use by a different variable or program. Please use a different port.")

            listenerSocket.bind(('localhost', self.port))
            listenerSocket.listen(1)

            # Debug print statement for listening
            # print(f"Listening for client connections on port {self.port}...")

            while True:
                connection, address = listenerSocket.accept()

                client_thread = threading.Thread(target=self.handleClient, args=(connection,))
                client_thread.start()
        finally:
            listenerSocket.close()