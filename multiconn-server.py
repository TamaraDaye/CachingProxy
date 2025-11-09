import socket
import threading
import argparse

CACHE = {}


def get_args():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="cmd", required=True)

    caching_proxy = subparser.add_parser("caching_proxy")

    caching_proxy.add_argument("--port", type=int)

    caching_proxy.add_argument("--host", type=str)

    args = parser.parse_args()

    return args.port, args.host


def handle_client(client_socket, addr):
    buffer = b""

    with client_socket as client:
        try:
            while True:
                request = client.recv(1024)

                if not request:
                    print(f"Client {addr[0]} terminated connection")
                    break

                buffer += request
                CACHE[addr] = buffer
                print(CACHE)
                client.send(b"Recieved your request")
        except Exception as e:
            print(f"Caught an exception {e}")


def run_server():
    server_ip = "0.0.0.0"
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        print(f"Listening on {server_ip}")

        while True:
            client_socket, addr = s.accept()
            print(f"Accepted connection from {addr[0]} : {addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()


run_server()
