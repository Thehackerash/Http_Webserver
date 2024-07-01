from response import response
import sys

def parser(request):
    #print("parser")
    output = {"method": "", "path": "", "headers": {}, "body": ""}
    lines = request.split("\r\n")
    if len(lines) < 3:
        return None
    
    status_line = lines[0].split(" ")

    if (not status_line[0]) or status_line[0] not in ["GET", "POST", "PUT", "HEAD"]:
        return None
    if (not status_line[1]) or status_line[1][0] != "/":
        return None
    
    output["method"] = status_line[0]
    output["path"] = status_line[1]
    #print(output["path"])
    lines = lines[1:]
    c = 0
    for line in lines:
        if line == "":
            break
        key, value = line.split(": ")
        output["headers"][key] = value
        c += 1
    output["body"] = lines[c+1]
    #print(output)
    return output

def handle_request(conn, req, directory=""):
    #print("handle request")
    if req['path'] == "/":
       return response(req, 200)
    
    elif req["path"].startswith("/echo/"):
        return response(req, 200, req["path"][6:])
    
    elif req["path"] == "/user-agent":
        print("user-agent")
        ua = req["headers"]["User-Agent"]
        return response(req, 200, ua)
    
    elif req["path"].startswith("/files"):
        print("/files is path")
        filename = req["path"][7:]
        print(f"directory : {directory}, filename : {filename}")
        try:
            if req["method"] == "GET":
                with open(f"{directory}/{filename}", "r") as file:
                    body = file.read()
                response_file = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\ncontent-length: {len(body)}\r\n\r\n{body}".encode();
                return response_file
            elif req["method"] == "POST":
                with open(f"{directory}/{filename}", "w") as file:
                    file.write(req["body"])
                response_file = f"HTTP/1.1 201 Created\r\n\r\n".encode();
                return response_file
        except Exception as e:
            response_file = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            return response_file
    else :
        #print("404")
        return response(req, 404)

def handle_client(conn, directory=""):
    try:
        byte = []
        while (byte := conn.recv(1024)) != b"":
            request = byte.decode()
            print(request)
            parsed_req = parser(request) 
            if(parsed_req == None):
                conn.send(str.encode("HTTP/1.1 500 internal server error\r\n\r\n"))
                return conn.close()
        
            conn.send(handle_request(conn, parsed_req, directory))
            return conn.close()
    except Exception as e:
        print("handle client error", e)
