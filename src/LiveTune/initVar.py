import time
import threading
import socket

class initVar:
    instances = []
    update_thread = None

    def __init__(self, var_name, initial_value, port):
        self.var_name = var_name
        self.var_value = initial_value
        self.lock = threading.Lock()
        self.port = port
        self.instances.append(self)

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
            return initVar(self.var_value + other.var_value)
        raise TypeError("Unsupported operand type for +: 'initVar' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, initVar):
            return initVar(self.var_value - other.var_value)
        raise TypeError("Unsupported operand type for -: 'initVar' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, initVar):
            return initVar(self.var_value * other.var_value)
        raise TypeError("Unsupported operand type for *: 'initVar' and '{}'".format(type(other).__name__))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, initVar):
            if other.var_value != 0:
                return initVar(self.var_value / other.var_value)
            raise ZeroDivisionError("Division by zero is not allowed.")
        raise TypeError("Unsupported operand type for /: 'initVar' and '{}'".format(type(other).__name__))

    def __getitem__(self, key):
        if key == 'value':
            return self.var_value
        raise KeyError("Invalid key '{}' for __getitem__".format(key))

    def __setitem__(self, key, value):
        if key == 'value':
            with self.lock:
                self.var_value = value
            return
        raise KeyError("Invalid key '{}' for __setitem__".format(key))

    @classmethod
    def updateVar(cls):
        while True:
            for instance in cls.instances:
                with instance.lock:
                    instance.var_value += 1
                    print(f"{instance.var_name} value:", instance.var_value)

            time.sleep(1)

    def handleClient(self, connection):
        while True:
            data = connection.recv(1024).decode()
            if not data:
                break

            with self.lock:
                self.var_value = int(data)

        connection.close()

    def start(self):
        if not initVar.update_thread:
            initVar.update_thread = threading.Thread(target=initVar.updateVar)
            initVar.update_thread.start()

        listenerThread = threading.Thread(target=self.startListener)
        listenerThread.start()

    def startListener(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenerSocket.bind(('localhost', self.port))
        listenerSocket.listen(1)

        print(f"Listening for client connections on port {self.port}...")

        while True:
            connection, address = listenerSocket.accept()
            print(f"Connected to client: {address}")

            client_thread = threading.Thread(target=self.handleClient, args=(connection,))
            client_thread.start()
