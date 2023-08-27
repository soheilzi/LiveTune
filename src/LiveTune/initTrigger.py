import threading
import socket
from typing import Any

TRIGGER = "request_type: trigger_var"

class initTrigger:
    instances = []
    update_thread = None

    def __init__(self, port, options=None):
        if port < 0:
            raise ValueError("Port number cannot be negative.")
        
        self.state_is_triggered = False
        self.lock = threading.Lock()
        self.port = port
        self.instances.append(self)
        self.enable()

    def __str__(self):
        return str(self.var_value)

    def __repr__(self):
        return f"initVar({self.var_value})"

    def __eq__(self, other):
        if isinstance(other, initTrigger):
            return self.var_value == other.var_value
        return False

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.state_is_triggered:
            self.state_is_triggered = False
            return True
        return False

    def handleClient(self, connection):
        while True:
            data = connection.recv(1024).decode()
            if not data:
                break

            if data == TRIGGER:
                with self.lock:
                    self.state_is_triggered = True

        connection.close()

    def enable(self):
        listenerThread = threading.Thread(target=self.startListener)
        listenerThread.start()


    def startListener(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            listenerSocket.bind(('localhost', self.port))
        except socket.error as e:
            raise OSError(f"Error binding to port {self.port}: {e}")

        listenerSocket.listen(1)

        # Debug print statement for listening
        # print(f"Listening for client connections on port {self.port}...")

        while True:
            connection, address = listenerSocket.accept()
            # Removed print statement for connected client
            # print(f"Connected to client: {address}")

            client_thread = threading.Thread(target=self.handleClient, args=(connection,))
            client_thread.start()
