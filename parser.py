import email
import pprint


def parse_request(request_string):
    request, headers = request_string.decode().split("\r\n", 1)

    message = email.message_from_string(headers)

    headers = dict(message.items())

    pprint.pprint(headers, width=160)

    return request, headers


def construct_request(request_string, origin):
    request, headers = parse_request(request_string)

    headers["Host"] = origin

    request_string = (
        f"{request}"
        + "\r\n"
        + "".join(f"{k}: {v} \r\n" for k, v in headers.items())
        + "\r\n"
    )

    return request_string.encode("utf-8")
