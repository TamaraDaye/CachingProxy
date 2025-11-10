import socket
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import threading
import argparse

CACHE = {}


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.parse_request()


# FIXME: handle the args properly
def get_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="cmd", required=True)
    caching_proxy = subparser.add_parser("caching-proxy")
    caching_proxy.add_argument("--port", type=int)
    caching_proxy.add_argument("--origin", type=str)
    caching_proxy.add_argument("--clear-cache", type=str)
    args = parser.parse_args()

    return args


# TODO :implment the response from client if cache miss
def get_response(request):
    url = get_args().origin
    port = 80
    print(url)
    print(request)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((url, port))
            client.sendall(request)
            buffer = b""
            while True:
                chunk = client.recv(1024)
                if not chunk:
                    print(f"Client terminated connection {url}")
                    break
                buffer += chunk
            response = buffer
        except Exception as e:
            print(f"Exception found {e}")
        return response


# FIXME:Handle request data for forwarding
def request_handler(data):
    location = get_args().origin


def handle_client(client_socket, addr):
    buffer = b""

    with client_socket as client:
        try:
            while True:
                chunk = client.recv(1024)

                if not chunk:
                    print(f"Client {addr[0]} terminated connection")
                    break

                buffer += chunk

                if b"\r\n\r\n" in buffer:
                    break

            request_data = buffer

            if request_data in CACHE:
                client.sendall(CACHE[request_data])

            else:
                request = parse_request(request_data)
                print(request)
                response = get_response(request_data)
                print(response, request_data)
                # pprint.pprint(CACHE, indent=4)
                CACHE[request_data] = response
                client.sendall(response)

        except Exception as e:
            print(f"Caught an exception {e}")


def run_server():
    args = get_args()
    PORT = args.port
    SERVER_IP = "0.0.0.0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        print(f"Listening on {PORT}")

        while True:
            client_socket, addr = s.accept()
            print(f"Accepted connection from {addr[0]} : {addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()


run_server()
