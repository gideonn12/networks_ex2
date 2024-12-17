import socket
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024


def format_msg(path):
    return "GET " + path + " HTTP/1.1\nConnection: close\r\n\r\n"


def read_message(s):
    msg = b''  # Use bytes instead of string
    headers = b''
    while b'\n\n' not in headers:
        headers += s.recv(BUFFER_SIZE)
    # if the message is empty, return false
    if headers == b'':
        return ""
    header_data, _, body = headers.partition(b'\n\n')
    msg += body

    header_lines = header_data.decode('utf-8', errors='replace').splitlines()
    print(header_lines[0])
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
        if "200 OK" in headers_decoded:
            handle_200(data, file_name)
        if "301 Moved Permanently" in headers_decoded:
            handle_301(data, file_name, headers_decoded)
        if "404 Not Found" in headers_decoded:
            handle_404(data, file_name)
    except UnicodeDecodeError as e:
        print(f"Failed to decode headers: {e}")
    except ValueError as e:
        print(f"Failed to split message: {e}")

def handle_200(msg, file_name):
    with open(file_name, "wb") as f:
        f.write(msg)

def handle_301(msg, file_name, headers):

    # we need now to send a request of the file that we got back, so do messege to file again
    location = headers.split("Location: ")[1].split("\r\n")[0]

    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(format_msg(location).encode())
    message = read_message(sock)
    file_name = location.split("/")[-1] or "index.html"
    a = message_to_file(message, file_name)
    sock.close()



def handle_404(msg, file_name):
    return

# if the response


while True:
    # get path from the CLI
    path = input()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(format_msg(path).encode())
    message = read_message(s)
    file_name = path.split("/")[-1] or "index.html"
    message_to_file(message, file_name)
    s.close()

