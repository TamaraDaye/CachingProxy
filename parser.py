import email
from pprint import pprint


def parse_request(request_string):
    request, headers = request_string.decode().split("\r\n", 1)
    message = email.message_from_string(headers)
    headers = dict(message.items())
    pprint(headers, width=160)
    return request, headers


def construct_request(request_string, origin, body=b""):
    request_line, headers = parse_request(request_string)

    headers["Host"] = origin

    headers["Connection"] = "close"

    headers["Accept-Encoding"] = "identity"

    header_block = "".join(f"{k}: {v}\r\n" for k, v in headers.items())

    full_request = (f"{request_line}\r\n{header_block}\r\n").encode("utf-8") + body

    return full_request


def construct_response(response_string, hit=False):
    if hit is False:
        return response_string

    head, _, body = response_string.partition("\r\n\r\n")
    response_line, *header_lines = head.split("\r\n")
    headers = dict(line.split(":", 1) for line in header_lines)
    headers["X-Cache"] = "Hit"
    header_block = "".join(f"{k.strip()}: {v.strip()}\r\n" for k, v in headers.items())
    rebuilt = f"{response_line}\r\n{header_block}\r\n".encode() + body.encode()
    return rebuilt


s = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nETag: "bc2473a18e003bdb249eba5ce893033f:1760028122.592274"\r\nLast-Modified: Thu, 09 Oct 2025 16:42:02 GMT\r\nVary: Accept-Encoding\r\nCache-Control: max-age=86000\r\nDate: Mon, 10 Nov 2025 14:16:08 GMT\r\nContent-Length: 513\r\nConnection: close\r\nAlt-Svc: h3=":443"; ma=93600\r\n\r\n<!doctype html><html lang="en"><head><title>Example Domain</title><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{background:#eee;width:60vw;margin:15vh auto;font-family:system-ui,sans-serif}h1{font-size:1.5em}div{opacity:0.8}a:link,a:visited{color:#348}</style><body><div><h1>Example Domain</h1><p>This domain is for use in documentation examples without needing permission. Avoid use in operations.<p><a href="https://iana.org/domains/example">Learn more</a></div></body></html>\n'


parse_request(s)
