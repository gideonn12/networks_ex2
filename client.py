import socket
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024


def format_msg(path):
    return "GET " + path + " HTTP/1.1\nConnection: keep-alive\r\n\r\n"


def read_message(s):
    msg = b''  # Use bytes instead of string
    headers = b''
    while b'\n\n' not in headers:
        print("headers: ", headers)
        headers += s.recv(BUFFER_SIZE)
        print("headers: ", headers)
    
    header_data, _, body = headers.partition(b'\n\n')
    msg += body

    header_lines = header_data.decode('utf-8', errors='replace').splitlines()
    content_length = 0
    for line in header_lines:
        if line.lower().startswith('content-length:'):
            content_length = int(line.split(':')[1].strip())
            break

    while len(msg) < content_length:
        msg += s.recv(BUFFER_SIZE)

    return header_data + b'\r\n\r\n' + msg


def message_to_file(message, file_name):
    try:
        headers, data = message.split(b'\r\n\r\n', 1)
        headers_decoded = headers.decode('utf-8', errors='ignore')
        print(headers_decoded)
        if "200 OK" in headers_decoded:
            with open(file_name, "wb") as f:
                f.write(data)
    except UnicodeDecodeError as e:
        print(f"Failed to decode headers: {e}")
    except ValueError as e:
        print(f"Failed to split message: {e}")


# if the response


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("connected to:", TCP_IP, ":", TCP_PORT)
    while True:
        # get path from the CLI
        path = input()
        # something going to break here
        print("the path is:", path)
        print("the msg is: ", format_msg(path))
        print("the encode msg is: ", format_msg(path).encode())
        s.send(format_msg(path).encode())
        print("passed the sending")
        message = read_message(s)
        file_name = path.split("/")[-1] or "index.html"
        message_to_file(message, file_name)
        break
    break
s.close()
