from pprint import pprint


# constrcut appropriate request body for origin
def construct_request(request_string, origin):
    """
    Takes raw request from server and replaces headers with appropriate information for origin server
    and parses request body
    """
    head, _, body = request_string.decode().partition("\r\n\r\n")
    request_line, *header_lines = head.split("\r\n")
    headers = dict(line.split(":", 1) for line in header_lines)
    headers["Host"] = origin.strip()
    header_block = "".join(f"{k.strip()}: {v.strip()}\r\n" for k, v in headers.items())
    rebuilt = f"{request_line}\r\n{header_block}\r\n".encode() + body.encode()
    return rebuilt


# construct appropriate response for proxy server
def construct_response(response_string):
    """
    Takes in response from origin and adds cache header this is the response being cached
    """
    head, _, body = response_string.decode().partition("\r\n\r\n")
    response_line, *header_lines = head.split("\r\n")
    headers = dict(line.split(":", 1) for line in header_lines)
    headers["X-Cache"] = "HIT"
    header_block = "".join(f"{k.strip()}: {v.strip()}\r\n" for k, v in headers.items())
    rebuilt = f"{response_line}\r\n{header_block}\r\n".encode() + body.encode()
    return rebuilt
