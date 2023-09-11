import threading
import socket
from typing import Any

class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

class LiveVariableBase:
    instances = []
    update_thread = None
    dictionary_port = []

    def __init__(self, tag: str):
        if not isinstance(tag, str):
            raise TypeError("Tag must be a string.")
        
        for instance in self.instances:
            if instance.tag == tag:
                raise Warning(f"{Color.RED}[WARN]{Color.END} {Color.YELLOW}{tag} already exists. Reusing tag names may have unintended consequences.{Color.END}")

        if self.dictionary_port == []:
            sock = socket.socket()
            try:
                sock.bind(('', 0))
                self.dictionary_port.append(sock.getsockname()[1])
                print("Port number for liveVar dictionary: {}".format(self.dictionary_port[0]))
                self.enable_dictionary_port()
            finally:
                sock.close()

        sock = socket.socket()
        try:
            sock.bind(('', 0))
            self.port = sock.getsockname()[1]
        finally:
            sock.close()

        self.tag = tag
        self.lock = threading.Lock()
        self.instances.append(self)

    def __str__(self):
        raise NotImplementedError
    def __repr__(self):
        raise NotImplementedError
    def __eq__(self, other):
        raise NotImplementedError
    def __add__(self, other):
        raise NotImplementedError
    def __sub__(self, other):
        raise NotImplementedError
    def __mul__(self, other):
        raise NotImplementedError
    def __truediv__(self, other):
        raise NotImplementedError
    def __rmul__(self, other):
        raise NotImplementedError
    def __iadd__(self, other):
        raise NotImplementedError
    def __isub__(self, other):
        raise NotImplementedError
    def __imul__(self, other):
        raise NotImplementedError
    def __itruediv__(self, other):
        raise NotImplementedError
    def __getitem__(self, key):
        raise NotImplementedError
    def __setitem__(self, key, value):
        raise NotImplementedError
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError
    def handleClient(self, connection):
        raise NotImplementedError

    def enable(self):
        listenerThread = threading.Thread(target=self.startListener)
        listenerThread.daemon = True
        listenerThread.start()

    def _find_port(self, tag):
        for instance in self.instances:
            if instance.tag == tag:
                return str(instance.port)
        raise KeyError(f"Tag '{tag}' not found.")

    def enable_dictionary_port(self):
        listenerThread = threading.Thread(target=self.startListener_dictionary_port)
        listenerThread.daemon = True
        listenerThread.start()

    def handleClient_dictionary_port(self, connection):
        REQTYPE = "request_type: dictionary_entry - " # the send format is "request_type: dictionary_entry - <tag>"
        message = connection.recv(1024).decode()
        if REQTYPE in message:
            tag = message[33:] # substring from 33 till end to get tag
            connection.send(self._find_port(tag).encode())
        connection.close()


    def startListener_dictionary_port(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listenerSocket.bind(('localhost', self.dictionary_port[0]))
            listenerSocket.listen(1)

            # Debug print statement for listening
            # print(f"Listening for client connections on port {self.dictionary_port[0]}...")

            while True:
                connection, address = listenerSocket.accept()

                client_thread = threading.Thread(target=self.handleClient_dictionary_port, args=(connection,))
                client_thread.daemon = True
                client_thread.start()
        finally:
            listenerSocket.close()

    def startListener(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listenerSocket.bind(('localhost', self.port))
            listenerSocket.listen(1)

            while True:
                connection, address = listenerSocket.accept()

                client_thread = threading.Thread(target=self.handleClient, args=(connection,))
                client_thread.daemon = True
                client_thread.start()
        finally:
            listenerSocket.close()