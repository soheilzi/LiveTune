import threading
import socket
from typing import Any
from LiveTune.LiveVariableBase import *

class liveVar(LiveVariableBase):
    def __init__(self, initial_value, tag):
        """Initializes a liveVar object.
        initial_value: The initial value of the variable.
        tag: A unique identifier for the variable.
        """
        super().__init__(tag)
        if not isinstance(initial_value, (int, float, bool)):
            raise TypeError("Initial value must be a number or boolean.")

        self.var_value = initial_value
        self.dtype = type(initial_value)
        self.has_changed = False
        self.enable()

    def __str__(self):
        return str(self.var_value)

    def __repr__(self):
        return f"liveVar({self.var_value})"

    def __eq__(self, other):
        if isinstance(other, liveVar):
            return self.var_value == other.var_value
        return False

    def __add__(self, other):
        if isinstance(other, liveVar):
            return self.var_value + other.var_value
        raise TypeError(f"Unsupported operand type for +: 'liveVar' and '{type(other).__name__}'")

    def __sub__(self, other):
        if isinstance(other, liveVar):
            return self.var_value - other.var_value
        raise TypeError(f"Unsupported operand type for -: 'liveVar' and '{type(other).__name__}'")

    def __mul__(self, other):
        if isinstance(other, liveVar):
            return self.var_value * other.var_value
        raise TypeError(f"Unsupported operand type for *: 'liveVar' and '{type(other).__name__}'")

    def __truediv__(self, other):
        if isinstance(other, liveVar):
            if other.var_value != 0:
                return self.var_value / other.var_value
            raise ZeroDivisionError("Division by zero is not allowed.")
        elif isinstance(other, int):
            if other != 0:
                return self.var_value / other
            raise ZeroDivisionError("Division by zero is not allowed.")
        raise TypeError(f"Unsupported operand type for /: 'liveVar' and '{type(other).__name__}'")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __iadd__(self, other):
        if isinstance(other, liveVar):
            with self.lock:
                self.var_value += other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value += other
            return self
        raise TypeError("Unsupported operand type for +=: 'liveVar' and '{}'".format(type(other).__name__))
    
    def __isub__(self, other):
        if isinstance(other, liveVar):
            with self.lock:
                self.var_value -= other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value -= other
            return self
        raise TypeError("Unsupported operand type for -=: 'liveVar' and '{}'".format(type(other).__name__))

    def __imul__(self, other):
        if isinstance(other, liveVar):
            with self.lock:
                self.var_value *= other.var_value
            return self
        elif isinstance(other, int):
            with self.lock:
                self.var_value *= other
            return self 
        raise TypeError("Unsupported operand type for *=: 'liveVar' and '{}'".format(type(other).__name__))

    def __itruediv__(self, other):
        if isinstance(other, liveVar):
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
        raise TypeError("Unsupported operand type for /=: 'liveVar' and '{}'".format(type(other).__name__))


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
            raise TypeError("Cannot change dtype of liveVar.")
        if key == 'port':
            raise TypeError("Cannot change port of liveVar.")
        raise KeyError("Invalid key '{}' for __setitem__".format(key))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        
        # do we want to reset the has_changed flag here?

        # if self.has_changed:
            # self.has_changed = False
        return self.var_value
    
    def changed(self): # check if the variable has changed since last call
        """Returns True if the variable has changed since the last call to changed()."""
        if self.has_changed:
            self.has_changed = False
            return True
        else:
            return False
        
    def update(self, value):
        """Updates the value of the variable."""
        if (type(value) != self.dtype):
            raise TypeError("Value must be of type {}".format(self.dtype))
        else:
            self.var_value = value

    def handleClient(self, connection):
        REQTYPE = "request_type: update_var"

        if connection.recv(1024).decode() == REQTYPE: # Receive request type from the client
            connection.send(str(self.dtype.__name__).encode())
        else:
            connection.close()
            return

        
        data = connection.recv(1024).decode()
        if not data:
            connection.close()
            return

        with self.lock:
            try:
                if self.dtype == bool:
                    if data == "True":
                        self.var_value = True
                        self.has_changed = True
                        print(f"{Color.BLUE}[LOG]{Color.END} {Color.GREEN}Successfully changed variable {self.tag}.{Color.END}")
                    elif data == "False":
                        self.var_value = False
                        self.has_changed = True
                        print(f"{Color.BLUE}[LOG]{Color.END} {Color.GREEN}Successfully changed variable {self.tag}.{Color.END}")
                    else:
                        print(f"{Color.RED}[ERROR]{Color.END} {Color.YELLOW}Invalid value for boolean {self.tag}.{Color.END}")
                        pass
                else:
                    self.var_value = self.dtype(data)
                    self.has_changed = True
                    print(f"{Color.BLUE}[LOG]{Color.END} {Color.GREEN}Successfully changed variable {self.tag}.{Color.END}")
            except:
                print(f"{Color.RED}[ERROR]{Color.END} {Color.YELLOW}Failed to change variable {self.tag}.{Color.END}")
                pass

        connection.close()