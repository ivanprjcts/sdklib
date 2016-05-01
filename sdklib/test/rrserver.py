import threading
import SocketServer


class RequestResponseHandler(SocketServer.BaseRequestHandler):

    REQUEST_RESPONSE_JSON = {}
    DEFAULT_RESPONSE = """HTTP/1.1 404 OK\n\n"""
    HTTP_200_OK_RESPONSE = """HTTP/1.1 200 OK\n\n"""

    @classmethod
    def add_request_response(cls, request, response=HTTP_200_OK_RESPONSE):
        cls.REQUEST_RESPONSE_JSON[request] = response

    @classmethod
    def clear(cls):
        cls.REQUEST_RESPONSE_JSON = {}

    def process_request(self, request):
        pr = ""
        req = request.replace('\r\n', '\n')
        lines = req.split('\n')
        for line in lines:
            if ("Host:" not in line and
                    "Accept:" not in line):
                pr += line + '\n'
        return pr[:-1]

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        processed_data = self.process_request(data)
        if processed_data in self.REQUEST_RESPONSE_JSON:
            response = self.REQUEST_RESPONSE_JSON[processed_data]
        else:
            response = self.DEFAULT_RESPONSE
        self.request.sendall(response)


class RRServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class RRServerManager():
    _RRSERVER = None

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

manager = RRServerManager()