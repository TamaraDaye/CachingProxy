import email


def parse_request(request_string):
    request, headers = request_string.decode().split("\r\n", 1)
    message = email.message_from_string(headers)
    headers = dict(message.items())
    return request, headers


def construct_request(request_string, origin, body=b""):
    request_line, headers = parse_request(request_string)

    headers["Host"] = origin

    headers["Connection"] = "close"

    headers["Accept-Encoding"] = "identity"

    header_block = "".join(f"{k}: {v}\r\n" for k, v in headers.items())

    full_request = (f"{request_line}\r\n{header_block}\r\n").encode("utf-8") + body

    return full_request
