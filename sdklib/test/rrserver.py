import threading
import hashlib
import socket

from sdklib.compat import socketserver


class RequestResponseHandler(socketserver.BaseRequestHandler):

    REQUEST_RESPONSE_JSON = {}
    DEFAULT_RESPONSE = b"""HTTP/1.1 404 OK\n\n"""
    HTTP_200_OK_RESPONSE = b"""HTTP/1.1 200 OK\n\n"""

    @classmethod
    def add_request_response(cls, request, response=None):
        response = response or cls.HTTP_200_OK_RESPONSE

        processed_request = cls.process_request(request)
        cls.REQUEST_RESPONSE_JSON[processed_request] = response

    @classmethod
    def clear(cls):
        cls.REQUEST_RESPONSE_JSON = {}

    @staticmethod
    def clean_request(request):
        pr = b""
        req = request.replace(b'\r\n', b'\n')
        lines = req.split(b'\n')
        for line in lines:
            if (b"Host:" not in line and
                    b"Accept:" not in line):
                pr += line + b'\n'
        return pr[:-1]

    @classmethod
    def process_request(cls, request):
        cr = cls.clean_request(request)
        digest = hashlib.sha1(cr).hexdigest()
        return digest

    @staticmethod
    def recv_basic(s):
        total_data = []
        s.settimeout(1)
        while True:
            try:
                data = s.recv(1024)
            except socket.timeout:
                data = None
            if not data:
                break
            total_data.append(data)
        return b''.join(total_data)

    def handle(self):
        req = self.recv_basic(self.request)
        cur_thread = threading.current_thread()
        processed_request = self.process_request(req)
        if processed_request in self.REQUEST_RESPONSE_JSON:
            response = self.REQUEST_RESPONSE_JSON[processed_request]
        else:
            response = self.DEFAULT_RESPONSE
        self.request.sendall(response)
        self.request.close()


class RRServerManager():
    _RRSERVER = None

    @staticmethod
    def add_request_response(request, response=None):
        RequestResponseHandler.add_request_response(request, response)

    @staticmethod
    def clear():
        RequestResponseHandler.clear()

    def start_rrserver(self, host='127.0.0.1', port=0):
        if not self._RRSERVER:
            self._RRSERVER = RRServer((host, port), RequestResponseHandler)
        ip, port = self._RRSERVER.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self._RRSERVER.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        return ip, port

    def close_rrserver(self):
        if self._RRSERVER:
            self._RRSERVER.shutdown()
            self._RRSERVER.server_close()


class RRServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    manager = RRServerManager()
