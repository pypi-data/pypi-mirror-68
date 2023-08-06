import pathlib
import socket
import json
import time
import ssl
import os

class Controller:
    def __init__(self):
        self.messages = {}

    def connect(self, relay, password=None, enable_ssl=True):
        if enable_ssl:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.load_default_certs()
            unwrapped_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = self.context.wrap_socket(unwrapped_socket, server_hostname=relay)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((relay, 9100))

        # If no password is specified, default to the one in secrets/psk.txt
        if not password:
            password_path = (pathlib.Path(__file__).parent / "secrets/psk.txt").resolve()
            if os.path.exists(password_path):
                with open(password_path) as f:
                    password = f.read().rstrip("\r\n")

        if password:
            self.socket.send(password.encode("utf-8"))
            ret = self.socket.recv(1024)
            if ret == b"OK":
                return
            else:
                raise ValueError("authentication failed")

    def clear(self):
        self.messages = {}

    def add(self, port, color=None, **kwargs):
        if port not in self.messages:
            self.messages[port] = []

        message = {}
        if color is not None:
            message["color"] = color

        for key, val in kwargs.items():
            message[key] = val

        self.messages[port].append(message)

    def write(self):
        timestamp = time.time()
        self.socket.send((json.dumps(self.messages)+"\n").encode("utf-8"))
        self.messages = {}
        stats = {}
        stats["server"] = json.loads(self.socket.recv(1024).decode("utf-8"))
        stats["controller"] = {"latency":int((time.time()-timestamp)*1000)}
        return stats
