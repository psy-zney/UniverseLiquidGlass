import argparse
import base64
import json
import socket
import time
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')


class Marionette:
    def __init__(self, port=2839):
        self.sock = socket.create_connection(('127.0.0.1', port), timeout=12)
        self.sock.settimeout(20)
        self.number = 0
        self.receive()

    def receive(self):
        prefix = bytearray()
        while True:
            ch = self.sock.recv(1)
            if not ch:
                raise RuntimeError('Browser closed the connection')
            if ch == b':':
                break
            prefix.extend(ch)
        size = int(prefix)
        payload = bytearray()
        while len(payload) < size:
            payload.extend(self.sock.recv(size - len(payload)))
        return json.loads(payload)

    def command(self, name, params=None):
        self.number += 1
        data = json.dumps([0, self.number, name, params or {}]).encode()
        self.sock.sendall(str(len(data)).encode() + b':' + data)
        response = self.receive()
        if response[2]:
            raise RuntimeError(json.dumps(response[2]))
        return response[3]
