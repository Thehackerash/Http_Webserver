
#response
def response(req, status, body="", headers={}):
    #print("response", req)
    if headers is None:
        headers = {}

    headers_copy = headers.copy()
    
    #build status line
    status_line = b""
    if status == 200:
        status_line += b"HTTP/1.1 200 OK\r\n"
    elif status == 404:
        status_line += b"HTTP/1.1 404 Not Found\r\n"
    elif status == 500:
        status_line += b"HTTP/1.1 500 Internal Server Error\r\n"
    else:
        status_line += b"HTTP/1.1 500 Internal Server Error\r\n"  # Default to 500 for unknown status codes

    # Build headers
    request_headers = b""
    if (encoding := req.get("headers", {}).get("Accept-Encoding", None)):
        print("Accept-Enc", encoding)
        encodings = encoding.split(", ")
        print("encodings", encodings)
        if "gzip" in encodings:
            headers_copy["content-encoding"] = "gzip"

    # Check if "Accept-Encoding" header exists in the request and contains "gzip"
    if "content-type" not in headers_copy:
        headers_copy["content-type"] = "text/plain"
    if body:
        headers_copy["content-length"] = str(len(body))

    for key, value in headers_copy.items():
        request_headers += f"{key}: {value}\r\n".encode()

    # Check if "Accept-Encoding" header exists in the request and contains "gzip"
    encoding = req.get("headers", {}).get("Accept-Encoding", "")
    bodyb = body.encode()

    # Encode body if present
    bodyb = b""
    if "gzip" in encoding.split(", "):
        headers_copy["Content-Encoding"] = "gzip"
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode='w') as gz:
            gz.write(bodyb)
        bodyb = out.getvalue()

    # Build response
    response = status_line + request_headers + b"\r\n" + bodyb
    print(response)
    return response


def to_hex(data):
    return " ".join(f"{byte:02X}" for byte in data)
