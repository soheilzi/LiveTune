import threading
import socket
from typing import Any
from LiveTune.liveVar import liveVar

TRIGGER = "request_type: trigger_var"

class initTrigger(liveVar):

    def __init__(self, tag):
        super().__init__(tag)
        self.state_is_triggered = False
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