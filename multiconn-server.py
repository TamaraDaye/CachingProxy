import socket
import ssl
import parser
import threading
import argparse

CACHE = {}


# argument parser for the caching server port and domain to cache responses
def get_args():
    """
    This function returns an argparse namesapce containning the arguments for the application
    port: port to run caching server origin
    origin: the domain to reverse proxy for
    """
    args_parser = argparse.ArgumentParser()
    subparser = args_parser.add_subparsers(dest="cmd", required=True)
    caching_proxy = subparser.add_parser("caching-proxy")
    caching_proxy.add_argument("--port", type=int)
    caching_proxy.add_argument("--origin", type=str)
    caching_proxy.add_argument("--clear-cache", type=str)
    args = args_parser.parse_args()

    return args


# TODO :implment the response from client if cache miss
def get_response(request_data):
    """
    Function to obtain response data for client socket instance uses raw requests
    if request is cached return directly from the cache else creates a socket and hits the origin
    endpoint for appropriate request caches after
    """
    url = get_args().origin
    port = 443

    # Customer HTTP request parser to obtain the req line for caching and fixed headers for appropriate request forwarding
    request, request_line = parser.construct_request(request_data, url)

    # return cached responsed if in cache
    if request_line in CACHE:
        print("Getting data from Cache")
        return CACHE[request_line]

    # create a ssl object to secure tcp connection and use HTTPs
    context = ssl.create_default_context()

    # create a tcp connection to be wrapped around with tls
    with socket.create_connection((url, port)) as sock:
        # wraps tcp socket with tls security encrypting data sent and received
        with context.wrap_socket(sock, server_hostname=url) as ssock:
            ssock.sendall(request)

            response = b""

            while True:
                chunk = ssock.recv(4096)

                if not chunk:
                    print("server terminated connection")
                    break
                response += chunk
    CACHE[request_line] = parser.construct_response(response)
    print("Getting data from origin")
    return response


def handle_client(client_socket, addr):
    """
    Function of handling client socket instances from their threads
    """
    buffer = b""

    with client_socket as client:
        try:
            while True:
                chunk = client.recv(1024)

                if not chunk:
                    print(f"Client {addr[0]} terminated connection")
                    break

                buffer += chunk

                if b"\r\n\r\n" in buffer:  # stop at the end of the request
                    break

            request_data = buffer
            response = get_response(request_data)
            client.sendall(response)

        except Exception as e:
            print(f"Caught an exception {e}")


def run_server():
    """
    create socket to act as server and uses multithreading
    to spin individual threads for each client socket returned to avoid
    blocking the main thread of execution
    """
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


if __name__ == "__main__":
    run_server()
